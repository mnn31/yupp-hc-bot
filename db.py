# db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["hypercharged"]

# Collections
users = db["users"]
themes = db["themes"]
follows = db["follows"]
