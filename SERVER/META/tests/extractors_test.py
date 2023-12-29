import unittest
from SERVER.META.metadata_card import *
from SERVER.META.metadata_extraction import *
class TestGarmentTypeClassification(unittest.TestCase):
    
#TO RUN THIS FILE DO :  py -m SERVER.META.metadata_test at root
    # def test_material_from_query(self):
    #     test_cases = [
    #         ("blue and white shoes", {"unknown"},{"unknown"}),
    #         ('something made of 100% polyester', {"synthetic"},{"natural","artificial"}),
    #         ('a hoodie with something written on the sleeve', {"unknown"},{"unknown"}),
    #         ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', {"unknown"},{"unknown"}),
    #         ("""'I want to buy women's boots that are "covered""""" , {"unknown"},{"unknown"}),
    #         ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""",{"unknown"},{"unknown"}),
    #         ("an item where the logo of the brand is printed/visible more than one time", {"unknown"},{"unknown"}),
    #         ("a garment with a cute drawing on it", {"unknown"},{"unknown"}),
    #         ("green and white shoes", {"unknown"},{"unknown"}),
    #         ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
    #         ("an item with the christian cross on it", {"unknown"},{"unknown"}),
    #         ("a looonng skirt", {"unknown"},{"unknown"}),
    #         ('a hoodie with something written on the sleeve',{"unknown"},{"unknown"}),
    #         ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater',{"unknown"},{"unknown"}),
    #         ("""'I want to buy women's boots that are "covered""""" , {"unknown"},{"unknown"}),
    #         ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", {"unknown"},{"unknown"}),
    #         ("an item where the logo of the brand is printed/visible more than one time", {"unknown"},{"unknown"}),
    #         ("a garment with a cute drawing on it", {"unknown"},{"unknown"}),
    #         ("green and white shoes", {"unknown"},{"unknown"}),
    #         ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
    #         ("an item with the christian cross on it", {"unknown"},{"unknown"}),
    #         ("a looonng skirt", {"unknown"},{"unknown"}),
    #         ("something i can wear with a leather jacket and a blue jean", {"unknown"},{"unknown"}),
    #         ("something i can wear with a leather jacket", {"unknown"},{"unknown"}),
    #         ("something i can wear with a blue jean", {"unknown"},{"unknown"}),
    #         ("something made of cotton and polyester only", {"natural","synthetic"},{"artificial"}),
    #         ("something similar to Arsene wenger's coat",{"unknown"},{"unknown"}),
    #         ("green and white shoes", {"unknown"},{"unknown"}),
    #         ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
    #         ("an item with the christian cross on it", {"unknown"},{"unknown"}),
    #         ("a looonng skirt", {"unknown"},{"unknown"}),
    #         ("something made of cotton and polyester only", {"natural","synthetic"},{"artificial"}),
    #         ("something similar to Arsene wenger's coat", {"unknown"},{"unknown"})
    #         ]

    #     for description, expected_in,expected_out in test_cases:
    #         with self.subTest(description=description):
    #             print()
    #             print("-----------------------")
    #             print(description)
    #             print(":")
    #             actual_in,actual_out = extract_meta_composition(description)
    #             print("actual in : ")
    #             print(actual_in)
    #             print("actual out : ")
    #             print(actual_out)
    #             self.assertTrue(actual_in ==expected_in)
    #             self.assertTrue(actual_out ==expected_out)
     
    # def test_colorblackwhite(self):
    #     # List of pairs (description, expected garment type)
    #     test_cases = [
    #         ("blue and white shoes", ["unknown","yes"]),
    #         ('something made of 100% polyester',["unknown","unknown"]),
    #         ('a hoodie with something written on the sleeve', ["unknown","unknown"]),
    #         ("shoes that are white and black and (another color)", ["yes","yes"]),
    #         ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', ["unknown","unknown"]),
    #         ("""'I want to buy women's boots that are "covered""""" , ["unknown","unknown"]),
    #         ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""",["unknown","unknown"]),
    #         ("an item where the logo of the brand is printed/visible more than one time",["unknown","unknown"]),
    #         ("a garment with a cute drawing on it",["unknown","unknown"]),
    #         ("green and white shoes", ["unknown","yes"]),
    #         ("a shirt with a red thing on the back", ["unknown","unknown"]),
    #         ("an item with the christian cross on it", ["unknown","unknown"]),
    #         ("a looonng skirt", ["unknown","unknown"]),
    #         ("shoes that are white and black and (another color)", ["yes","yes"]),
    #         ('a hoodie with something written on the sleeve',["unknown","unknown"]),
    #         ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater',["unknown","unknown"]),
    #         ("""'I want to buy women's boots that are "covered""""" , ["unknown","unknown"]),
    #         ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", ["unknown","unknown"]),
    #         ("an item where the logo of the brand is printed/visible more than one time", ["unknown","unknown"]),
    #         ("a garment with a cute drawing on it", ["unknown","unknown"]),
    #         ("green and white shoes", ["unknown","yes"]),
    #         ("a shirt with a red thing on the back",["unknown","unknown"]),
    #         ("shoes that are white and black and (another color)", ["yes","yes"]),
    #         ("an item with the christian cross on it", ["unknown","unknown"]),
    #         ("a looonng skirt",["unknown","unknown"]),
    #         ("something i can wear with a leather jacket and a blue jean", ["unknown","unknown"]),
    #         ("something i can wear with a leather jacket", ["unknown","unknown"]),
    #         ("something i can wear with a blue jean",["unknown","unknown"]),
    #         ("something made of cotton and polyester only", ["unknown","unknown"]),
    #         ("something similar to Arsene wenger's coat",["unknown","unknown"]),
    #         ("green and white shoes", ["unknown","yes"]),
    #         ("a shirt with a red thing on the back", ["unknown","unknown"]),
    #         ("an item with the christian cross on it", ["unknown","unknown"]),
    #         ("a looonng skirt", ["unknown","unknown"]),
    #         ("something made of cotton and polyester only", ["unknown","unknown"]),
    #         ("something similar to Arsene wenger's coat",["unknown","unknown"])
    #         ]

    #     for description, expected in test_cases:
    #         with self.subTest(description=description):
    #             print()
    #             print("query = "+description)
    #             result = extract_meta_blackwhite(description)
    #             print("actual result :")
    #             print(result)
    #             print()
    #             self.assertTrue(result[0]==expected[0] and result[1]==expected[1])
    def test_othercolor(self):
        # List of pairs (description, expected garment type)
        test_cases = [
            ("blue and white shoes", "yes"),
            ('something made of 100% polyester',"unknown"),
            ('a hoodie with something written on the sleeve', "unknown"),
            ("shoes that are white and black and (another color)", "yes"),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', "unknown"),
            ("""'I want to buy women's boots that are "covered""""" , "unknown"),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""","unknown"),
            ("an item where the logo of the brand is printed/visible more than one time","unknown"),
            ("a garment with a cute drawing on it","unknown"),
            ("green and white shoes", "yes"),
            ("a shirt with a red thing on the back", "yes"),
            ("an item with the christian cross on it", "unknown"),
            ("a looonng skirt", "unknown"),
            ("shoes that are white and black and (another color)", "yes"),
            ('a hoodie with something written on the sleeve',"unknown"),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater',"unknown"),
            ("""'I want to buy women's boots that are "covered""""" , "unknown"),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", "unknown"),
            ("an item where the logo of the brand is printed/visible more than one time", "unknown"),
            ("a garment with a cute drawing on it", "unknown"),
            ("green and white shoes", "yes"),
            ("a shirt with a red thing on the back","yes"),
            ("shoes that are white and black and (another color)", "yes"),
            ("an item with the christian cross on it", "unknown"),
            ("a looonng skirt","unknown"),
            ("something i can wear with a leather jacket and a blue jean", "unknown"),
            ("something i can wear with a leather jacket", "unknown"),
            ("something i can wear with a blue jean","unknown"),
            ("something made of cotton and polyester only", "unknown"),
            ("something similar to Arsene wenger's coat","unknown"),
            ("green and white shoes", "yes"),
            ("a shirt with a red thing on the back", "yes"),
            ("an item with the christian cross on it", "unknown"),
            ("a looonng skirt", "unknown"),
            ("something made of cotton and polyester only", "unknown"),
            ("something similar to Arsene wenger's coat","unknown")
            ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                print()
                print("query = "+description)
                extractor = OtherColorExtractor()
                result = extractor.extract(description)
                print("actual result :")
                print(result)
                print()
                self.assertTrue(result==expected)
    
if __name__ == '__main__':
    unittest.main()
