from flask import Flask, request, jsonify , render_template
import os
import sys
import json
from bson import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_wtf.csrf import CSRFProtect
from ServerUtil import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import config_server
from security_util import *
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
        self.config["RATELIMIT_HEADERS_ENABLED"] = True #https://flask-limiter.readthedocs.io/en/stable/configuration.html
        if(self.config['catalogue_collection_name'] in db.list_collection_names()):
            self.catalogue = db[self.config['catalogue_collection_name']]
            self.hashtable = divide_into_tiny_chunks(self)
            #self.hashtable_small_chunks = divide_description_into_smaller_chunks(self)
            self.embedding = create_embedding(self.hashtable.keys())
            #self.embedding_of_small_chunks = create_embedding(self.hashtable_small_chunks.keys())

app = MyApp(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_key_for_csrf",
)
csrf = CSRFProtect(app) 
limiter = Limiter(app=app, key_func=lambda: request.headers.get('X-Real-IP') or get_remote_address())

@app.after_request
def apply_csp(response):
    #https://flask.palletsprojects.com/en/2.3.x/security/#security-csp 
    #response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' www.askstyler.com;" #Tell the browser where it can load various types of resource from.
    #response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #Tells the browser to convert all HTTP requests to HTTPS, preventing man-in-the-middle (MITM) attacks.
    response.headers['X-Content-Type-Options'] = 'nosniff'
    #response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
@limiter.limit("3 per day")
def process():
    print("we call /process ...")

    user_input = request.form['query']
    user_input = sanitize_input(user_input)

    if not_valid(user_input):
        return "input not valid"

    actual_ids = get_Ids_of_similiar_docs_from_emebdding(app,user_input)

    set_of_ids_GPT4, set_of_ids_GPT3 = set(actual_ids[:10]),set(actual_ids[10:])
    correpsonding_items_gpt4 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT4)
    correpsonding_items_gpt3 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT3)
    print("corredponsing items for gpt4 : ")
    print(correpsonding_items_gpt4)
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
    final_documents = filter_collection_By_Id("reference8",list_of_ids)
    json_output = json.dumps(final_documents, cls=MongoJsonEncoder)
    return json_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #tells Flask to listen on all network interfaces within the container, making it accessible through the Docker host