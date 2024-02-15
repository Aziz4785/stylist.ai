import re
import pymongo

import f21_config
from urllib.parse import urlparse, parse_qs
def remove_WashCold(collection_name):
    db_uri = f21_config.db_uri
    db_name = f21_config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    pattern1 =  "Machine wash cold"
    pattern2 =  "Hand wash cold"
    pattern3 =  "- Machine wash cold"
    pattern4 =  "- Hand wash cold"
    # Iterate through the documents in the collection
    for document in collection.find():
        if isinstance(document, dict):
            for key in document:
                if isinstance(document[key], str):
                    document[key] = document[key].replace(pattern3, "")
                    document[key] = document[key].replace(pattern4, "")
                    document[key] = document[key].replace(pattern1, "")
                    document[key] = document[key].replace(pattern2, "")
                    
            collection.update_one({"_id": document["_id"]}, {"$set": document})

    client.close()
        

def remove_CompleteTheLook(collection_name):
<<<<<<< HEAD
    db_uri = config.db_uri
    db_name = config_server.db_name
=======
    db_uri = f21_config.db_uri
    db_name = f21_config.db_name
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    pattern = r"Complete the look with \d+"

    # Iterate through the documents in the collection
    for document in collection.find():
        if isinstance(document, dict):
            for key in document:
                if isinstance(document[key], str):
                    document[key] = re.sub(pattern, '', document[key]).strip()
            collection.update_one({"_id": document["_id"]}, {"$set": document})

    client.close()

def reduce_image_width(collection_name):
<<<<<<< HEAD
    db_uri = config_server.db_uri
    db_name = config_server.db_name
=======
    db_uri = f21_config.db_uri
    db_name = f21_config.db_name
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Iterate through each item in the data
    for document in collection.find():
        if isinstance(document, dict) and "images" in document:
            updated_images = []
            for url in document['images']:
                if ".jpg?sw=" in url:
                    # Extract query parameters
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)

                    sw = int(query_params.get('sw', [0])[0])
                    sh = int(query_params.get('sh', [0])[0])

                    # Check if sw and sh meet the criteria
                    if sw <= 200 and sh <= 300:
                        updated_images.append(url)

            collection.update_one({'_id': document['_id']}, {'$set': {'images': updated_images}})
    client.close()

<<<<<<< HEAD
def add_incremental_id(collection_name, last_id=0):
    db_uri = config_server.db_uri
    db_name = config_server.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    current_id = last_id
    for document in collection.find():
        if isinstance(document, dict):
            current_id += 1
            hex_id = f"{current_id:06x}"  
            document['id'] = "#I"+hex_id

        collection.update_one({"_id": document["_id"]}, {"$set": document})

    client.close()
    return current_id

def load_lastID_from_db():
    db_uri = config_server.db_uri
    db_name = config.db_name
    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    variables_util = db["variables_util"]

    # Check if the collection exists
    if "variables_util" in db.list_collection_names():
        last_id_doc = variables_util.find_one({}, {'lastID': 1})
        if last_id_doc and 'lastID' in last_id_doc:
            return int(last_id_doc['lastID'])
        else:
            return 3
    else:
        return 3

def save_LastID(last_id):
    #last_id is in decimal
    db_uri = config_server.db_uri
    db_name = config_server.db_name
    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    variables_util = db["variables_util"]

    existing_id = load_lastID_from_db()

    # Check if the new last_id is greater than the existing one
    if last_id > existing_id:
        variables_util.update_one({}, {'$set': {'lastID': last_id}}, upsert=True)
    else:
        raise ValueError("New last_id must be greater than the existing last_id.")
    
=======
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

def post_process_json_files_in_folder(db_name, operations):
    """
    Performs given operations on collections in the specified database 
    where the collection name starts with 'data_'.

    :param db_name: Name of the MongoDB database.
    :param operations: A list of functions to be applied on each qualifying collection.
    """
<<<<<<< HEAD
    client = pymongo.MongoClient(config_server.db_uri)
=======
    client = pymongo.MongoClient(f21_config.db_uri)
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37
    db = client[db_name]
    for collection_name in db.list_collection_names():
        if collection_name.startswith(f21_config.collection_name_start_with):
            for operation in operations:
                if operation.__name__ == 'add_incremental_id':
                    last_id = operation(collection_name, last_id)
                else:
                    operation(collection_name)


operations = [reduce_image_width,remove_WashCold,remove_CompleteTheLook]
                    
<<<<<<< HEAD
post_process_json_files_in_folder(config_server.db_name, operations)
=======
post_process_json_files_in_folder(f21_config.db_name, operations)
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37
