#!/usr/bin/env python3
"""
Quick Setup Script for UPI Payment Simulation System
This script helps set up and run the complete system
"""

import os
import sys
import subprocess
import webbrowser
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    print(f"[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[✓] {description} completed successfully")
            return True
        else:
            print(f"[✗] {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False

def main():
    print_header("UPI Payment Simulation System - Setup & Launch")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("[i] Project Directory:", script_dir)
    print("[i] Python Version:", sys.version.split()[0])
    
    # Check if virtual environment exists
    venv_path = os.path.join(script_dir, '.venv')
    if not os.path.exists(venv_path):
        print_header("Creating Virtual Environment")
        if not run_command(f"{sys.executable} -m venv .venv", "Create virtual environment"):
            print("[!] Failed to create virtual environment")
            return
    
    # Determine Python executable in venv
    if sys.platform == "win32":
        python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
        pip_exe = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        python_exe = os.path.join(venv_path, 'bin', 'python')
        pip_exe = os.path.join(venv_path, 'bin', 'pip')
    
    # Check if requirements are installed
    print_header("Installing Dependencies")
    if os.path.exists('requirements.txt'):
        if not run_command(f"{pip_exe} install -r requirements.txt -q", "Install dependencies"):
            print("[!] Failed to install dependencies")
            return
    
    # Remove old database to start fresh (optional)
    db_file = 'upi_system.db'
    if os.path.exists(db_file):
        response = input(f"\n[?] Database '{db_file}' exists. Reset it? (y/n): ").lower()
        if response == 'y':
            os.remove(db_file)
            print("[✓] Database reset")
    
    print_header("System Ready - Starting Server")
    print("[i] Starting FastAPI server on http://localhost:8000")
    print("[i] Press Ctrl+C to stop the server")
    print("\n[✓] Frontend URL: http://localhost:8000")
    print("[✓] API Docs: http://localhost:8000/docs")
    print("[✓] Alternative Docs: http://localhost:8000/redoc")
    
    # Open browser
    print("\n[i] Opening frontend in browser...")
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:8000')
    except Exception as e:
        print(f"[!] Could not open browser: {e}")
    
    # Start the server
    print("\n" + "="*60)
    cmd = f"{python_exe} -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    os.system(cmd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Server stopped by user")
        sys.exit(0)
