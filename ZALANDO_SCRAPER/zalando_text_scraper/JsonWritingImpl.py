from JsonWritingStrategy import *
import pymongo
import json
import os

db_uri = "mongodb://localhost:27017/"
db_name = "mydatabase"

class IncrementalJsonWritingStrategy(JsonWritingStrategy):
    def __init__(self,collection_name):
        self.is_first_entry = True
        #mongodb :
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def write_json(self, data):
        #mongodb :
          # Assuming 'data' is a dictionary or a list of dictionaries
        if isinstance(data, dict):
            self.collection.insert_one(data)
        elif isinstance(data, list):
            self.collection.insert_many(data)
        else:
            raise ValueError("Data is neither a dictionary nor a list of dictionaries")


class BatchJsonWritingStrategy(JsonWritingStrategy):
    """
    to be implemented...
    """
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.batch_data = []

    def write_json(self, data):
        self.batch_data.append(data)
        
