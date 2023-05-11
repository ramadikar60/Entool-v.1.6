from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Konfigurasi MongoDB Atlas
CLUSTER = os.getenv("CLUSTER")
DB = os.getenv("DB")
COLLECTION = os.getenv("COLLECTION")

cluster = MongoClient(CLUSTER)
db = cluster[DB]
collection = db[COLLECTION]