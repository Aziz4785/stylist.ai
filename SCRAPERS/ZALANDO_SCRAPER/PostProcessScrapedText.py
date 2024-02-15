import re
import pymongo
import config_zalando

def remove_SeeEnvironementSpec(collection_name):
    db_uri = config_zalando.db_uri
    db_name = config_zalando.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    pattern = "See environmental specifications"

    # Iterate through the documents in the collection
    for document in collection.find():
        if isinstance(document, dict):
            for key in document:
                if isinstance(document[key], str):
                    document[key] = document[key].replace(pattern, "")

            collection.update_one({"_id": document["_id"]}, {"$set": document})

    client.close()
        
def reduce_image_width(collection_name):
<<<<<<< HEAD
    db_uri = config_server.db_uri
    db_name = config.db_name
=======
    db_uri = config_zalando.db_uri
    db_name = config_zalando.db_name
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Iterate through each item in the data
    for document in collection.find():
        if isinstance(document, dict):
            # Iterate through each image URL in the 'images' array
            if "images" in document:
                for i, url in enumerate(document['images']):
                    # Find and replace 'imwidth' value if greater than 200
                    if "imwidth=" in url and int(url.split("imwidth=")[1].split("&")[0]) > 200:
                        # Split the URL at 'imwidth=' and then at '&' to isolate the value
                        parts = url.split("imwidth=")
                        subparts = parts[1].split("&", 1)
                        # Replace the value with 156
                        subparts[0] = "156"
                        # Reconstruct the URL
                        document['images'][i] = parts[0] + "imwidth=" + "&".join(subparts)

            collection.update_one({"_id": document["_id"]}, {"$set": document})
    client.close()

def add_gender_to_collection(collection_name):
    db_uri = config_zalando.db_uri
    db_name = config_zalando.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Determine the gender based on the collection name
    if "femme" in collection_name:
        gender_value = "women"
    elif "homme" in collection_name:
        gender_value = "men"
    else:
        gender_value = "unknown"

    for document in collection.find():
        if isinstance(document, dict):
            document['gender'] = gender_value
            collection.update_one({"_id": document["_id"]}, {"$set": document})

    client.close()

def remove_reference(collection_name):
    # Regular expression pattern to match "Reference: " followed by any characters
    # stopping at a space, comma, point, or the end of the string
    pattern = r"Reference: [^ ,.]*[ ,.]?"

<<<<<<< HEAD
    db_uri = config_server.db_uri
    db_name = config.db_name
=======
    db_uri = config_zalando.db_uri
    db_name = config_zalando.db_name
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]


    # Iterate through the documents in the collection
    for document in collection.find():
        if isinstance(document, dict):
            for key in document:
                if isinstance(document[key], str):
                    document[key] = re.sub(pattern, "", document[key])

            collection.update_one({"_id": document["_id"]}, {"$set": document})

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
    client = pymongo.MongoClient(config_zalando.db_uri)
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37
    db = client[db_name]
    last_id = 3  # Starting ID in decimal
    for collection_name in db.list_collection_names():
        if collection_name.startswith(config_zalando.collection_name_start_with):
            for operation in operations:
                if operation.__name__ == 'add_incremental_id':
                    last_id = operation(collection_name, last_id)
                else:
                    operation(collection_name)

operations = [remove_reference, remove_SeeEnvironementSpec,reduce_image_width]
                    
post_process_json_files_in_folder(config_zalando.db_name, operations)