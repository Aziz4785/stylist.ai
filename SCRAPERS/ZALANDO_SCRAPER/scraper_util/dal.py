import pymongo
import config

def inReference(reference_name, id_to_check):
    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[reference_name]

    found = collection.find_one({"_id": id_to_check})
    client.close()
    return bool(found)

