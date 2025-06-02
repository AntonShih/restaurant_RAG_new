import os
from dotenv import load_dotenv

load_dotenv()

def get_mongodb_config():
    return {
        "uri": os.getenv("MONGODB_URI"),
        "db_name": os.getenv("MONGODB_DB_NAME")
    }
