import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

# In MongoDB, a database is not created until it gets content!

mycollection = mydb["customers"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycollection.insert_one(mydict)
print(x.inserted_id)


mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

x = mycollection.insert_many(mylist)

mylist = [
  { "_id": 1, "name": "JohAn", "address": "Highway 37"},
  { "_id": 2, "name": "PeteAr", "address": "Lowstreet 27"},
  { "_id": 3, "name": "AmyA", "address": "Apple st 652"},
  { "_id": 4, "name": "HanAnah", "address": "Mountain 21"},
  { "_id": 5, "name": "MichAael", "address": "Valley 345"},
  { "_id": 6, "name": "SaAndy", "address": "Ocean blvd 2"},
  { "_id": 7, "name": "BeAtty", "address": "Green Grass 1"},
  { "_id": 8, "name": "RicAhard", "address": "Sky st 331"},
  { "_id": 9, "name": "SusAan", "address": "One way 98"},
  { "_id": 10, "name": "VicAky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "BeAn", "address": "Park Lane 38"},
  { "_id": 12, "name": "WilAliam", "address": "Central st 954"},
  { "_id": 13, "name": "ChAuck", "address": "Main Road 989"},
  { "_id": 14, "name": "ViAola", "address": "Sideway 1633"}
]

x = mycollection.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(x.inserted_ids)
#print list of the _id values of the inserted documents:
print(x.inserted_ids)
print(myclient.list_database_names())
print(mydb.list_collection_names())