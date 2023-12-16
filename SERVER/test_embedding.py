import unittest
from flask_testing import TestCase
from server3 import app  # Import your Flask app
import json
import sys
import os
from ServerUtil import *
script_dir = os.path.dirname(os.path.abspath(__file__))
"""
True Positive: The right clothes showing up when you search.
False Negative: The right clothes don't show up when they should.
False Positive: Clothes that you didn't want show up in your search.
True Negative: Clothes that you didn't want don't show up, which is good.


Our priority : minimize number of False negative  (hence the use of the recall metric)
the goal is to have  precision >0.8
"""
def compute_precision(actual_id_set,expected_id_set):
    # True Positives (TP): Items in the actual set that are also in the expected set
    tp = len(actual_id_set.intersection(expected_id_set))

    precision = 1
    # Calculate precision
    if(len(expected_id_set))>0:
        precision = tp / min(20,len(expected_id_set))
    return precision

def extract_id_from_response(data):
    ans = []
    for elem in data:
        ans.append(elem['id'])
    return ans

class MyTest(TestCase):
    test_results = []

    @classmethod
    def setUpClass(cls):
        cls.test_results = [] #init

    @classmethod
    def tearDownClass(cls):
        # Save the report to a file after all tests in the class

        total_precision = sum(result['precision'] for result in cls.test_results)
        average_precision = total_precision / len(cls.test_results) if cls.test_results else 0

        report_data = {
            "average_precision": average_precision,
            "test_results": cls.test_results
        }
        with open('test_embedding_report.json', 'w') as file:
            json.dump(report_data, file, indent=4)

    def create_app(self):
        app.config['TESTING'] = True
        return app
    

    def load_expected_json(self):
        with open('expected_output.json') as file:
            return json.load(file)
    
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_process_content1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "a garment with a cute drawing on it"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I000109"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_color1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "shoes that are white and black and (another color)"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I00005c","#I000058","#I00005f","#I000061","#I00006b",
                        "#I00006c","#I000072","#I00007c","#I000082","#I00008c","#I00008e"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("test_process_color1")
        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)

        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_color2(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "green and white shoes"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I000016","#I000063","#I000086","#I00008d"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)
        print("test_process_color2")
        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })
    
    def test_process_design1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "a shirt with a red thing on the back"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I000267"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_content3(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "an item with the christian cross on it"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I0000a9"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_design2(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "a looonng skirt"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I000169"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_comp1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "something made of cotton and polyester only"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I000092","#I0000e3","#I0000ed","#I0000f0","#I0000fd",
                        "#I000106","#I0000d8","#I0000d4","#I0000c4","#I000240",
                        "#I00025a","#I000242","#I0000b1","#I0000c2","#I000097",
                        "#I000141","#I0000ab"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_sameStyle1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data6" #does not work
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "something similar to Arsene wenger's coat"
   
        docs = get_similar_doc_from_embedding(app.embedding,user_input,k=20) #get the best k docs
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, app.hashtable)
        expected_ids = ["#I00014b"]
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        print("actual ids : ")
        print(actual_ids)
        print("expected ids :")
        print(expected_ids)
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": baseline_used
        })