"""
Script to run the backend server with mock data.
"""
import os
import subprocess
import sys

def run_backend():
    """
    Run the backend server with mock data.
    """
    print("Starting Email to ERP Agent backend server with mock data...")
    
    # Change to the backend directory
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    os.chdir(backend_dir)
    
    # Install dependencies if needed
    print("Checking dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run the server
    print("Starting server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    run_backend()
