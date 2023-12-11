import unittest
from flask_testing import TestCase
from server3 import app  # Import your Flask app
import json
import sys

def extract_id_from_response(data):
    print("data :")
    print(data)
    ans = []
    for elem in data:
        ans.append(elem['id'])
    return ans

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def load_expected_json(self):
        with open('expected_output.json') as file:
            return json.load(file)
    
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_process_color1(self):
        test_query = {'query': 'blue and white shoes'}
        response = self.client.post('/process', data=test_query)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        baseline_file = "baseline_data5.json"
        ref_file = "Reference5.json"

        expected_ids = ["#I00001c","#I000076","#I00003f"]
        print("actual ids : ")
        actual_ids = extract_id_from_response(response.data)
        print(actual_ids)
        #self.assertEqual(output_json, expected_json)
