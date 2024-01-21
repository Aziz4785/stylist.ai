import pymongo
import time
import sys

def wait_for_mongo(db_uri, max_attempts=10, delay=5):
    attempts = 0
    client = None
    while attempts < max_attempts:
        try:
            print(f"Attempting to connect to MongoDB (Attempt {attempts + 1}/{max_attempts})...")
            client = pymongo.MongoClient(db_uri, serverSelectionTimeoutMS=5000)  # 5 second timeout
            # Trigger a server selection process
            client.admin.command('ping')
            print("MongoDB is ready!")
            return True
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"Connection attempt failed: {err}")
            attempts += 1
            time.sleep(delay)

    print("Failed to connect to MongoDB after several attempts.")
    return False

if __name__ == "__main__":
    mongo_uri = "mongodb://mongodb:27017/" 
    if not wait_for_mongo(mongo_uri):
        sys.exit(1)
