
import unittest
from ..metadata_card import MetaDataCard
from SERVER.META.metadata_extraction import *

#to run this file go to root directory and do :  py -m SERVER.META.tests.metadatacard_test
class TestMetaDataCard(unittest.TestCase):

    def setUp(self):
        # Initialize the extractors
        self.type_extractor = TypeExtractor()
        self.composition_extractor = CompositionExtractor()
        self.bw_extractor = BlackWhiteExtractor()

    def create_and_test_metadata_card(self, query, expected_metadata):
        # Create a MetaDataCard with the extractors
        metadata_card = MetaDataCard({
            "type": self.type_extractor,
            "composition": self.composition_extractor,
            "blackwhite": self.bw_extractor
        })

        # Generate metadata from the query
        metadata_card.generate_from_query(query)

        # Compare the generated metadata with the expected metadata
        self.assertEqual(metadata_card.metadata["type"], expected_metadata["type"])
        self.assertEqual(metadata_card.metadata["composition_in"], expected_metadata["composition_in"])
        self.assertEqual(metadata_card.metadata["composition_out"], expected_metadata["composition_out"])
        self.assertEqual(metadata_card.metadata["contains_black"], expected_metadata["contains_black"])
        self.assertEqual(metadata_card.metadata["contains_white"], expected_metadata["contains_white"])

    def test_blue_and_white_shoes(self):
        query = "blue and white shoes"
        expected_metadata = {
            "type": "Footwear",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "yes"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_polyester_item(self):
        query = "something made of 100% polyester"
        expected_metadata = {
            "type": "unknown",
            "composition_in": {"synthetic"},
            "composition_out": {"natural", "artificial"},
            "contains_black": "unknown",
            "contains_white": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_3(self):
        query = "a tshirt/pull or something similar where the colors on it are separated by horizontal lines"
        expected_metadata = {
            "type": "Tops",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_4(self):
        query = "an item for men (but not trousers/pants) with the norvegian flag on it"
        expected_metadata = {
            "type": "unknown",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "yes"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_5(self):
        query = "a tshirt where the name of the brand is written in big"
        expected_metadata = {
            "type": "Tops",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_7(self):
        query = "an officier collar coat"
        expected_metadata = {
            "type": "Outerwear",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_8(self):
        query = "I want a checkered shirt containing the color green"
        expected_metadata = {
            "type": "Tops",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "yes"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_9(self):
        query = "I want bi-colored shoes, with white as one of the colors"
        expected_metadata = {
            "type": "Footwear",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "yes",
            "contains_other_color": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

    def test_10(self):
        query = "a pair of women's shorts that I can wear over pantyhose"
        expected_metadata = {
            "type": "Bottoms",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "unknown"
        }
        self.create_and_test_metadata_card(query, expected_metadata)

if __name__ == '__main__':
    unittest.main()
