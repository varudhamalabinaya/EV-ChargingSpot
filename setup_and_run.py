#!/usr/bin/env python3
"""
Complete setup and run script for Plug Spotter Pro
Handles backend and frontend startup with MongoDB connection testing
"""
import subprocess
import sys
import os
import time
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT


def run_command(cmd, cwd=None, name="Command"):
    """Run a command and return success status"""
    try:
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print(f"{'='*60}")
        print(f"Command: {' '.join(cmd)}")
        print(f"Working directory: {cwd or os.getcwd()}\n")
        
        result = subprocess.run(cmd, cwd=cwd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error running {name}: {e}")
        return False


def install_backend_deps():
    """Install backend dependencies"""
    os.chdir(PROJECT_ROOT)
    
    deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "motor==3.3.2",
        "pymongo==4.6.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0"
    ]
    
    print("\n" + "="*60)
    print("BACKEND SETUP: Installing Python dependencies")
    print("="*60)
    
    for dep in deps:
        print(f"  Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", dep])
    
    print("✓ Backend dependencies installed")
    return True


async def test_mongodb():
    """Test MongoDB connection"""
    print("\n" + "="*60)
    print("TESTING: MongoDB Connection")
    print("="*60)
    
    try:
        from dotenv import load_dotenv
        
        load_dotenv(PROJECT_ROOT / ".env")
        
        mongo_uri = os.getenv("MONGODB_URI")
        mongo_db = os.getenv("MONGODB_DB", "plugspotter")
        
        if not mongo_uri:
            print("✗ MONGODB_URI not found in .env file")
            return False
        
        print(f"  Database: {mongo_db}")
        print(f"  Connecting...")
        
        from motor.motor_asyncio import AsyncIOMotorClient
        
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=10000)
        await client.admin.command('ping')
        
        # Test collection access
        db = client[mongo_db]
        await db.stations.find_one()
        
        print("✓ MongoDB connection successful!")
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("\n  Troubleshooting:")
        print("  1. Verify MONGODB_URI in .env file")
        print("  2. Check MongoDB Atlas credentials")
        print("  3. Whitelist your IP in MongoDB Atlas")
        print("  4. Ensure internet connection is stable")
        return False


def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n" + "="*60)
    print("FRONTEND SETUP: Installing npm dependencies")
    print("="*60)
    
    os.chdir(FRONTEND_DIR)
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-dotenv"])
    
    return run_command(["npm", "install"], cwd=FRONTEND_DIR, name="npm install")


def main():
    print("\n" + "█"*60)
    print("█ PLUG SPOTTER PRO - Complete Setup & Launch")
    print("█"*60)
    
    # Step 1: Install backend dependencies
    print("\n[1/5] Installing Backend Dependencies...")
    if not install_backend_deps():
        print("⚠ Some dependencies may have failed, continuing anyway...")
    
    # Step 2: Test MongoDB connection
    print("\n[2/5] Testing MongoDB Connection...")
    if not asyncio.run(test_mongodb()):
        print("\n⚠ MongoDB connection failed!")
        print("Please verify your .env configuration and try again.")
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Step 3: Install frontend dependencies
    print("\n[3/5] Installing Frontend Dependencies...")
    if not install_frontend_deps():
        print("✗ Frontend installation failed")
        sys.exit(1)
    
    print("\n" + "█"*60)
    print("█ SETUP COMPLETE - Ready to launch servers")
    print("█"*60)
    
    print("\n[4/5] LAUNCHING BACKEND SERVER...")
    print("      URL: http://localhost:8000")
    print("      API Docs: http://localhost:8000/docs")
    print("\n[5/5] LAUNCHING FRONTEND SERVER...")
    print("      URL: http://localhost:5173")
    
    print("\n" + "="*60)
    print("Starting services...\n")
    
    # Start backend in background
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    print("⟳ Backend server starting...")
    time.sleep(3)  # Give backend time to start
    
    # Start frontend
    print("⟳ Frontend server starting...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    print("\n" + "█"*60)
    print("█ SERVERS RUNNING")
    print("█"*60)
    print("\n✓ Backend:  http://localhost:8000")
    print("✓ Frontend: http://localhost:5173")
    print("✓ API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        # Keep processes running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down services...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait(timeout=5)
        frontend_process.wait(timeout=5)
        print("✓ Services stopped")


if __name__ == "__main__":
    main()
