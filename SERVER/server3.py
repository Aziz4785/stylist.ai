from flask import Flask, request, jsonify , render_template
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from META.metadata_card import *
from META.metadata_matching_controller import *
from META.metadata_extraction import *
from META.metadata_matching import *

from ServerUtil import *
import config_server

os.environ["OPENAI_API_KEY"] = config_server.OPENAI_API_KEY


class MyApp(Flask):
    
    def __init__(self, import_name):
        db_uri = config_server.db_uri
        db_name = config_server.db_name
        client = pymongo.MongoClient(db_uri)
        print("List of databases:", client.list_database_names())
        db = client[db_name]
        super(MyApp, self).__init__(import_name)
        self.config['catalogue_collection_name'] = "Catalogue1"
        if(self.config['catalogue_collection_name'] in db.list_collection_names()):
            self.catalogue = db[self.config['catalogue_collection_name']]
            self.hashtable = divide_into_tiny_chunks(self)
            #self.hashtable_small_chunks = divide_description_into_smaller_chunks(self)
            self.embedding = create_embedding(self.hashtable.keys())
            #self.embedding_of_small_chunks = create_embedding(self.hashtable_small_chunks.keys())

app = MyApp(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    extractors = {
            "type": TypeExtractor(),
            "composition": CompositionExtractor(),
            "blackwhite": BlackWhiteExtractor(),
            "otherColor": OtherColorExtractor(),
            "gender": GenderExtractor()
        }
    matchers = {
        "type": TypeMatcher(),
        "composition": CompositionMatcher(),
        "blackwhite": BlackWhiteMatcher(),
        "otherColor": OtherColorMatcher(),
        "gender": GenderMatcher()
    }
    matching_controller = MetadataMatchingController(matchers)

    metadata_card = MetaDataCard(extractors)

    user_input = request.form['query']

    metadata_card.generate_from_query(user_input)
    print("metadata of the user input : ")
    print(metadata_card)
    separated_user_input = separate_sentence(user_input)
    meta_filtered_docs=[]
    k=60
    while(len(meta_filtered_docs)<20 and k<1000):
        separated_user_input=['','']
        docs_with_score = get_similar_doc_for_separated_input(app,app.embedding, user_input,separated_user_input,k=k)
        meta_filtered_docs = filter_docs(app,docs_with_score,metadata_card,matching_controller)
        print("first 5 docs after meta filtering : ")
        #meta_filtered_docs is a list of (doc,score)
        print(meta_filtered_docs[:5])
        k*=2

    actual_ids_pairs = get_topK_uniqueIds_from_docs(app.hashtable,meta_filtered_docs,k=30)
    actual_ids= [pair[0] for pair in actual_ids_pairs]

    

    set_of_ids_GPT4, set_of_ids_GPT3 = set(actual_ids[:10]),set(actual_ids[10:])
    correpsonding_items_gpt4 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT4)
    correpsonding_items_gpt3 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT3)

    gpt4_answer = get_chatgpt_response(correpsonding_items_gpt4, user_input, with_analysis=True)
    gpt3_answer = get_all_GPT3_response(correpsonding_items_gpt3, user_input, with_analysis=True)
    print("chat gpt4 answer : ")
    print(gpt4_answer)
    print("gpt3 ANSWER :")
    print(gpt3_answer)
    list_of_ids = extract_Ids_from_text(gpt4_answer)
    list_of_ids.extend(extract_Ids_from_text(gpt3_answer))
    print("list of ids = ")
    print(list_of_ids)
    output_json = filter_collection_By_Id("reference8",list_of_ids)
    return output_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #tells Flask to listen on all network interfaces within the container, making it accessible through the Docker host