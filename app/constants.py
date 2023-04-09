from pymongo import MongoClient
import os, dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from twilio.rest import Client


dotenv.load_dotenv()
db = MongoClient(os.environ.get('MONGO_URI', None)).taskhopper
motor = AsyncIOMotorClient(os.environ.get('MONGO_URI', None)).taskhopper
twilio = Client(os.environ.get('TWILIO_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
