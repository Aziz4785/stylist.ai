import unittest
from flask_testing import TestCase
import sys
import os

server_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(server_directory)

from server3 import app  
import json
import common_variables

from META.metadata_card import *
from META.metadata_matching_controller import *
from META.metadata_extraction import *
from META.metadata_matching import *

from ServerUtil import *

# run docker exec -it d2d67708437c python -m unittest /server/tests/test_embedding_catalog1.py  OR  docker-compose run (ou exec jsp plus) server python -m unittest tests/test_embedding_catalog1.py

def compute_precision(actual_id_set,expected_id_set):
    # True Positives (TP): Items in the actual set that are also in the expected set
    tp = len(actual_id_set.intersection(expected_id_set))

    precision = 1
    # Calculate precision
    if(len(expected_id_set))>0 and len(actual_id_set)>0:
        precision = tp / min(len(actual_id_set),len(expected_id_set))
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

        total_precision_simple = sum(result['precision'] for result in cls.test_results if result['query_formulation'] == "simple")
        count_simple_results = sum(1 for result in cls.test_results if result['query_formulation'] == "simple")
        average_precision_simple = total_precision_simple / count_simple_results if count_simple_results else 0

        report_data = {
            "average_precision": average_precision,
            "average_precision (simple queries)": average_precision_simple,
            "test_results": cls.test_results
        }
        with open('tests/test_embedding_catalog1_report.json', 'w', encoding='utf-8') as file:
            json.dump(report_data, file, indent=4, ensure_ascii=False)

    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        self.app = self.create_app()
        self.catalog_used = "catalogue1"

    def run_test_case(self, user_input, expected_ids,query_formulation="other"):
        print()
        print()
        print()
        print()
        print()
        print()
        print("user input : "+user_input)

        # Step 2: Create a MetaDataCard with these extractors
        extractors = {
            "type": TypeExtractor(),
            "composition": CompositionExtractor(),
            "blackwhite": BlackWhiteExtractor(),
            "otherColor": OtherColorExtractor(),
            "genre": GenreExtractor()
        }
        matchers = {
            "type": TypeMatcher(),
            "composition": CompositionMatcher(),
            "blackwhite": BlackWhiteMatcher(),
            "otherColor": OtherColorMatcher(),
            "genre": GenreMatcher()
        }
        matching_controller = MetadataMatchingController(matchers)

        metadata_card = MetaDataCard(extractors)
        metadata_card.generate_from_query(user_input)
        print("metadata of the user input : ")
        print(metadata_card)

        meta_filtered_docs=[]
        k=60
        while(len(meta_filtered_docs)<20 and k<1000):
            separated_user_input=['','']
            docs_with_score = get_similar_doc_for_separated_input(self.app,self.app.embedding, user_input,separated_user_input,k=k)
            meta_filtered_docs = filter_docs(self.app,docs_with_score,metadata_card,matching_controller)
            print("first 5 docs after meta filtering : ")
            #meta_filtered_docs is a list of (doc,score)
            print(meta_filtered_docs[:5])
            k*=2
        
        actual_ids_pairs = get_topK_uniqueIds_from_docs(app.hashtable,meta_filtered_docs,k=24)
        #each elem of actual_ids_pairs looks like this :('#I00026b', 0.39710677)
        print(" the returned ids from get_topK_uniqueIds_from_docs : ")
        actual_ids= [pair[0] for pair in actual_ids_pairs]
        print(actual_ids)

        precision = compute_precision(set(actual_ids), set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "catalogue_used": self.catalog_used,
            "query_formulation": query_formulation
        })


    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_1(self):
        user_input = "a blue shirt"
        expected_ids = ["#I000257","#I00025d","#I000276","#I000237","#I0001f8"]
        self.run_test_case(user_input, expected_ids, "simple")
