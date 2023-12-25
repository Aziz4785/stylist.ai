import unittest
from metadata_card import extract_meta_composition 

class TestGarmentTypeClassification(unittest.TestCase):
    """
    def test_material_from_query(self):
        test_cases = [
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
                print()
                print("-----------------------")
                print(description)
                print(":")
                actual_in,actual_out = extract_meta_composition(description)
                print("actual in : ")
                print(actual_in)
                print("actual out : ")
                print(actual_out)
                self.assertTrue(actual_in ==expected_in)
                self.assertTrue(actual_out ==expected_out)
        """

    def test_colorblackwhite(self):
        # List of pairs (description, expected garment type)
        test_cases = [
            ("Heather grey, white\n\nThe Tommy Jeans ORIGINAL TEE - T-shirt basique is a classic heather grey with a small, white logo embroidery on the left chest area, adding a subtle touch of branding. It features a round collar and short sleeves, providing a casual yet stylish look. The jersey fabric ensures a comfortable fit and breathability. Its versatile design makes it suitable for a range of occasions and easy to pair with various bottoms and shoes.", {"no","yes"}),
            ("brown\n\nThe Tommy Hilfiger CORE BOOT Derbies are brown suede boots featuring a round toe and block heel, giving them a classic and robust appearance. They have a lacing closure system with round, dark brown laces that complement the shoe's overall color. The boots exhibit a solid color design, maintaining simplicity and elegance. A distinctive feature is the subtle presence of a brand logo, which adds a touch of designer prestige while retaining the shoe's understated aesthetics. The synthetic outsole shows a thin, red stripe that subtly contrasts with the brown suede, enhancing the visual appeal of the boots. Overall, the design is clean and timeless, suitable for both casual and more dressed-up occasions.", {"no","no"}),
            ("The garment is navy blue. It is a pair of men's boxer brief shorts with a snug fit and a short leg design, promoting a modern silhouette. The waistband is elastic and prominently features the Tommy Hilfiger brand with the name written in white on a red stripe above a white stripe, which adds a striking contrast to the solid navy blue body of the garment. There are no visible seams on the shorts, indicating a seamless design that probably enhances comfort. The fit appears normal, adhering closely to the body without being overly tight. There is no visible pattern or additional graphics besides the brand name on the waistband.", {"no","yes"}),
            ("White\n\nThe showcased Pier One Chemise is a classic men's long-sleeved shirt in a bright white hue. It features a Kent collar and a front button closure, providing a clean and traditional look. The shirt's design is elegant and simple with no visible graphics or text, emphasizing its solid color and creating a pristine, professional appearance. It has a light transparency level, which contributes to its breathability and comfort. The shirt's tailored fit and lightweight fabric make it suitable for both formal and casual settings. The garment's environmental characteristics are not visible in the images.", {"no","yes"}),
            ("Navy blue, beige, white.\n\nThe New Balance 574 UNISEX sneakers feature a classic low-top design. The upper is predominantly navy blue, contrasted by a large, beige 'N' logo on the side and matching beige accents on the heel and outsole tread. The round shoe toe maintains a traditional and versatile look, while the flat heel ensures a stable, everyday wear. Its lacing closure promises a secure fit. The design encapsulates a timeless athletic aesthetic with a breathable upper, highlighted by tonal stitching and additional brand detailing on the tongue and heel in white text. The outsole is a light tan, complementing the overall color scheme.", {"no","yes"}),
            ("Black\n\nThe leggings displayed in the images are solid black in color and designed for maternity wear. They exhibit a high-waisted style, ensuring a comfortable fit for expecting mothers. The leggings feature an elastic waistband that provides an adjustable and secure fit. Owing to the high cotton content, the leggings likely offer a soft and breathable experience. The jersey material ensures added stretch and flexibility, courtesy of the elastane, which complements the body changes during pregnancy. The images do not show any visible graphics, prints, or text, highlighting the leggings' versatile and straightforward design. The overall appearance suggests practicality with a focus on comfort and adaptability for daily wear.", {"yes","no"}),
            ("The adidas Sportswear Survêtement is predominantly black. The design is sleek and contemporary, maintaining a solid color theme with the brand's signature three stripes in white running down the sides of the sleeves and pants for a subtle contrast. It features a trucker-style collar on the zip-up jacket for a semi-formal touch and ribbed, elastic cuffs for comfort and fit. The jacket showcases a small, white adidas logo on the right chest, while the pants repeat the logo on the left thigh. The waist of the pants is elasticized for a custom fit, and both the jacket and pants are equipped with side pockets for functionality, adhering to a standard fitness aesthetic. The ensemble presents a unified sporty look suitable for fitness activities.", {"yes","yes"}),
            ("The garment is solid black and features a half-zip closure at the front with an officer collar, providing a refined yet casual look. Its design is sleek and minimalistic, without any visible text or graphics, which emphasizes its versatility for various outfits. The pullover has a form-fitting silhouette, accentuated by elastic cuffs and waistband, enhancing its tailored appearance. It is breathable and can be styled as both a standalone piece, as seen in the first image, or layered under outerwear like the coat shown in the second image, demonstrating its functionality in diverse ensembles. The back view in the third image maintains the garment's clean lines and solid color, ensuring a consistent look all around.", {"yes","no"}),
            ("Tan, black, white\n\nThe Pier One Baskets montantes are tan with black and white accents. The shoes feature a high-top design, with a round toe and flat heel. They have a lacing closure for a snug fit. The style is streamlined and practical, with a lack of graphics or text, highlighting their versatile solid color. The outsole has a contrasting white color with a distinct black stripe, and the soles appear to have a grip pattern for traction. The overall design presents a sturdy and robust aesthetic suitable for casual wear.", {"yes","yes"}),
            ("Black\n\nThis ONLNEWKATY winter coat is black with a solid color pattern. It features a warm lined hood with removable faux fur trim, adding both function and an element of luxury. The coat closes with a zipper that may be concealed by a covering flap, offering an option between exposed and covered closure, added with a button placket for a stylish accent. The design includes practical elements like pockets on both sides, which enhance its utility. The coat's overall structure presents a sleek and clean outline that promises warmth and comfort without compromising on style. No visible graphics or text interrupt the simple elegance of the coat.",{"yes","no"}),
            ("Black\n\nThe PULL&BEAR FORMAL - Pantalon classique is a high-waisted, solid black pant that features a classic and elegant design. Its straight-leg cut creates a streamlined silhouette, while the zip fly closure ensures a secure and smooth fit. The side pockets offer a functional detail while maintaining the pant's sleek appearance. The absence of any visible graphics or text preserves its sophisticated and versatile style, making it suitable for formal occasions. The overall look is one of understated refinement.", {"yes","no"}),
            ("White, navy blue\n\nThese Lacoste POWERCOURT Baskets basses feature a clean, white-predominant design with accents of navy blue, notably at the heel which showcases a tri-color ribbon detail in red, white, and blue. The side of the shoe displays the iconic Lacoste crocodile logo in green with red. The flat heel shape and round toe cap contribute to a classic, sporty silhouette, while the lacing closure ensures a secure fit. Cutouts on the shoe's upper add a subtle textural variation, enhancing both aesthetics and breathability. The overall appearance is sleek and minimalist, with solid color blocking and a focus on understated style.", {"no","yes"}),
            ("Black, white, grey, orange, blue\n\nThe Jordan GFX SS CREW T-shirt features a classic black base color. Designed with a round neck, its short sleeves make it ideal for casual wear. The front is adorned with a small white, Jumpman logo on the chest, presenting a subtle branding element. The back of the shirt is more visually compelling, featuring a large, vivid print with bold lettering that reads \"FLY ABOVE,\" accompanied by an image of a basketball player in motion. This graphic is accented with gray and orange details, adding a dynamic and sporty touch to the overall design, with additional white text and logo enhancing its athletic appeal. The shirt's silhouette is traditional, with a relaxed fit that is common in sportswear and streetwear fashion.", {"yes","yes"}),
            ("navy\n\nThe Isaac Dewhirst BASIC PLAIN SUIT SLIM FIT is a sophisticated navy suit. Its blazer features a sleek lapel collar and a button closure, offering a tailored silhouette with its slim fit design. Pockets add a functional element, while shoulder pads give structure to the jacket's refined shape. The suit trousers also exhibit a slim fit, complementing the streamlined aesthetic of the suit, with no visible pattern or graphics disrupting the solid navy color. It radiates a classic and modern vibe suitable for various formal occasions.", {"no","no"}),
            ("""Olive green, black glitter.\n\nThe Vanessa Bruno Cabas tote features a sturdy olive-green canvas construction with sparkling black glitter trim. It has a practical and spacious open-top design, with an additional mobile phone compartment inside. Long handles allow for shoulder carrying, and the bottom panel provides a slight contrast in color, enhancing the bag's structure. It boasts a minimalist aesthetic with a dash of glamour, perfect for versatile daily use.""",{"no","no"}),
            ("This Polo Ralph Lauren long-sleeved, hooded sweatshirt features a full zipper closure at the front, providing a versatile opening. The solid color design imbues a clean and classic look, while the separate kangaroo pocket offers a convenient space for carrying essentials or keeping hands warm. The hood is equipped with a drawstring, allowing for adjustable coverage. The brand's iconic logo is subtly embroidered on the chest, adding a touch of distinction. With an elastic waist, this sweatshirt presents a snug and comfortable fit around the hips. The overall appearance is casual yet polished, embodying a relaxed, preppy style synonymous with the Ralph Lauren brand.\n", {"no","unknown"}),
            ("Navy, brown\n\nThis Polo Ralph Lauren Tote Unisex - Cabas features a deep navy blue canvas body contrasted with rich brown leather handles. On the front, there is an embroidered graphic of a bear dressed in a green jacket, sweater, and jeans, adding a playful and iconic touch. Below the bear, the brand's distinctive text logo is visible in white. The bag's simple rectangular structure and open-top design give it a casual yet classic tote silhouette, making it versatile for various occasions.", {"no","yes"}),
            ("Colors: bright pink\n\nThe Polo Ralph Lauren long-sleeve T-shirt presented is a bright pink garment. It features a classic round neck and a solid color design with no noticeable patterns. The clean, casual style is accentuated by a small, contrasting emblem on the left chest area. The T-shirt has a regular fit with a straight hemline and long sleeves, offering a comfortable yet refined appearance suitable for various casual settings.", {"no","yes"}),
            ("""Black, gold.\n\nThe images show a black leather handbag with a solid color design. Its quilted texture and structured shape give it an elegant and timeless look. The bag features a distinctive gold-tone circular closure on the front, adding a touch of sophistication. The top handle is complemented by a detachable chain strap, offering versatility in carrying options. The interior, as revealed in one of the images, appears to be spacious with a cotton lining and includes practical compartments for organization. There are no visible graphics or text, maintaining the handbag's sleek and polished aesthetic.""", {"yes","no"}),
            ("""White, orange, black\n\nThe Nike Sportswear COURT VINTAGE UNISEX - Baskets basses are predominantly white with subtle orange and black accents. These low-top sneakers feature a classic round toe and a flat heel, suitable for tennis. The closure is achieved with white laces. The side display perforations and cutouts contribute to the shoe’s breathability and design detail. A signature swoosh logo is visible on the shoe's side in a contrasting black with an orange outline. On the tongue and heel tab, branding completes the look, with a small orange swoosh and text against a black label. The outsole is white, maintaining a monochromatic base for an overall minimalist and retro aesthetic.""", {"yes","yes"}),
            ("""The images depict a pair of Even&Odd Wide Fit Bottines in a solid black color. These ankle boots have a round toe design and feature a chunky block heel with a platform sole. The rugged outsole enhances its bold silhouette. The boots are of slip-on style, utilizing elastic straps on the sides for ease of fitting, along with pull-loops at the back to assist in wearing them. They are detailed with rivets, likely contributing to both the aesthetic and structure of the boots. The design is sleek and utilitarian, leaning towards a modern and edgy fashion statement. There are no visible graphics or text on the boots.""",  {"yes","no"})
        ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                result = classify_garment_type(description)
                #self.assertEqual(result, expected)
                self.assertTrue(result in self.corresponding_embedding[expected])
    
if __name__ == '__main__':
    unittest.main()
