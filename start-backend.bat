@echo off
cd /d "%~dp0"

echo Installing backend dependencies...
pip install --upgrade pip
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 motor==3.3.2 pymongo==4.6.0 pydantic==2.5.0 pydantic-settings==2.1.0 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.6

echo.
echo Testing MongoDB connection...
python << 'EOF'
import asyncio
import sys
sys.path.insert(0, '%cd%')

async def test_mongo():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            print("ERROR: MONGODB_URI not found in .env")
            return False
        
        print(f"Connecting to MongoDB...")
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("✓ MongoDB connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

result = asyncio.run(test_mongo())
sys.exit(0 if result else 1)
EOF

echo.
echo Starting backend server on http://localhost:8000...
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
