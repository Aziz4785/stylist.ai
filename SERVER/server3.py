from flask import Flask, request, jsonify , render_template, session
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
        print("List of databases:", client.list_database_names())
        db = client[db_name]
        self.search_counts_collection = db['search_counts']
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
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
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
    ip_address = request.remote_addr  # Get the IP address of the user
    max_searches_per_day = 100  # Set the max number of searches allowed per day

    # Find the document for the current user's IP address
    search_count = app.search_counts_collection.find_one({'ip': ip_address})

    if search_count:
        # If a document exists, calculate the remaining searches
        searches_left = max_searches_per_day - search_count.get('count', 0)
    else:
        # If no document exists for the IP, the user has all their searches left
        searches_left = max_searches_per_day

    # Render the template with the number of searches left
    return render_template('index.html', searches_left=searches_left)


@app.route('/process', methods=['POST'])
@limiter.limit("100 per day")
def process():
    print("we call /process ...")

    user_input = request.form['query']
    user_input = sanitize_input(user_input)

    if not_valid(user_input):
        return "input not valid"

    # actual_ids = get_Ids_of_similiar_docs_from_emebdding(app,user_input)

    """ set_of_ids_GPT4, set_of_ids_GPT3 = set(actual_ids[:10]),set(actual_ids[10:])
    correpsonding_items_gpt4 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT4)
    correpsonding_items_gpt3 = filter_collection_By_Id(app.config['catalogue_collection_name'],set_of_ids_GPT3)
    print(str(len(correpsonding_items_gpt4))+" items for gpt4 and "+str(len(correpsonding_items_gpt3))+" items for gpt3")
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
    final_documents = filter_collection_By_Id("reference8",list_of_ids) """
    final_documents = {"hello":"world"}
    json_output = json.dumps(final_documents, cls=MongoJsonEncoder)
    ip_address = request.remote_addr  # Get user's IP address
    search_count = app.search_counts_collection.find_one({'ip': ip_address})

    if search_count is None:
        # If this IP is making its first search, create a new document for it.
        new_count = 100
        app.search_counts_collection.insert_one({'ip': ip_address, 'count': 1})
        searches_left = 99
    else:
        # Increment the search count and update the document.
        new_count = search_count['count'] + 1
        app.search_counts_collection.update_one({'ip': ip_address}, {'$set': {'count': new_count}})
        searches_left = 100 - new_count

    # Limit searches to 100 per IP per day
    if new_count > 100:
        return jsonify({'error': 'Search limit reached'}), 429
    return jsonify({'result': final_documents, 'searches_left': searches_left})

