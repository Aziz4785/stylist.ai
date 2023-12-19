import unittest
from metadata_generator import classify_garment_type  # Replace 'your_module' with the name of the module where your function is defined

class TestGarmentTypeClassification(unittest.TestCase):

    def test_classification(self):
        # List of pairs (description, expected garment type)
        test_cases = [
            ("A short-sleeved cotton t-shirt.", "Tops"),
            ("Denim jeans with a straight fit.", "Bottoms"),
            ("A waterproof hooded jacket.", "Outerwear"),
            ("Silk boxers with an elastic waistband.", "Underwear"),
            ("Running shoes with cushioned soles.", "Footwear"),
            ("A leather belt with a metal buckle.", "Accessories"),
            ("A jumpsuit with a zippered front.", "One-Pieces"),
            ("An item that does not fit into any category.", "unknown"),
            ("""Olive green, black glitter.\n\nThe Vanessa Bruno Cabas tote features a sturdy olive-green canvas construction with sparkling black glitter trim. It has a practical and spacious open-top design, with an additional mobile phone compartment inside. Long handles allow for shoulder carrying, and the bottom panel provides a slight contrast in color, enhancing the bag's structure. It boasts a minimalist aesthetic with a dash of glamour, perfect for versatile daily use.""","Accessories"),
            ("""Black, gold.\n\nThe images show a black leather handbag with a solid color design. Its quilted texture and structured shape give it an elegant and timeless look. The bag features a distinctive gold-tone circular closure on the front, adding a touch of sophistication. The top handle is complemented by a detachable chain strap, offering versatility in carrying options. The interior, as revealed in one of the images, appears to be spacious with a cotton lining and includes practical compartments for organization. There are no visible graphics or text, maintaining the handbag's sleek and polished aesthetic.""", "Accessories"),
            ("""White, orange, black\n\nThe Nike Sportswear COURT VINTAGE UNISEX - Baskets basses are predominantly white with subtle orange and black accents. These low-top sneakers feature a classic round toe and a flat heel, suitable for tennis. The closure is achieved with white laces. The side display perforations and cutouts contribute to the shoe’s breathability and design detail. A signature swoosh logo is visible on the shoe's side in a contrasting black with an orange outline. On the tongue and heel tab, branding completes the look, with a small orange swoosh and text against a black label. The outsole is white, maintaining a monochromatic base for an overall minimalist and retro aesthetic.""", "Footwear"),
            ("""The images depict a pair of Even&Odd Wide Fit Bottines in a solid black color. These ankle boots have a round toe design and feature a chunky block heel with a platform sole. The rugged outsole enhances its bold silhouette. The boots are of slip-on style, utilizing elastic straps on the sides for ease of fitting, along with pull-loops at the back to assist in wearing them. They are detailed with rivets, likely contributing to both the aesthetic and structure of the boots. The design is sleek and utilitarian, leaning towards a modern and edgy fashion statement. There are no visible graphics or text on the boots.""", "Footwear")
        ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                result = classify_garment_type(description)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
