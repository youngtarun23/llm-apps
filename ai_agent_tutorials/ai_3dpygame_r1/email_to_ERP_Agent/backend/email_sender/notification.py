"""
Email notification module for sending follow-up emails.
"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional

from ..models.sku import SKUInfo


class EmailSender:
    """
    Email sender for sending notifications.
    """
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """
        Initialize the email sender.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            username: SMTP username
            password: SMTP password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            html_body: Email body (HTML)
            
        Returns:
            True if email was sent successfully
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email
            
            # Attach plain text version
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach HTML version if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False


class NotificationService:
    """
    Service for sending notifications.
    """
    def __init__(self, email_sender: EmailSender):
        """
        Initialize the notification service.
        
        Args:
            email_sender: Email sender for sending notifications
        """
        self.email_sender = email_sender
        self.logger = logging.getLogger(__name__)
    
    def send_invalid_sku_notification(self, to_email: str, invalid_skus: List[SKUInfo], original_email_subject: str) -> bool:
        """
        Send notification for invalid SKUs.
        
        Args:
            to_email: Recipient email address
            invalid_skus: List of invalid SKUInfo objects
            original_email_subject: Subject of the original email
            
        Returns:
            True if notification was sent successfully
        """
        subject = f"Invalid SKUs in email: {original_email_subject}"
        
        # Create plain text body
        body = "The following SKUs in your email could not be validated:\n\n"
        for sku in invalid_skus:
            body += f"- SKU: {sku.sku_code}, Quantity: {sku.quantity}\n"
        
        body += "\nPlease verify these SKUs and try again."
        
        # Create HTML body
        html_body = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h2>Invalid SKUs in your email</h2>
            <p>The following SKUs in your email could not be validated:</p>
            <table>
                <tr>
                    <th>SKU Code</th>
                    <th>Quantity</th>
                </tr>
        """
        
        for sku in invalid_skus:
            html_body += f"""
                <tr>
                    <td>{sku.sku_code}</td>
                    <td>{sku.quantity}</td>
                </tr>
            """
        
        html_body += """
            </table>
            <p>Please verify these SKUs and try again.</p>
        </body>
        </html>
        """
        
        return self.email_sender.send_email(to_email, subject, body, html_body)
    
    def send_processing_confirmation(self, to_email: str, valid_skus: List[SKUInfo], original_email_subject: str) -> bool:
        """
        Send processing confirmation.
        
        Args:
            to_email: Recipient email address
            valid_skus: List of valid SKUInfo objects
            original_email_subject: Subject of the original email
            
        Returns:
            True if confirmation was sent successfully
        """
        subject = f"SKUs processed successfully: {original_email_subject}"
        
        # Create plain text body
        body = "The following SKUs have been processed successfully:\n\n"
        for sku in valid_skus:
            body += f"- SKU: {sku.sku_code}, Quantity: {sku.quantity}\n"
        
        body += "\nThank you for your order."
        
        # Create HTML body
        html_body = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                .success { color: green; }
            </style>
        </head>
        <body>
            <h2>SKUs Processed Successfully</h2>
            <p>The following SKUs have been processed successfully:</p>
            <table>
                <tr>
                    <th>SKU Code</th>
                    <th>Quantity</th>
                    <th>Status</th>
                </tr>
        """
        
        for sku in valid_skus:
            html_body += f"""
                <tr>
                    <td>{sku.sku_code}</td>
                    <td>{sku.quantity}</td>
                    <td class="success">Processed</td>
                </tr>
            """
        
        html_body += """
            </table>
            <p>Thank you for your order.</p>
        </body>
        </html>
        """
        
        return self.email_sender.send_email(to_email, subject, body, html_body)


class MockEmailSender(EmailSender):
    """
    Mock email sender for testing.
    """
    def __init__(self):
        """
        Initialize the mock email sender.
        """
        super().__init__("smtp.example.com", 587, "noreply@example.com", "password")
        self.sent_emails = []
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send an email (mock implementation).
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            html_body: Email body (HTML)
            
        Returns:
            True if email was sent successfully
        """
        self.sent_emails.append({
            "to": to_email,
            "subject": subject,
            "body": body,
            "html_body": html_body
        })
        
        return True
