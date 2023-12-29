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
        with open('test_embedding_bl7_report.json', 'w') as file:
            json.dump(report_data, file, indent=4)

    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        self.app = self.create_app()
        self.baseline_used = "baseline_data7"
        self.app.config['BASELINE_PATH'] = os.path.join(script_dir, '..', 'MAIN_DATA', f'{self.baseline_used}.json')

    def load_expected_json(self):
        with open('expected_output.json') as file:
            return json.load(file)
    
    def run_test_case(self, user_input, expected_ids):
        docs = get_similar_doc_for_separated_input(self.app.embedding, user_input)
        set_of_ids_GPT4, set_of_ids_GPT3 = get_Ids_from_hashmap(docs, self.app.hashtable)
        actual_ids = set_of_ids_GPT4.union(set_of_ids_GPT3)

        precision = compute_precision(set(actual_ids), set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": self.baseline_used
        })

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_1(self):
        user_input = "example of query"
        expected_ids = ["#I000109","example id 1","example id2 ",...]
        self.run_test_case(user_input, expected_ids)
