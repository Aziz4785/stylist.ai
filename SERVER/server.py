from flask import Flask, request, jsonify , render_template
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from langchain.chains.question_answering import load_qa_chain
import json
import re
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ServerUtil import *
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY



app = Flask(__name__)
baseline = read_json("baseline_data4.json")
print(" baseline object created")
docsearch = create_embedding(baseline)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    query = request.form['query']
    print(" embedding created")
    results = ask_embedding_qa_langchain(docsearch,query)
    list_of_ids = extract_Ids(results)
    print(list_of_ids)
    mock_json = mock_process(list_of_ids)
    return mock_json

if __name__ == '__main__':
    app.run(debug=True)