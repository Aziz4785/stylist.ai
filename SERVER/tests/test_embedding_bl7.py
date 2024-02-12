import unittest
from flask_testing import TestCase
from SERVER.server3 import app  # Import your Flask app
import json
import os
import SERVER.common_variables
# Imports from SERVER/META
from SERVER.META.metadata_card import *
from SERVER.META.metadata_matching_controller import *
from SERVER.META.metadata_extraction import *
from SERVER.META.metadata_matching import *

# If ServerUtil.py is in the SERVER directory
from SERVER.ServerUtil import *

# run py -m unittest SERVER.tests.test_embedding_bl7 at root
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
    if(len(expected_id_set))>0 and len(actual_id_set)>0:
        precision = tp / min(len(actual_id_set),len(expected_id_set))
    return precision

def extract_id_from_response(data):
    ans = []
    for elem in data:
        ans.append(elem['_id'])
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

        total_precision_simple_separated = sum(result['separated_simple_precision'] for result in cls.test_results if result['query_formulation'] == "simple" and "separated_simple_precision" in result )
        count_simple_separated_results = sum(1 for result in cls.test_results if result['query_formulation'] == "simple" and "separated_simple_precision" in result)
        print("number of simple separated : "+str(count_simple_separated_results))
        average_precision_separated_simple = total_precision_simple_separated / count_simple_separated_results if count_simple_separated_results else 0

        total_precision_IWsimple = sum(result['precision'] for result in cls.test_results if result['query_formulation'] == "i_want_simple")
        count_IW = sum(1 for result in cls.test_results if result['query_formulation'] == "i_want_simple")
        average_precision_IWsimple = total_precision_IWsimple / count_IW if count_IW else 0


        total_precision_ILFsimple = sum(result['precision'] for result in cls.test_results if result['query_formulation'] == "imlookingfor_simple")
        count_ILF = sum(1 for result in cls.test_results if result['query_formulation'] == "imlookingfor_simple")
        average_precision_ILFsimple = total_precision_ILFsimple / count_ILF if count_ILF else 0

        total_precision_feature_word = sum(result['feature_word_precision'] for result in cls.test_results)
        average_precision_featureword = total_precision_feature_word / len(cls.test_results) if cls.test_results else 0
        report_data = {
            "average_precision": average_precision,
            "average_precision_featureword": average_precision_featureword,
            "average_precision (simple queries)": average_precision_simple,
            "average_precision_separated_simple": average_precision_separated_simple,
            "average_precision (i want simple queries)": average_precision_IWsimple,
            "average_precision (imlooking for simple queries)": average_precision_ILFsimple,
            "test_results": cls.test_results
        }
        with open('test_embedding_bl7_report.json', 'w', encoding='utf-8') as file:
            json.dump(report_data, file, indent=4, ensure_ascii=False)

    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        self.app = self.create_app()
        self.baseline_used = "baseline_data7"
        self.app.config['BASELINE_PATH'] = os.path.join(os.path.dirname(__file__), '..', '..', 'MAIN_DATA', f'{self.baseline_used}.json')

    def load_expected_json(self):
        with open('expected_output.json') as file:
            return json.load(file)
    
    def run_test_case(self, user_input, expected_ids,query_formulation="other"):
        print()
        print()
        print()
        print()
        print()
        print()
        print("user input : "+user_input)
        type_extractor = TypeExtractor()
        composition_extractor = CompositionExtractor()
        bw_extractor = BlackWhiteExtractor()
        otherColor_extrator =OtherColorExtractor()
        gender_extractor = GenderExtractor()

        type_matcher = TypeMatcher()
        composition_matcher = CompositionMatcher()
        bw_matcher = BlackWhiteMatcher()
        otherColor_matcher = OtherColorMatcher()
        gender_matcher= GenderMatcher()
        # Step 2: Create a MetaDataCard with these extractors
        extractors = {
            "type": type_extractor,
            "composition": composition_extractor,
            "blackwhite": bw_extractor,
            "otherColor": otherColor_extrator,
            "gender": gender_extractor
        }
        matchers = {
            "type": type_matcher,
            "composition": composition_matcher,
            "blackwhite": bw_matcher,
            "otherColor": otherColor_matcher,
            "gender": gender_matcher
        }
        matching_controller = MetadataMatchingController(matchers)

        metadata_card = MetaDataCard(extractors)
        metadata_card.generate_from_query(user_input)
        print("metadata of the user input : ")
        print(metadata_card)
        separated_user_input = separate_sentence(user_input)
        feature_words = extract_feature_words_from_query(user_input).split(',')
        most_important_word = feature_words[0]
        if(len(feature_words)>1 and most_important_word.lower() in {"white","black","men","women","for men","for women"} ):
            most_important_word = feature_words[1]
        print("feature words : ")
        print(feature_words)

        meta_filtered_separated_docs = []
        k=60
        if(query_formulation == "simple"):
            while(len(meta_filtered_separated_docs)<20 and k<1000):
                docs_with_score = get_similar_doc_for_separated_input(self.app,self.app.embedding, user_input,separated_user_input,k=k)
                meta_filtered_separated_docs = filter_docs(self.app,docs_with_score,metadata_card,matching_controller)
                k*=2

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
        ids_from_featureWord = get_topK_uniqueIds_from_docs(app.hashtable_small_chunks,meta_filtered_feature_words_docs,k=24)
        #each elem of actual_ids_pairs looks like this :('#I00026b', 0.39710677)
        print(" the returned ids from get_topK_uniqueIds_from_docs : ")
        actual_ids= [pair[0] for pair in actual_ids_pairs]
        actual_ids_from_featureword= [pair[0] for pair in ids_from_featureWord]
        print(actual_ids)

        precision = compute_precision(set(actual_ids), set(expected_ids))
        feature_word_precision = compute_precision(set(actual_ids_from_featureword), set(expected_ids))
        
        if(query_formulation == "simple"):
            idsPairs_from_separated_input_simple = get_topK_uniqueIds_from_docs(app.hashtable,meta_filtered_separated_docs,k=24)
            ids_from_separated_input_simple= [pair[0] for pair in idsPairs_from_separated_input_simple]
            separated_input_precision = compute_precision(set(ids_from_separated_input_simple), set(expected_ids))
        MyTest.test_results.append({
            "query": user_input,
            "precision": precision,
            "keyword":most_important_word,
            "feature_word_precision":feature_word_precision,
            "baseline_used": self.baseline_used,
            "query_formulation": query_formulation
        })
        if(query_formulation == "simple"):
            MyTest.test_results[-1]["separated_simple_precision"]=separated_input_precision
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_1(self):
        user_input = "a tshirt/pull or something similar where the colors on it are separated by horizontal lines"
        expected_ids = ["#I000257","#I00025d","#I000276","#I000237","#I0001f8"]
        self.run_test_case(user_input, expected_ids, "simple")

    def test_1a(self):
        #user_input = "Could you help me find a t-shirt, pullover, or something similar where the colors are separated by horizontal lines?"
        user_input = "I want a tshirt/pull or something similar where the colors on it are separated by horizontal lines"
        expected_ids = ["#I000257","#I00025d","#I000276","#I000237","#I0001f8"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_1b(self):
        #user_input = "I'm interested in finding garments such as t-shirts or pullovers, specifically those with colors divided by horizontal lines."
        user_input = "I'm looking for a tshirt/pull or something similar where the colors on it are separated by horizontal lines"
        expected_ids = ["#I000257","#I00025d","#I000276","#I000237","#I0001f8"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_2(self):
        user_input = "an item for men (but not trousers/pants) with the norwegian flag on it"
        expected_ids = ["#I00025a"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_2a(self):
        user_input = "I want an item for men (but not trousers/pants) with the norwegian flag on it"
        #user_input = "I am looking for men's clothing. On this item of clothing, we should be able to see the flag of Norway. I don't want pants please"
        expected_ids = ["#I00025a"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_2b(self):
        user_input = "I'm looking for an item for men (but not trousers/pants) with the norwegian flag on it"
        #user_input = "I'm aiming to buy men's wear, other than trousers or pants, that includes the Norwegian flag."
        expected_ids = ["#I00025a"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_3(self):
        user_input = "a tshirt where the name of the brand is written in big"
        expected_ids = ["#I000272","#I00020b","#I000298","#I0001fb","#I000295","#I000201"]
        self.run_test_case(user_input, expected_ids, "simple")

    def test_3a(self):
        user_input = "I want a tshirt where the name of the brand is written in big"
        #user_input = "I'm looking for t-shirts where the brand name is featured prominently. Do you have any?"
        expected_ids = ["#I000272","#I00020b","#I000298","#I0001fb","#I000295","#I000201"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_3b(self):
        user_input = "I'm looking for a tshirt where the name of the brand is written in big"
        #user_input = "I want to find t-shirts that have large, eye-catching brand names on them."
        expected_ids = ["#I000272","#I00020b","#I000298","#I0001fb","#I000295","#I000201"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_4(self):
        user_input = "a stand collar coat"
        expected_ids = ["#I000273"]
        self.run_test_case(user_input, expected_ids, "simple")

    def test_4a(self):
        user_input = "I want a stand collar coat"
        #user_input = "Do you have a coat with a high collar please?"
        expected_ids = ["#I000273"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_4b(self):
        user_input = "I'm looking for a stand collar coat"
        #user_input = "I'm interested in finding a coat that features a stand collar."
        expected_ids = ["#I000273"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_5(self):
        user_input = "a checkered shirt containing the color green"
        expected_ids = ["#I000275"]
        self.run_test_case(user_input, expected_ids, "simple")

    def test_5a(self):
        user_input = "I want a checkered shirt containing the color green"
        #user_input = "Could you show me your selection of checkered shirts that include the color green?"
        expected_ids = ["#I000275"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_5b(self):
        user_input = "I'm looking for a checkered shirt containing the color green"
        #user_input = "I'd like to see your checkered shirts, especially those with green in the pattern."
        expected_ids = ["#I000275"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_7(self):
        user_input = "bi-colored shoes, with white as one of the colors"
        expected_ids = ["#I0003cb","#I000460","#I0000e9","#I0000c0","#I0004a2","#I0000b4","#I000088","#I00008a","#I00007b","#I0000b4","#I0000f2"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_7a(self):
        user_input = "I want bi-colored shoes, with white as one of the colors"
        #user_input = "I want shoes that contain white and another color"
        expected_ids = ["#I0003cb","#I000460","#I0000e9","#I0000c0","#I0004a2","#I0000b4","#I000088","#I00008a","#I00007b","#I0000b4","#I0000f2"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_7b(self):
        user_input = "I'm looking for bi-colored shoes, with white as one of the colors"
        #user_input = "I'm aiming to buy shoes that combine two colors, with white as one of them."
        expected_ids = ["#I0003cb","#I000460","#I0000e9","#I0000c0","#I0004a2","#I0000b4","#I000088","#I00008a","#I00007b","#I0000b4","#I0000f2"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_8(self):
        user_input = "women's shorts that I can wear over pantyhose"
        expected_ids = ["#I000250","#I000209"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_8a(self):
        user_input = "I want women's shorts that I can wear over tights"
        expected_ids = ["#I000250","#I000209"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_8b(self):
        user_input = "I'm looking for women's shorts that I can wear over tights"
        #user_input = "I'm seeking women's shorts with enough room to be worn over tights."
        expected_ids = ["#I000250","#I000209"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")
    
    def test_9(self):
        user_input = "marinière style for women"
        expected_ids = ["#I000237","#I000243","#I0001fe"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_9a(self):
        user_input = "I want a marinière style for women"
        #user_input = "I'm keen on finding women's garments that showcase a marinière style."
        expected_ids = ["#I000237","#I000243","#I0001fe"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_9b(self):
        user_input = "I'm looking for a marinière style for women"
        #user_input = "women's clothing with a marinière style" #translated from french
        expected_ids = ["#I000237","#I000243","#I0001fe"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_10(self):
        user_input = "something related to FC barcelona"
        expected_ids = ["#I0000ad"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_10a(self):
        #user_input = "I want to buy something to my kid. He is a fan of FC Barcelona"
        user_input = "I want something related to FC barcelona"
        expected_ids = ["#I0000ad"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_10b(self):
        user_input = "I'm looking for something related to FC barcelona"
        #user_input = "i am a Fc barcelona fan and i want others to know that i am a Fc barcelona  fan. Please find me a piece of clothing that allows me to do this"
        expected_ids = ["#I0000ad"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")
    
    def test_11(self):
        user_input = "shoes where the outer sole starts from the top back of the shoe"
        expected_ids = ["#I0004b1"]
        self.run_test_case(user_input, expected_ids, "simple")

    def test_11a(self):
        user_input = "I want shoes where the outer sole starts from the top back of the shoe"
        expected_ids = ["#I0004b1"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_11b(self):
        user_input = "I'm looking for shoes where the outer sole starts from the top back of the shoe"
        expected_ids = ["#I0004b1"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_12(self):
        user_input = "black and white shoes with a thick sole"
        expected_ids = ["#I00046e","#I00047c","#I000480","#I000484","#I0004af","#I000494","#I000485","#I000459","#I000447","#I00000d"]
        self.run_test_case(user_input, expected_ids, "simple")
    
    def test_12a(self):
        user_input = "I want black and white shoes with a thick sole"
        expected_ids = ["#I00046e","#I00047c","#I000480","#I000484","#I0004af","#I000494","#I000485","#I000459","#I000447","#I00000d"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_12b(self):
        user_input = "I'm looking for black and white shoes with a thick sole"
        expected_ids = ["#I00046e","#I00047c","#I000480","#I000484","#I0004af","#I000494","#I000485","#I000459","#I000447","#I00000d"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")

    def test_13(self):
        user_input = "clothes with no more than 10% polyester"
        expected_ids = ["#I0001e3","#I00026a","#I000257","#I00049b", "#I000477", "#I000461","#I000419",
                        "#I000450","#I00044c","#I00044b","#I00044a","#I000417","#I0003ed","#I0003df",
                        "#I0003d3","#I0003d2","#I0003d1","#I0003cf","#I0003cc", "#I0003c4","#I000254",
                        "#I000251","#I00024f","#I00024d","#I000248","#I00023f", "#I00022f","#I00022d"]
        self.run_test_case(user_input, expected_ids,"simple")

    def test_13a(self):
        user_input = "I want clothes with no more than 10% polyester"
        expected_ids = ["#I0001e3","#I00026a","#I000257","#I00049b", "#I000477", "#I000461","#I000419",
                        "#I000450","#I00044c","#I00044b","#I00044a","#I000417","#I0003ed","#I0003df",
                        "#I0003d3","#I0003d2","#I0003d1","#I0003cf","#I0003cc", "#I0003c4","#I000254",
                        "#I000251","#I00024f","#I00024d","#I000248","#I00023f", "#I00022f","#I00022d"]
        self.run_test_case(user_input, expected_ids, "i_want_simple")

    def test_13b(self):
        user_input = "I'm looking for clothes with no more than 10% polyester"
        expected_ids = ["#I0001e3","#I00026a","#I000257","#I00049b", "#I000477", "#I000461","#I000419",
                        "#I000450","#I00044c","#I00044b","#I00044a","#I000417","#I0003ed","#I0003df",
                        "#I0003d3","#I0003d2","#I0003d1","#I0003cf","#I0003cc", "#I0003c4","#I000254",
                        "#I000251","#I00024f","#I00024d","#I000248","#I00023f", "#I00022f","#I00022d"]
        self.run_test_case(user_input, expected_ids,"imlookingfor_simple")