import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.player import Player

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# Initialize the MongoClient globally so it can be reused
client = AsyncMongoClient(MONGO_URI) if MONGO_URI else None
db = client['Sports'] if client is not None else None
collection = db['squash'] if db is not None else None

async def init_db():
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI not found in environment")
    # Initialize Beanie with our Document models
    await init_beanie(database=db, document_models=[Player])
