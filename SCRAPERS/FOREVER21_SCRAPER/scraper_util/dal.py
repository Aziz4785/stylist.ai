import pymongo
import config_server

<<<<<<< HEAD
def inReference(reference_name, href_to_check):
    db_uri = config_server.db_uri
    db_name = config_server.db_name
=======
def inReference(reference_name, id_to_check):
    db_uri = config.db_uri
    db_name = config.db_name
>>>>>>> 1675d6534603dcba84caa870be40482a1a54da37

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[reference_name]

    found = collection.find_one({"_id": id_to_check})
    client.close()
    return bool(found)
