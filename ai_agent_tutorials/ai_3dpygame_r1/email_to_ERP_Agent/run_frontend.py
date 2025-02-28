"""
Script to run the frontend server.
"""
import os
import subprocess
import sys

def run_frontend():
    """
    Run the frontend server.
    """
    print("Starting Email to ERP Agent frontend server...")
    
    # Change to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    os.chdir(frontend_dir)
    
    # Install dependencies if needed
    print("Checking dependencies...")
    subprocess.run(["npm", "install"])
    
    # Run the server
    print("Starting server...")
    subprocess.run(["npm", "run", "dev"])

if __name__ == "__main__":
    run_frontend()
