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



script_dir = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'Reference6.json')
default_baseline_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'baseline_data6.json')


class MyApp(Flask):
    def __init__(self, import_name):
        super(MyApp, self).__init__(import_name)
        self.config['BASELINE_PATH'] = default_baseline_path
        self.baseline = read_json(self.config['BASELINE_PATH'])
        self.hashtable = divide_into_tiny_chunks(self.baseline)
        self.embedding = create_embedding(self.hashtable.keys())
        

app = MyApp(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    query = request.form['query']
    separated_user_input = separate_sentence(query)
    if(separated_user_input[0]!='' and separated_user_input[1]!=''):
        docs = get_similar_doc_from_embedding(app.embedding,query,k=10)
        docs2 = get_similar_doc_from_embedding(app.embedding,separated_user_input[1],k=10)
        docs.extend(docs2)
    else:
        docs = get_similar_doc_from_embedding(app.embedding,query,k=20) #get the best k docs
    print("docs : ")
    print(docs)
    set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs,app.hashtable)
    print("set_of_ids_GPT4 : ")
    print(set_of_ids_GPT4)
    correpsonding_items_gpt4 = filter_json_By_Id(app.config['BASELINE_PATH'],set_of_ids_GPT4)
    correpsonding_items_gpt3 = filter_json_By_Id(app.config['BASELINE_PATH'],set_of_ids_GPT3)
    gpt4_answer = get_chatgpt_response(correpsonding_items_gpt4, query, with_analysis=True)
    gpt3_answer = get_all_GPT3_response(correpsonding_items_gpt3, query, with_analysis=True)
    print("chat gpt4 answer : ")
    print(gpt4_answer)
    print("gpt3 ANSWER :")
    print(gpt3_answer)
    list_of_ids = extract_Ids_from_text(gpt4_answer)
    list_of_ids.extend(extract_Ids_from_text(gpt3_answer))
    print("list of ids = ")
    print(list_of_ids)
    output_json = filter_json_By_Id(reference_path,list_of_ids)
    return output_json

if __name__ == '__main__':
    app.run(debug=True)