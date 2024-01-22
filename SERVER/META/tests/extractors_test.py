import unittest

import sys
import os

server_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
sys.path.append(server_directory)

from META.metadata_card import *
from META.metadata_extraction import *

class TestIndividualExtractors(unittest.TestCase):
    
    def test_material_from_query(self):
        test_cases = [
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", {"unknown"},{"unknown"}),
            ("an item for men (but not trousers/pants) with the norwegian flag on it",{"unknown"},{"unknown"}),
            ("a tshirt where the name of the brand is written in big", {"unknown"},{"unknown"}),
            ("a stand collar coat", {"unknown"},{"unknown"}),
            ("I want a checkered shirt containing the color green", {"unknown"},{"unknown"}),
            ("an officier collar coat" , {"unknown"},{"unknown"}),
            ("I want bi-colored shoes, with white as one of the colors",{"unknown"},{"unknown"}),
            ("a pair of women's shorts that I can wear over pantyhose",{"unknown"},{"unknown"}),
            ("sailor/marinière style for women ",{"unknown"},{"unknown"}),
            ("something related to FC barcelona", {"unknown"},{"unknown"}),

            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", {"unknown"},{"unknown"}),
            ("an item for men (but not trousers/pants) with the norwegian flag on it",{"unknown"},{"unknown"}),
            ("a tshirt where the name of the brand is written in big", {"unknown"},{"unknown"}),
            ("a stand collar coat", {"unknown"},{"unknown"}),
            ("I want a checkered shirt containing the color green", {"unknown"},{"unknown"}),
            ("an officier collar coat" , {"unknown"},{"unknown"}),
            ("I want bi-colored shoes, with white as one of the colors",{"unknown"},{"unknown"}),
            ("a pair of women's shorts that I can wear over pantyhose",{"unknown"},{"unknown"}),
            ("sailor/marinière style for women ",{"unknown"},{"unknown"}),
            ("something related to FC barcelona", {"unknown"},{"unknown"}),

            ("blue and white shoes", {"unknown"},{"unknown"}),
            ('something made of 100% polyester', {"synthetic"},{"natural","artificial"}),
            ('a hoodie with something written on the sleeve', {"unknown"},{"unknown"}),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', {"unknown"},{"unknown"}),
            ("""'I want to buy women's boots that are "covered""""" , {"unknown"},{"unknown"}),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""",{"unknown"},{"unknown"}),
            ("an item where the logo of the brand is printed/visible more than one time", {"unknown"},{"unknown"}),
            ("a garment with a cute drawing on it", {"unknown"},{"unknown"}),
            ("green and white shoes", {"unknown"},{"unknown"}),
            ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
            ("an item with the christian cross on it", {"unknown"},{"unknown"}),
            ("a looonng skirt", {"unknown"},{"unknown"}),
            ('a hoodie with something written on the sleeve',{"unknown"},{"unknown"}),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater',{"unknown"},{"unknown"}),
            ("""'I want to buy women's boots that are "covered""""" , {"unknown"},{"unknown"}),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", {"unknown"},{"unknown"}),
            ("an item where the logo of the brand is printed/visible more than one time", {"unknown"},{"unknown"}),
            ("a garment with a cute drawing on it", {"unknown"},{"unknown"}),
            ("green and white shoes", {"unknown"},{"unknown"}),
            ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
            ("an item with the christian cross on it", {"unknown"},{"unknown"}),
            ("a looonng skirt", {"unknown"},{"unknown"}),
            ("something i can wear with a leather jacket and a blue jean", {"unknown"},{"unknown"}),
            ("something i can wear with a leather jacket", {"unknown"},{"unknown"}),
            ("something i can wear with a blue jean", {"unknown"},{"unknown"}),
            ("something made of cotton and polyester only", {"natural","synthetic"},{"artificial"}),
            ("something similar to Arsene wenger's coat",{"unknown"},{"unknown"}),
            ("green and white shoes", {"unknown"},{"unknown"}),
            ("a shirt with a red thing on the back", {"unknown"},{"unknown"}),
            ("an item with the christian cross on it", {"unknown"},{"unknown"}),
            ("a looonng skirt", {"unknown"},{"unknown"}),
            ("something made of cotton and polyester only", {"natural","synthetic"},{"artificial"}),
            ("something similar to Arsene wenger's coat", {"unknown"},{"unknown"})
            ]

        for description, expected_in,expected_out in test_cases:
            with self.subTest(description=description):
                extractor = CompositionExtractor()
                actual_in,actual_out  = extractor.extract(description)
                if(actual_in!=expected_in or actual_out!=expected_out):
                    print()
                    print("-----------------------")
                    print(description)
                    print(":")
                    print("actual in : ")
                    print(actual_in)
                    print("actual out : ")
                    print(actual_out)
                self.assertTrue(actual_in ==expected_in)
                self.assertTrue(actual_out ==expected_out)
     
    def test_colorblackwhite(self):
        # List of pairs (description, expected garment type)
        print("testing black white extractor")
        test_cases = [
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", ["unknown","unknown"]),
            ("an item for men (but not trousers/pants) with the norwegian flag on it",["unknown","yes"]),
            ("a tshirt where the name of the brand is written in big", ["unknown","unknown"]),
            ("a stand collar coat", ["unknown","unknown"]),
            ("I want a checkered shirt containing the color green", ["unknown","unknown"]),
            ("an officier collar coat" , ["unknown","unknown"]),
            ("I want bi-colored shoes, with white as one of the colors",["unknown","yes"]),
            ("a pair of women's shorts that I can wear over pantyhose",["unknown","unknown"]),
            ("sailor/marinière style for women ",["unknown","unknown"]),
            ("something related to FC barcelona",["unknown","unknown"]),

            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", ["unknown","unknown"]),
            ("an item for men (but not trousers/pants) with the norwegian flag on it",["unknown","yes"]),
            ("a tshirt where the name of the brand is written in big", ["unknown","unknown"]),
            ("a stand collar coat", ["unknown","unknown"]),
            ("I want a checkered shirt containing the color green", ["unknown","unknown"]),
            ("an officier collar coat" , ["unknown","unknown"]),
            ("I want bi-colored shoes, with white as one of the colors",["unknown","yes"]),
            ("a pair of women's shorts that I can wear over pantyhose",["unknown","unknown"]),
            ("sailor/marinière style for women ",["unknown","unknown"]),
            ("something related to FC barcelona",["unknown","unknown"]),

            ("blue and white shoes", ["unknown","yes"]),
            ('something made of 100% polyester',["unknown","unknown"]),
            ('a hoodie with something written on the sleeve', ["unknown","unknown"]),
            ("shoes that are white and black and (another color)", ["yes","yes"]),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', ["unknown","unknown"]),
            ("""'I want to buy women's boots that are "covered""""" , ["unknown","unknown"]),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""",["unknown","unknown"]),
            ("an item where the logo of the brand is printed/visible more than one time",["unknown","unknown"]),
            ("a garment with a cute drawing on it",["unknown","unknown"]),
            ("green and white shoes", ["unknown","yes"]),
            ("a shirt with a red thing on the back", ["unknown","unknown"]),
            ("an item with the christian cross on it", ["unknown","unknown"]),
            ("a looonng skirt", ["unknown","unknown"]),
            ("shoes that are white and black and (another color)", ["yes","yes"]),
            ('a hoodie with something written on the sleeve',["unknown","unknown"]),
            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater',["unknown","unknown"]),
            ("""'I want to buy women's boots that are "covered""""" , ["unknown","unknown"]),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", ["unknown","unknown"]),
            ("an item where the logo of the brand is printed/visible more than one time", ["unknown","unknown"]),
            ("a garment with a cute drawing on it", ["unknown","unknown"]),
            ("green and white shoes", ["unknown","yes"]),
            ("a shirt with a red thing on the back",["unknown","unknown"]),
            ("shoes that are white and black and (another color)", ["yes","yes"]),
            ("an item with the christian cross on it", ["unknown","unknown"]),
            ("a looonng skirt",["unknown","unknown"]),
            ("something i can wear with a leather jacket and a blue jean", ["unknown","unknown"]),
            ("something i can wear with a leather jacket", ["unknown","unknown"]),
            ("something i can wear with a blue jean",["unknown","unknown"]),
            ("something made of cotton and polyester only", ["unknown","unknown"]),
            ("something similar to Arsene wenger's coat",["unknown","unknown"]),
            ("green and white shoes", ["unknown","yes"]),
            ("a shirt with a red thing on the back", ["unknown","unknown"]),
            ("an item with the christian cross on it", ["unknown","unknown"]),
            ("a looonng skirt", ["unknown","unknown"]),
            ("something made of cotton and polyester only", ["unknown","unknown"]),
            ("something similar to Arsene wenger's coat",["unknown","unknown"])
            ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                print("-----------------------")
                extractor = BlackWhiteExtractor()
                result = extractor.extract(description)
                if(result[0]!=expected[0] or result[1]!=expected[1]):
                    
                    print("query = "+description)
                    print("actual result :")
                    print(result)
                    print("expected result :")
                    print(expected)
                self.assertTrue(result[0]==expected[0] and result[1]==expected[1])

    def test_othercolor(self):
        print("testing other color...")
        print()
        # List of pairs (description, expected garment type)
        test_cases = [
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","yes"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "yes"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","unknown"),
            ("sailor/marinière style for women ","unknown"),
            ("something related to FC barcelona", "unknown"),

            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","yes"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "yes"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","unknown"),
            ("sailor/marinière style for women ","unknown"),
            ("something related to FC barcelona", "unknown"),
            
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
                extractor = OtherColorExtractor()
                result = extractor.extract(description)
                if(result != expected):
                    print()
                    print("query = "+description)
                    print("actual result :")
                    print(result)
                    print("expected result :")
                    print(expected)
                    print()
                self.assertTrue(result==expected)
    
    def test_genre(self):
        print("testing genre...")
        print()
        test_cases = [
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","men"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "unknown"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","women"),
            ("sailor/marinière style for women ","women"),
            ("something related to FC barcelona", "unknown"),

            ("a garment with a cute drawing on it", "unknown"),
            ("shoes that are white and black and (another color)", "unknown"),
            ("green and white shoes", "unknown"),
            ("a shirt with a red thing on the back", "unknown"),
            ("an item with the christian cross on it","unknown"),
            ("a looonng skirt","unknown"),
            ("something made of cotton and polyester only", "unknown"),
            ("something similar to Arsene wenger's coat", "unknown"),

            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', "unknown"),
            ("""'I want to buy women's boots that are "covered""""", "women"),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", "unknown"),
            ("an item where the logo of the brand is printed/visible more than one time","unknown"),
            ("blue and white shoes", "unknown"),

            ("something i can wear with a leather jacket and a blue jean", "unknown"),
            ("something i can wear with a leather jacket", "unknown"),
            ("something i can wear with a blue jean","unknown"),

            #x2:
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","men"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "unknown"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","women"),
            ("sailor/marinière style for women ","women"),
            ("something related to FC barcelona", "unknown"),

            ("a garment with a cute drawing on it", "unknown"),
            ("shoes that are white and black and (another color)", "unknown"),
            ("green and white shoes", "unknown"),
            ("a shirt with a red thing on the back", "unknown"),
            ("an item with the christian cross on it","unknown"),
            ("a looonng skirt","unknown"),
            ("something made of cotton and polyester only", "unknown"),
            ("something similar to Arsene wenger's coat", "unknown"),

            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', "unknown"),
            ("""'I want to buy women's boots that are "covered""""", "women"),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", "unknown"),
            ("an item where the logo of the brand is printed/visible more than one time","unknown"),
            ("blue and white shoes", "unknown"),

            ("something i can wear with a leather jacket and a blue jean", "unknown"),
            ("something i can wear with a leather jacket", "unknown"),
            ("something i can wear with a blue jean","unknown"),
            #x3:

            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","men"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "unknown"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","women"),
            ("sailor/marinière style for women ","women"),
            ("something related to FC barcelona", "unknown"),

            ("a garment with a cute drawing on it", "unknown"),
            ("shoes that are white and black and (another color)", "unknown"),
            ("green and white shoes", "unknown"),
            ("a shirt with a red thing on the back", "unknown"),
            ("an item with the christian cross on it","unknown"),
            ("a looonng skirt","unknown"),
            ("something made of cotton and polyester only", "unknown"),
            ("something similar to Arsene wenger's coat", "unknown"),

            ('a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater', "unknown"),
            ("""'I want to buy women's boots that are "covered""""", "women"),
            ("""boots that are “dropping” ie the tip of the boot fabric covers/falls on the heel part and covers the heel! trend last year and this year""", "unknown"),
            ("an item where the logo of the brand is printed/visible more than one time","unknown"),
            ("blue and white shoes", "unknown"),

            ("something i can wear with a leather jacket and a blue jean", "unknown"),
            ("something i can wear with a leather jacket", "unknown"),
            ("something i can wear with a blue jean","unknown"),
            ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                extractor = GenreExtractor()
                result = extractor.extract(description)
                if(result != expected):
                    print()
                    print("query = "+description)
                    print("actual result :")
                    print(result)
                    print("expected :")
                    print(expected)
                self.assertTrue(result==expected)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestIndividualExtractors('test_colorblackwhite'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    #if you want to run all the tests, uncomment this and comment all the block above:
    #unittest.main()