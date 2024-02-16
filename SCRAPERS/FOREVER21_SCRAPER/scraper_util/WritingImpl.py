from .WritingStrategy import *
import pymongo
import os
import sys

zalando_scraper_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(zalando_scraper_directory)

try:
    import config
except ModuleNotFoundError:
    print("Failed to import config. Current sys.path:", sys.path)  
    raise


db_uri = config.db_uri
db_name = config.db_name

class IncrementalWritingStrategy(WritingStrategy):
    def __init__(self,collection_name):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def write(self, data):
        #mongodb :
          # Assuming 'data' is a dictionary or a list of dictionaries
        if isinstance(data, dict):
            self.collection.insert_one(data)
        elif isinstance(data, list):
            self.collection.insert_many(data)
        else:
            raise ValueError("Data is neither a dictionary nor a list of dictionaries")


class BatchWritingStrategy(WritingStrategy):
    """
    to be implemented...
    """
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.batch_data = []

    def write(self, data):
        self.batch_data.append(data)
        
