from ServerUtil import *
import pickle

from itertools import islice





db_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(db_uri)
db_name = config_server.db_name
db = client[db_name]
catalogue = db["Catalogue1"]

def divide_into_tiny_chunks(catalogue):
    print("dividing catalogue into tiny chunks  ...")
    hashtable={}
    for item in catalogue.find():
        brand= ""
        name= ""
        details= ""
        sentences= []
        if("visual description" in item):
            sentences = extract_sentences(item["visual description"])
            description_without_newlines = replace_double_newlines(item["visual description"])
            if(description_without_newlines not in hashtable):
                hashtable[description_without_newlines] = set()
            hashtable[description_without_newlines].add(item["_id"])

        if("brand" in  item):
            brand = item["brand"]
        if("name of the product" in item):
            name = item["name of the product"]+", "
        if("details about that item" in item):
            details = item["details about that item"]
            if details not in hashtable:
                hashtable[details] = set()
            hashtable[details].add(item["_id"])
        if("materials" in item):
            materials = item["materials"]
            if materials not in hashtable:
                hashtable[materials] = set()
            hashtable[materials].add(item["_id"])

        name_key = name +" "+brand
        if name_key not in hashtable:
            hashtable[name_key] = set()
        if brand not in hashtable:
            hashtable[brand] = set()

        hashtable[name_key].add(item["_id"])
        hashtable[brand].add(item["_id"])

        for sentence in sentences:
            if(sentence not in hashtable):
                hashtable[sentence] = set()
            hashtable[sentence].add(item["_id"])
           

        
    print("done")
    return hashtable

def create_and_save_hashtable(catalogue_name,filename):
    db_name = config_server.db_name
    db = client[db_name]
    catalogue = db[catalogue_name]
    print("creating the hashtable...")
    hashtable = divide_into_tiny_chunks(catalogue)
    with open(filename, 'wb') as file:
        pickle.dump(hashtable, file)
    return hashtable


# Function to create and save embeddings
def create_and_save_embeddings(documents, file_name="faiss_embedding"):
    if not documents:
        return None
    if(documents is None or len(documents)==0):
        return None
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(documents, embeddings)
    vector_store.save_local(file_name)
    print("Embeddings created and saved.")

hashtable = create_and_save_hashtable("Catalogue1","hashtable")
print("hashtable created successfully : length of hashtable: "+str(len(hashtable)))
first_three = islice(hashtable.items(), 3)
# Printing the first three elements
for key, value in first_three:
    print(f"{key}: {value}")
create_and_save_embeddings(hashtable.keys())