import unittest
from flask_testing import TestCase
from server3 import app  # Import your Flask app
import json
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
"""
True Positive: The right clothes showing up when you search.
False Negative: The right clothes don't show up when they should.
False Positive: Clothes that you didn't want show up in your search.
True Negative: Clothes that you didn't want don't show up, which is good.


Our priority : minimize number of False negative  (hence the use of the recall metric)
the goal is to have recall >0.7 and precision >0.7
"""
def compute_recall(actual_id_set,expected_id_set):
    # True Positives (TP): Items in the actual set that are also in the expected set
    tp = len(actual_id_set.intersection(expected_id_set))

    # False Negatives (FN): Items in the expected set but not in the actual set
    fn = len(expected_id_set - actual_id_set)

    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    return recall

def compute_precision(actual_id_set,expected_id_set):
    # True Positives (TP): Items in the actual set that are also in the expected set
    tp = len(actual_id_set.intersection(expected_id_set))

    # False Positives (FP): Items in the actual set but not in the expected set
    fp = len(actual_id_set - expected_id_set)

    # Calculate precision
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
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

        total_recall = sum(result['recall'] for result in cls.test_results)
        total_precision = sum(result['precision'] for result in cls.test_results)
        average_recall = total_recall / len(cls.test_results) if cls.test_results else 0
        average_precision = total_precision / len(cls.test_results) if cls.test_results else 0


        description = {
            "1": "True Positive: The right clothes showing up when you search.",                     
            "2": "False Negative: The right clothes don't show up when they should.",
            "3": "False Positive: Clothes that you didn't want show up in your search.",
            "4": "True Negative: Clothes that you didn't want don't show up, which is good.",
            "5": "Our priority : minimize number of False negative  (hence the use of the recall metric)",
            "6": "the goal is to have recall >0.7 and precision >0.7"
                            
        }

        report_data = {
            "header": description,
            "average_recall": average_recall,
            "average_precision": average_precision,
            "test_results": cls.test_results
        }
        with open('test_report.json', 'w') as file:
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

    def test_process_color1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "blue and white shoes"
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)
    
        ref_file = "Reference5.json"

        expected_ids = ["#I00001c","#I000076","#I00003f"]
        response_data = json.loads(response.data.decode('utf-8'))
        actual_ids = extract_id_from_response(response_data)

        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })
        #self.assertEqual(output_json, expected_json)

    def test_process_comp1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = 'something made of 100% polyester'
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        ref_file = "Reference5.json"

        expected_ids = ["#I0002f8","#I00004d","#I000026","#I00000e","#I000646",
                        "#I0003ef","#I0003d8","#I0003d4","#I00034a","#I000344","#I000341","#I00033d",
                        "#I000338","#I00032b","#I00032a","#I000328","#I000325","#I000349","#I000324","#I00031e",
                        "#I00031b","#I000315","#I00030f","#I000302","#I000300","#I0002f8"]
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)

        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_content1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = 'a hoodie with something written on the sleeve'
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        ref_file = "Reference5.json"

        expected_ids = ["#I0003df"]# smth written on the sleeve but not hoodie : #I0003d9 #I0003b7 #I0003a3
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)
    
        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_design1(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = 'a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater'
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        expected_ids = ["#I0003a3","#I0003e6"]
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)
    
        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_design2(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = """'I want to buy women's boots that are "covered"""""  #true name is padlock boots
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        expected_ids = ["#I000016","#I00001e","#I000056"]
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)
    
        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_design3(self):
        #same as test_process_design2 but more detailled
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = """boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year"""  #true name is padlock boots
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        expected_ids = ["#I000016"]
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)
    
        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })

    def test_process_content2(self):
        app.config['TESTING'] = True
        baseline_used="baseline_data5"
        app.config['BASELINE_PATH'] = os.path.join(script_dir, '..',  'MAIN_DATA', f'{baseline_used}.json')

        user_input = "an item where the logo of the brand is printed/visible more than one time"  
        test_query = {'query': user_input}
        response = self.client.post('/process', data=test_query)
        self.assertEqual(response.status_code, 200)

        expected_ids = ["#I0003b2"]
        response_data = json.loads(response.data.decode('utf-8'))

        actual_ids = extract_id_from_response(response_data)
    
        recall = compute_recall(set(actual_ids),set(expected_ids))
        precision = compute_precision(set(actual_ids),set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "recall": recall,
            "precision": precision,
            "baseline_used": baseline_used
        })







