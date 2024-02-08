import pymongo
import config_server

def inReference(reference_name, href_to_check):
    db_uri = config.db_uri
    db_name = config_server.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[reference_name]

    found = collection.find_one({"url": href_to_check})
    client.close()
    return bool(found)
