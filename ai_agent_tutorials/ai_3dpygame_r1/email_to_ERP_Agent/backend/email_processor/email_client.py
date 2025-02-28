"""
Email client module for fetching and processing emails.
"""
import base64
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models.email import EmailMessage, Attachment
from ..models.sku import SKUInfo


class GmailClient:
    """
    Client for interacting with Gmail API.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, token_path: str, credentials_path: str):
        """
        Initialize the Gmail client.
        
        Args:
            token_path: Path to the token file
            credentials_path: Path to the credentials file
        """
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.creds = None
        self.service = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API.
        
        Returns:
            bool: True if authentication was successful
        """
        try:
            if os.path.exists(self.token_path):
                self.creds = Credentials.from_authorized_user_info(
                    json.loads(open(self.token_path).read()),
                    self.SCOPES
                )
            
            # If there are no valid credentials, let the user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.token_path, 'w') as token:
                    token.write(self.creds.to_json())
            
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
        
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False
    
    def fetch_emails(self, query: str = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch emails from Gmail.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email messages
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return []
            
            # Default query to fetch recent emails
            if not query:
                query = 'is:unread'
            
            # Get messages that match the query
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return []
            
            # Fetch full message details for each message
            detailed_messages = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id'],
                    format='full'
                ).execute()
                detailed_messages.append(msg)
            
            return detailed_messages
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def parse_email(self, gmail_message: Dict[str, Any]) -> EmailMessage:
        """
        Parse Gmail message into EmailMessage model.
        
        Args:
            gmail_message: Gmail message object
            
        Returns:
            EmailMessage object
        """
        # Extract headers
        headers = gmail_message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
        from_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
        date_str = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
        
        # Parse date
        try:
            # This is a simplified date parser and may need to be enhanced
            date = datetime.strptime(date_str.split(' +')[0].strip(), '%a, %d %b %Y %H:%M:%S')
        except:
            date = datetime.now()
        
        # Extract body
        body = self._get_email_body(gmail_message['payload'])
        
        # Extract attachments
        attachments = self._get_attachments(gmail_message['payload'], gmail_message['id'])
        
        return EmailMessage(
            id=gmail_message['id'],
            thread_id=gmail_message['threadId'],
            subject=subject,
            from_email=from_email,
            date=date,
            body=body,
            attachments=attachments,
            labels=gmail_message.get('labelIds', []),
            processed=False
        )
    
    def _get_email_body(self, payload: Dict[str, Any]) -> str:
        """
        Extract email body from payload.
        
        Args:
            payload: Email payload
            
        Returns:
            Email body as text
        """
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                elif 'parts' in part:
                    return self._get_email_body(part)
        elif payload['mimeType'] == 'text/plain':
            if 'data' in payload['body']:
                return base64.urlsafe_b64decode(
                    payload['body']['data']).decode('utf-8')
        
        return ""
    
    def _get_attachments(self, payload: Dict[str, Any], message_id: str) -> List[Attachment]:
        """
        Extract attachments from email payload.
        
        Args:
            payload: Email payload
            message_id: Gmail message ID
            
        Returns:
            List of Attachment objects
        """
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if 'filename' in part and part['filename']:
                    if 'body' in part and 'attachmentId' in part['body']:
                        attachment = Attachment(
                            id=part['body']['attachmentId'],
                            filename=part['filename'],
                            mime_type=part['mimeType'],
                            size=part['body'].get('size', 0),
                            content=None  # We don't fetch the content here to save bandwidth
                        )
                        attachments.append(attachment)
                
                if 'parts' in part:
                    attachments.extend(self._get_attachments(part, message_id))
        
        return attachments
    
    def get_attachment_content(self, message_id: str, attachment_id: str) -> Optional[bytes]:
        """
        Fetch attachment content.
        
        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID
            
        Returns:
            Attachment content as bytes
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            
            if 'data' in attachment:
                return base64.urlsafe_b64decode(attachment['data'])
            
            return None
        
        except HttpError as error:
            print(f"An error occurred fetching attachment: {error}")
            return None
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark an email as read.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return False
            
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            return True
        
        except HttpError as error:
            print(f"An error occurred marking message as read: {error}")
            return False


class EmailProcessor:
    """
    Process emails to extract SKU information.
    """
    def __init__(self, email_client: GmailClient):
        """
        Initialize the email processor.
        
        Args:
            email_client: Email client for fetching emails
        """
        self.email_client = email_client
    
    def process_emails(self, query: str = None, max_results: int = 10) -> List[Tuple[EmailMessage, List[SKUInfo]]]:
        """
        Process emails to extract SKU information.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of emails to process
            
        Returns:
            List of tuples containing EmailMessage and extracted SKUInfo
        """
        results = []
        
        # Fetch emails
        gmail_messages = self.email_client.fetch_emails(query, max_results)
        
        for gmail_message in gmail_messages:
            # Parse email
            email = self.email_client.parse_email(gmail_message)
            
            # Extract SKUs
            skus = self.extract_skus(email)
            
            # Mark as processed
            if skus:
                email.processed = True
                self.email_client.mark_as_read(email.id)
            
            results.append((email, skus))
        
        return results
    
    def extract_skus(self, email: EmailMessage) -> List[SKUInfo]:
        """
        Extract SKU information from email.
        
        Args:
            email: EmailMessage object
            
        Returns:
            List of SKUInfo objects
        """
        skus = []
        
        # Extract SKUs from email body
        body_skus = self._extract_skus_from_text(email.body)
        skus.extend(body_skus)
        
        # Extract SKUs from attachments if needed
        # This would require parsing different file formats (CSV, Excel, PDF, etc.)
        # For simplicity, we're only extracting from the email body in this example
        
        return skus
    
    def _extract_skus_from_text(self, text: str) -> List[SKUInfo]:
        """
        Extract SKU information from text.
        
        Args:
            text: Text to extract SKUs from
            
        Returns:
            List of SKUInfo objects
        """
        skus = []
        
        # Define regex patterns for SKU extraction
        # This is a simplified example - real implementations would be more sophisticated
        sku_pattern = r'SKU[:\s]+([A-Z0-9\-]+)'
        quantity_pattern = r'QTY[:\s]+(\d+)'
        
        # Find all SKUs
        sku_matches = re.finditer(sku_pattern, text, re.IGNORECASE)
        
        for match in sku_matches:
            sku_code = match.group(1).strip()
            
            # Try to find quantity for this SKU
            # This is a simplified approach - in reality, you'd need more context-aware parsing
            quantity = 1
            qty_match = re.search(quantity_pattern, text[match.start():match.start()+100], re.IGNORECASE)
            if qty_match:
                quantity = int(qty_match.group(1))
            
            sku_info = SKUInfo(
                sku_code=sku_code,
                quantity=quantity,
                source_email_id=None,  # Will be set later
                validated=False,
                erp_entry_id=None
            )
            
            skus.append(sku_info)
        
        return skus
