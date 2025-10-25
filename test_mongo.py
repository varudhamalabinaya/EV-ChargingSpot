import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_mongo():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        
        mongo_uri = os.getenv('MONGODB_URI')
        mongo_db = os.getenv('MONGODB_DB', 'plugspotter')
        
        if not mongo_uri:
            print("✗ MONGODB_URI not found in .env")
            return False
        
        print(f"Testing MongoDB connection...")
        print(f"Database: {mongo_db}")
        print(f"URI: {mongo_uri[:50]}...")
        
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=10000)
        await client.admin.command('ping')
        print("✓ MongoDB connection successful!")
        
        db = client[mongo_db]
        collections = await db.list_collection_names()
        print(f"✓ Collections: {collections}")
        
        client.close()
        return True
    except Exception as e:
        print(f"✗ MongoDB failed: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mongo())
    exit(0 if result else 1)
