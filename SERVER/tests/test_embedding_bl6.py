import unittest
from flask_testing import TestCase
from server3 import app  # Import your Flask app
import json
import sys
import os
from SERVER.META.metadata_card import *
from ServerUtil import *
from META.metadata_card import *
from META.metadata_matching_controller import *
from META.metadata_extraction import *
from META.metadata_matching import *
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
        with open('test_embedding_bl6_report.json', 'w') as file:
            json.dump(report_data, file, indent=4)

    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        self.app = self.create_app()
        self.baseline_used = "baseline_data6"
        self.app.config['BASELINE_PATH'] = os.path.join(script_dir, '..', 'MAIN_DATA', f'{self.baseline_used}.json')

    def load_expected_json(self):
        with open('expected_output.json') as file:
            return json.load(file)
    
    # def run_test_case(self, user_input, expected_ids):
    #     print()
    #     print()
    #     print()
    #     print("user input : "+user_input)
    #     input_type = classify_garment_type(user_input) #input_type could be for example "Tops" , or "Bottom" or "unknown" etc..
    #     print("this input type is : ")
    #     print(input_type)
    #     correpsonding_embedding = app.get_corresponding_embedding(input_type)
    #     separated_user_input = separate_sentence(user_input)
    #     list_of_docList = get_similar_doc_for_separated_input(self.app,correpsonding_embedding, user_input,separated_user_input)
    #     #first doclist is for gpt4 and the rest for gpt3
    #     size_of_sets=[9,11]
    #     #if(separated_user_input[0] != "" and is_single_word(separated_user_input[0])):
    #         #size_of_sets=[5,15]
    #     if(len(list_of_docList)==1):
    #         size_of_sets=[20]
    #     set_list = get_Ids_from_hashmap(list_of_docList, self.app.hashtable,size_of_sets)
    #     print(" the returned list of set from get_Ids_from_hashmap : ")
    #     print(set_list)
    #     if(len(set_list)==2):
    #         actual_ids = set_list[0].union(set_list[1])
    #     else:
    #         actual_ids = set_list[0]

    #     precision = compute_precision(set(actual_ids), set(expected_ids))

    #     MyTest.test_results.append({
    #         "query": user_input,
    #         "precision": precision,
    #         "baseline_used": self.baseline_used
    #     })

    def run_test_case(self, user_input, expected_ids):
        print()
        print()
        print()
        print("user input : "+user_input)
        type_extractor = TypeExtractor()
        composition_extractor = CompositionExtractor()
        bw_extractor = BlackWhiteExtractor()
        otherColor_extrator =OtherColorExtractor()
        type_matcher = TypeMatcher()
        composition_matcher = CompositionMatcher()
        bw_matcher = BlackWhiteMatcher()
        otherColor_matcher = OtherColorMatcher()
        # Step 2: Create a MetaDataCard with these extractors
        extractors = {
            "type": type_extractor,
            "composition": composition_extractor,
            "blackwhite": bw_extractor,
            "otherColor": otherColor_extrator
        }
        matchers = {
            "type": type_matcher,
            "composition": composition_matcher,
            "blackwhite": bw_matcher,
            "otherColor": otherColor_matcher
        }
        matching_controller = MetadataMatchingController(matchers)

        metadata_card = MetaDataCard(extractors)
        metadata_card.generate_from_query(user_input)
        print("metadata of the user input : ")
        print(metadata_card)
        separated_user_input = separate_sentence(user_input)
        docs_with_score = get_similar_doc_for_separated_input(self.app,self.app.embedding, user_input,separated_user_input)
        print("first 5 docs before meta filtering : ")
        print(docs_with_score[:5])
        meta_filtered_docs = filter_docs(self.app,docs_with_score,metadata_card,matching_controller)
        print("first 5 docs after meta filtering : ")
        print(meta_filtered_docs[:5])
        actual_ids_pairs = get_topK_uniqueIds_from_docs(app.hashtable,meta_filtered_docs)
        #each elem of actual_ids_pairs looks like this :('#I00026b', 0.39710677)
        print(" the returned ids from get_topK_uniqueIds_from_docs : ")
        actual_ids= [pair[0] for pair in actual_ids_pairs]
        print(actual_ids)

        precision = compute_precision(set(actual_ids), set(expected_ids))

        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "baseline_used": self.baseline_used
        })

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_process_content1(self):
        user_input = "a garment with a cute drawing on it"
        expected_ids = ["#I000109"]
        self.run_test_case(user_input, expected_ids)

    def test_process_color1(self):
        user_input = "shoes that are white and black and (another color)"
        expected_ids = ["#I00005c","#I000058","#I00005f","#I000061","#I00006b","#I000087","#I000254",
                        "#I00006c","#I000072","#I00007c","#I000082","#I00008c","#I00008e"]
        self.run_test_case(user_input, expected_ids)
    
    def test_process_color2(self):
        user_input = "green and white shoes"
        expected_ids = ["#I000016","#I000063","#I000086","#I00008d"]
        self.run_test_case(user_input, expected_ids)

    def test_process_design1(self):
        user_input = "a shirt with a red thing on the back"
        expected_ids = ["#I000267"]
        self.run_test_case(user_input, expected_ids)

    def test_process_content3(self):
        user_input = "an item with the christian cross on it"
        expected_ids = ["#I0000a9"]
        self.run_test_case(user_input, expected_ids)

    def test_process_design2(self):
        user_input = "a looonng skirt"
        expected_ids = ["#I000169"]
        self.run_test_case(user_input, expected_ids)

    def test_process_comp1(self):
        user_input = "something made of cotton and polyester only"
        expected_ids = ["#I000092","#I0000e3","#I0000ed","#I0000f0","#I0000fd","#I000282","#I000166",
                        "#I000106","#I0000d8","#I0000d4","#I0000c4","#I000240","#I000275","#I00011a",
                        "#I00025a","#I000242","#I0000b1","#I0000c2","#I000097","#I000167","#I000127",
                        "#I000141","#I0000ab","#I000109","#I000276","#I000159","#I000126","#I000245"]
        self.run_test_case(user_input, expected_ids)

    def test_process_sameStyle1(self):   
        user_input = "something similar to Arsene wenger's coat"
        expected_ids = ["#I00014b"]
        self.run_test_case(user_input, expected_ids)
