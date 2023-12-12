from flask import Flask, request, jsonify , render_template
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import json
import re

from ServerUtil import *
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'Reference5.json')
default_baseline_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'baseline_data5.json')
app.config['BASELINE_PATH'] = default_baseline_path



baseline = read_json(app.config['BASELINE_PATH'])
hashtable = divide_into_tiny_chunks(baseline)
print("creating embedding ...")
embedding = create_embedding(hashtable.keys())
print("done")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    query = request.form['query']
    docs = get_similar_doc_from_embedding(embedding,query)
    print("docs : ")
    print(docs)
    set_of_ids = get_Ids_from_hashmap(docs,hashtable)
    print("set_of_ids : ")
    print(set_of_ids)
    correpsonding_items = filter_json_By_Id(app.config['BASELINE_PATH'],set_of_ids)
    correpsonding_items_string = convert_to_proper_string(correpsonding_items)
    gpt4_answer = get_chatgpt_response(correpsonding_items_string, query, with_analysis=False)
    print("chat gpt answer : ")
    print(gpt4_answer)
    list_of_ids = extract_Ids_from_text(gpt4_answer)
    output_json = filter_json_By_Id(reference_path,list_of_ids)
    return output_json

if __name__ == '__main__':
    app.run(debug=True)