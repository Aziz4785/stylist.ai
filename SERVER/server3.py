from flask import Flask, request, jsonify , render_template
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
import sys
import SERVER.common_variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import json
import re

from SERVER.ServerUtil import *
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY



script_dir = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'Reference7.json')
default_baseline_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'baseline_data7.json')


class MyApp(Flask):
    
    def __init__(self, import_name):
        super(MyApp, self).__init__(import_name)
        self.config['BASELINE_PATH'] = default_baseline_path
        self.baseline = read_json(self.config['BASELINE_PATH'])
        self.hashtable = divide_into_tiny_chunks(self,self.baseline)
        self.hashtable_small_chunks = divide_description_into_smaller_chunks(self.baseline)
        self.embedding = create_embedding(self.hashtable.keys())
        self.embedding_of_small_chunks = create_embedding(self.hashtable_small_chunks.keys())

app = MyApp(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    type_extractor = TypeExtractor()
    composition_extractor = CompositionExtractor()
    bw_extractor = BlackWhiteExtractor()
    otherColor_extrator =OtherColorExtractor()
    genre_extractor = GenreExtractor()

    type_matcher = TypeMatcher()
    composition_matcher = CompositionMatcher()
    bw_matcher = BlackWhiteMatcher()
    otherColor_matcher = OtherColorMatcher()
    genre_matcher= GenreMatcher()
    
    extractors = {
        "type": type_extractor,
        "composition": composition_extractor,
        "blackwhite": bw_extractor,
        "otherColor": otherColor_extrator,
        "genre": genre_extractor
    }
    matchers = {
        "type": type_matcher,
        "composition": composition_matcher,
        "blackwhite": bw_matcher,
        "otherColor": otherColor_matcher,
        "genre": genre_matcher
    }
    matching_controller = MetadataMatchingController(matchers)
    
    metadata_card = MetaDataCard(extractors)

    user_input = request.form['query']

    metadata_card.generate_from_query(user_input)
    print("metadata of the user input : ")
    print(metadata_card)
    separated_user_input = separate_sentence(user_input)
    feature_words = extract_feature_words_from_query(user_input).split(',')
    most_important_word = feature_words[0]
    if(len(feature_words)>1 and most_important_word.lower() in {"white","black","men","women","for men","for women"} ):
        most_important_word = feature_words[1]

    meta_filtered_docs=[]
    k=60
    while(len(meta_filtered_docs)<20 and k<1000):
        docs_similar_to_feature_words = get_similar_docs_from_small_embedding(self.app,most_important_word)
        separated_user_input=['','']
        docs_with_score = get_similar_doc_for_separated_input(self.app,self.app.embedding, user_input,separated_user_input,k=k)
        meta_filtered_docs = filter_docs(self.app,docs_with_score,metadata_card,matching_controller)
        meta_filtered_feature_words_docs = filter_docs(self.app,docs_similar_to_feature_words,metadata_card,matching_controller)
        print("first 5 docs after meta filtering : ")
        #meta_filtered_docs is a list of (doc,score)
        print(meta_filtered_docs[:5])
        print("best 40 docs similar to feature words : ")
        print(meta_filtered_feature_words_docs[:40])
        k*=2

    actual_ids_pairs = get_topK_uniqueIds_from_docs(app.hashtable,meta_filtered_docs,k=24)
    actual_ids= [pair[0] for pair in actual_ids_pairs]

    

    set_of_ids_GPT4, set_of_ids_GPT3 = set(actual_ids[:10]),set(actual_ids[10:])
    correpsonding_items_gpt4 = filter_json_By_Id(app.config['BASELINE_PATH'],set_of_ids_GPT4)
    correpsonding_items_gpt3 = filter_json_By_Id(app.config['BASELINE_PATH'],set_of_ids_GPT3)

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
    output_json = filter_json_By_Id(reference_path,list_of_ids)
    return output_json

if __name__ == '__main__':
    app.run(debug=True)