from flask import Flask, request, jsonify , render_template
import os
import sys
import json
from bson import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from werkzeug.middleware.proxy_fix import ProxyFix
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
        logging.info("List of databases:", client.list_database_names())
        db = client[db_name]
        super(MyApp, self).__init__(import_name)
        self.config["RATELIMIT_HEADERS_ENABLED"] = True #https://flask-limiter.readthedocs.io/en/stable/configuration.html
        if(config_server.catalogue_name in db.list_collection_names()):
            self.catalogue = db[config_server.catalogue_name]
            self.hashtable = load_hashtable("hashtable")
            self.embedding = load_embeddings()
            #self.embedding_of_small_chunks = create_embedding(self.hashtable_small_chunks.keys())

app = MyApp(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_key_for_csrf",
)
csrf = CSRFProtect(app) 
app.wsgi_app = ProxyFix( 
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
) #https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
limiter = Limiter(app=app, key_func=lambda: request.headers.get('X-Real-IP') or get_remote_address())

@app.after_request
def apply_csp(response):
    #https://flask.palletsprojects.com/en/2.3.x/security/#security-csp 
    #response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' www.askstyler.com;" #Tell the browser where it can load various types of resource from.
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #Tells the browser to convert all HTTP requests to HTTPS, preventing man-in-the-middle (MITM) attacks.
    response.headers['X-Content-Type-Options'] = 'nosniff'
    #response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
@limiter.limit("3 per day")
def process():
    try:
        logging.info("we call /process ...")
        user_input = request.form['query']
        user_input = sanitize_input(user_input)
        user_input = preprocess_input(user_input)
        if not_valid(user_input):
            return jsonify({"error": "input not valid"}), 400  # Return JSON response with HTTP 400 status

        save_query(user_input)
        actual_ids = get_Ids_of_similiar_docs_from_emebdding(app,user_input)
        logging.info("ids from embedding : ")
        logging.info(actual_ids)
        logging.info(" ")
        set_of_ids_GPT4, set_of_ids_GPT3 = set(actual_ids[:15]),set(actual_ids[15:35])

        id_index_map_gpt4 = set_to_hashmap(set_of_ids_GPT4) #key is an id of catalogue and value is a formatted index for example : #I0046
        id_index_map_gpt3 = set_to_hashmap(set_of_ids_GPT3)
        index_id_map_GPT4 = invert_dict(id_index_map_gpt4)
        index_id_map_GPT3 = invert_dict(id_index_map_gpt3)

        logging.info("id index for gpt4 :")
        logging.info(id_index_map_gpt4)

        logging.info("id index for gpt3 :")
        logging.info(id_index_map_gpt3)

        correpsonding_items_gpt4 = filter_collection_By_Id(config_server.catalogue_name,set_of_ids_GPT4)
        correpsonding_items_gpt3 = filter_collection_By_Id(config_server.catalogue_name,set_of_ids_GPT3)
        logging.info(str(len(correpsonding_items_gpt4))+" items for gpt4 and "+str(len(correpsonding_items_gpt3))+" items for gpt3")
        gpt4_answer = get_all_GPT4_response(correpsonding_items_gpt4, user_input, id_index_map_gpt4, with_analysis=True)
        gpt3_answer = get_all_GPT3_response(correpsonding_items_gpt3, user_input, id_index_map_gpt3, with_analysis=True)
        
        logging.info("chat gpt4 answer : ")
        logging.info(gpt4_answer)
        logging.info("gpt3 ANSWER :")
        logging.info(gpt3_answer)
        list_of_ids = convert_to_catalgoue_ids(extract_small_Ids_from_text(gpt4_answer),index_id_map_GPT4)
        list_of_ids.extend(convert_to_catalgoue_ids(extract_small_Ids_from_text(gpt3_answer),index_id_map_GPT3))
        logging.info("list of ids = ")
        logging.info(list_of_ids)
        final_documents = filter_collection_By_Id(config_server.reference_name,list_of_ids)
        json_output = json.dumps(final_documents, cls=MongoJsonEncoder)
        return json_output
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.info("error occured ..")
        return jsonify({"error": "An unexpected error occurred"}), 500
