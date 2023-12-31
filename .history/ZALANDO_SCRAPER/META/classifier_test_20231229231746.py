import unittest
from ZALANDO_SCRAPER.META.metadata_generator import * # Replace 'your_module' with the actual module name

# run py -m ZALANDO_SCRAPER.META.classifier_test    at root
def classify_othercolor(description):
    api_client = OpenAIClient()  # Assuming this sets up the API client correctly
    classifier = OtherColorClassifier(api_client)
    return classifier.classify(description)

def classify_type(description):
    api_client = OpenAIClient()  # Assuming this sets up the API client correctly
    classifier = GarmentTypeClassifier(api_client)
    return classifier.classify(description)

def classify_composition(description):
    api_client = OpenAIClient()  # Assuming this sets up the API client correctly
    classifier = CompositionClassifier(api_client)
    return classifier.classify(description)

class TestClassification(unittest.TestCase):
    def test_otherColor_classification(self):
        test_cases = [("Khaki\n\nThis pair of Jack & Jones Chino pants exhibits a solid khaki color. They are designed with a sleek and modern fit that appears to be neither too tight nor too loose, ensuring versatility for various occasions. The chinos feature a classic button and zip closure, with belt loops around the waist for accessorizing with a belt. There are side pockets at the hips and additional welt pockets at the back, which are typical characteristics of chino-style trousers. The hem of the pants is neatly finished, and the fabric lays smoothly over the shoes, showcasing a clean and casual look. There is no visible graphics or text on these pants; they maintain a simple yet sophisticated aesthetics.","yes"),
                      ("The DeFacto Slim Fit Pullover is presented in a solid burgundy color. It features a minimalistic, clean design with a high, close-fitting turtleneck that provides both warmth and style. The pullover has a body-hugging slim fit cut that accentuates the body shape, and it appears to have long sleeves with ribbed cuffs. Similarly, the bottom hem of the pullover is also ribbed, promoting a snug fit with added elasticity around the waist. There are no visible graphics, patterns, or text on the garment; its aesthetic is defined by its sleek and straightforward appearance. Overall, the garment exudes a sophisticated and contemporary vibe suitable for various casual and semi-formal occasions.","yes"),
                      ("White, black\n\nThe Lacoste T-CLIP - Baskets basses are a classic low-cut sneaker design featuring a harmonious blend of white and black colors. The upper includes black leather accents strategically placed at the toe, lace guard, and heel, combined with large white panels on the sides and top, creating a refined contrast. A prominent, stylized crocodile logo is featured on the side, typical of the brand's iconic branding. The shoe has a round toe shape and utilizes lacing for closure, providing a secure and adjustable fit. The sole shows a streamlined black and white profile that complements the upper's color palette, and additional branding appears on the heel where the brand's name is displayed in black lettering on a white patch.","no"),
                      ("Tan, dark blue, white, gray, yellow.\n\nThe Timberland SPRINT TREKKER boots feature a tan nubuck/textile upper with a dark blue padded collar. The outsole is a contrasting white with gray accents. Yellow lacing adds a pop of color, secured by metal hooks that ensure durability and ease of fastening. The design includes a round toe cap and a flat heel shape, catering to both comfort and functionality. The prominent Timberland logo is visible on the side of the heel counter and on the tongue, giving it a recognizable brand identity. The boots convey a rugged yet stylish aesthetic, suitable for outdoor activities as well as casual wear.","yes"),
                      ("Beige, Heather\n\nThe Stradivarius SOFT-TOUCH Manteau classique is a long beige coat with a heather pattern. It features a structured design with a prominent lapel collar and a double-breasted front closure accented by buttons. The coat is tailored with flap pockets, adding practicality to its elegant appearance. The entirety of the garment showcases a minimalist and sophisticated style typical of classic outerwear, exuding an air of timeless fashion. There are no visible graphics or text on the coat, emphasizing its clean and chic aesthetic.","yes"),
                      ("Black\n\nThe Claudie Pierlot cape is a chic, black outerwear piece with a solid color pattern. It features elegant, minimalistic design elements consistent with a refined aesthetic. The cape has a turtleneck collar and an unlined construction, providing a sleek, flowy silhouette. The front view reveals a single visible fastening at the neck, which creates a clean line down the front, and the hem reaches approximately mid-thigh or knee length, depending on the wearer's height. Overall, the cape has a structured yet relaxed appearance, exuding effortless style. There are no visible graphics or text.","no"),
                      ("White, black, gold\n\nThe Puma CAVEN UNISEX - Baskets basses are low-top sneakers with a predominantly white upper featuring black and gold accents. The side showcases a signature Puma formstrip in black, while the branding includes a gold Puma logo on the tongue and additional gold text along the laces. They have a round shoe toe, a flat heel shape, and are closed by lacing over a flower-like toe design. The outsole appears to be a textured abrasion-resistant rubber for durability and grip. These sneakers exude a classic, sporty aesthetic that is versatile for various styles and occasions.","yes"),
                      ("Color: Black\n\nThe PULL&BEAR MOM jeans present a classic black color with a solid pattern, crafted from denim. These high-waisted jeans feature a tapered fit that gives a snug silhouette while still offering room through the hip and thigh. The closure is a traditional zip fly with a button on top. The jeans have five pockets: two in the back, two in the front with a smaller coin pocket inset in the right front pocket. They demonstrate a minimalist design with no visible graphics or text, focusing on a sleek and straightforward aesthetic suitable for versatile styling. The images show the jeans as a foundational piece that could be easily integrated into various outfits.","no"),
                      ("The Pier One Pullover features a color block design with shades of black, gray, and white. It incorporates a heathered pattern throughout, which gives it a textured appearance. The round collar is subtly outlined with a ribbed, solid black trim, offering a clean finish. Its cuffs and hem also have ribbed detailing for a snug fit, emphasizing the pullover's casual yet stylish look. There are no visible graphics or text on the garment. Overall, it presents a contemporary and versatile style suitable for various casual looks.","yes"),
                      ("Black\n\nThe Even&Odd cropped jumper is a solid black pullover featuring a ribbed texture. It has a round collar and a cropped silhouette that creates a contemporary and easy-to-style piece. Its design includes long sleeves that contribute to a relaxed, slightly oversized look, suitable for casual wear. There are no graphics or text visible, emphasizing its minimalist and versatile appeal.","no")
                        ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                print("for "+description[:20])
                
                result = classify_othercolor(description)
                print("actual answer is :"+result)
                print("expected = "+expected)
                print()
                self.assertEqual(result, expected)


    def test_type_classification(self):
        test_cases = [
            ("A short-sleeved cotton t-shirt.", "Tops"),
            ("Denim jeans with a straight fit.", "Bottoms"),
            ("A waterproof hooded jacket.", "Outerwear"),
            ("Silk boxers with an elastic waistband.", "Underwear"),
            ("Running shoes with cushioned soles.", "Footwear"),
            ("A leather belt with a metal buckle.", "Accessories"),
            ("A jumpsuit with a zippered front.", "One-Pieces"),
            ("An item that does not fit into any category.", "unknown"),
            ("ORIGINAL TEE - T-shirt basique, Heather grey, white\n\nThe Tommy Jeans ORIGINAL TEE - T-shirt basique is a classic heather grey with a small, white logo embroidery on the left chest area, adding a subtle touch of branding. It features a round collar and short sleeves, providing a casual yet stylish look. The jersey fabric ensures a comfortable fit and breathability. Its versatile design makes it suitable for a range of occasions and easy to pair with various bottoms and shoes.", "Tops"),
            ("CORE BOOT - Derbies, brown\n\nThe Tommy Hilfiger CORE BOOT Derbies are brown suede boots featuring a round toe and block heel, giving them a classic and robust appearance. They have a lacing closure system with round, dark brown laces that complement the shoe's overall color. The boots exhibit a solid color design, maintaining simplicity and elegance. A distinctive feature is the subtle presence of a brand logo, which adds a touch of designer prestige while retaining the shoe's understated aesthetics. The synthetic outsole shows a thin, red stripe that subtly contrasts with the brown suede, enhancing the visual appeal of the boots. Overall, the design is clean and timeless, suitable for both casual and more dressed-up occasions.", "Footwear"),
            ("PREMIUM ESSENTIAL 3 PACK - Shorty, The garment is navy blue. It is a pair of men's boxer brief shorts with a snug fit and a short leg design, promoting a modern silhouette. The waistband is elastic and prominently features the Tommy Hilfiger brand with the name written in white on a red stripe above a white stripe, which adds a striking contrast to the solid navy blue body of the garment. There are no visible seams on the shorts, indicating a seamless design that probably enhances comfort. The fit appears normal, adhering closely to the body without being overly tight. There is no visible pattern or additional graphics besides the brand name on the waistband.", "Underwear"),
            ("Chemise, White\n\nThe showcased Pier One Chemise is a classic men's long-sleeved shirt in a bright white hue. It features a Kent collar and a front button closure, providing a clean and traditional look. The shirt's design is elegant and simple with no visible graphics or text, emphasizing its solid color and creating a pristine, professional appearance. It has a light transparency level, which contributes to its breathability and comfort. The shirt's tailored fit and lightweight fabric make it suitable for both formal and casual settings. The garment's environmental characteristics are not visible in the images.", "Tops"),
            ("574 UNISEX - Baskets basses, Navy blue, beige, white.\n\nThe New Balance 574 UNISEX sneakers feature a classic low-top design. The upper is predominantly navy blue, contrasted by a large, beige 'N' logo on the side and matching beige accents on the heel and outsole tread. The round shoe toe maintains a traditional and versatile look, while the flat heel ensures a stable, everyday wear. Its lacing closure promises a secure fit. The design encapsulates a timeless athletic aesthetic with a breathable upper, highlighted by tonal stitching and additional brand detailing on the tongue and heel in white text. The outsole is a light tan, complementing the overall color scheme.", "Footwear"),
            ("2 PACK - Legging, Black\n\nThe leggings displayed in the images are solid black in color and designed for maternity wear. They exhibit a high-waisted style, ensuring a comfortable fit for expecting mothers. The leggings feature an elastic waistband that provides an adjustable and secure fit. Owing to the high cotton content, the leggings likely offer a soft and breathable experience. The jersey material ensures added stretch and flexibility, courtesy of the elastane, which complements the body changes during pregnancy. The images do not show any visible graphics, prints, or text, highlighting the leggings' versatile and straightforward design. The overall appearance suggests practicality with a focus on comfort and adaptability for daily wear.", "Bottoms"),
            ("Survêtement, The adidas Sportswear Survêtement is predominantly black. The design is sleek and contemporary, maintaining a solid color theme with the brand's signature three stripes in white running down the sides of the sleeves and pants for a subtle contrast. It features a trucker-style collar on the zip-up jacket for a semi-formal touch and ribbed, elastic cuffs for comfort and fit. The jacket showcases a small, white adidas logo on the right chest, while the pants repeat the logo on the left thigh. The waist of the pants is elasticized for a custom fit, and both the jacket and pants are equipped with side pockets for functionality, adhering to a standard fitness aesthetic. The ensemble presents a unified sporty look suitable for fitness activities.", "Other"),
            ("EEMIL HALF ZIP NOOS - Pullover, The garment is solid black and features a half-zip closure at the front with an officer collar, providing a refined yet casual look. Its design is sleek and minimalistic, without any visible text or graphics, which emphasizes its versatility for various outfits. The pullover has a form-fitting silhouette, accentuated by elastic cuffs and waistband, enhancing its tailored appearance. It is breathable and can be styled as both a standalone piece, as seen in the first image, or layered under outerwear like the coat shown in the second image, demonstrating its functionality in diverse ensembles. The back view in the third image maintains the garment's clean lines and solid color, ensuring a consistent look all around.", "Tops"),
            ("Baskets montantes, Tan, black, white\n\nThe Pier One Baskets montantes are tan with black and white accents. The shoes feature a high-top design, with a round toe and flat heel. They have a lacing closure for a snug fit. The style is streamlined and practical, with a lack of graphics or text, highlighting their versatile solid color. The outsole has a contrasting white color with a distinct black stripe, and the soles appear to have a grip pattern for traction. The overall design presents a sturdy and robust aesthetic suitable for casual wear.", "Footwear"),
            ("ONLNEWKATY - Manteau d'hiver, Black\n\nThis ONLNEWKATY winter coat is black with a solid color pattern. It features a warm lined hood with removable faux fur trim, adding both function and an element of luxury. The coat closes with a zipper that may be concealed by a covering flap, offering an option between exposed and covered closure, added with a button placket for a stylish accent. The design includes practical elements like pockets on both sides, which enhance its utility. The coat's overall structure presents a sleek and clean outline that promises warmth and comfort without compromising on style. No visible graphics or text interrupt the simple elegance of the coat.", "Outerwear"),
            ("Black\n\nThe PULL&BEAR FORMAL - Pantalon classique is a high-waisted, solid black pant that features a classic and elegant design. Its straight-leg cut creates a streamlined silhouette, while the zip fly closure ensures a secure and smooth fit. The side pockets offer a functional detail while maintaining the pant's sleek appearance. The absence of any visible graphics or text preserves its sophisticated and versatile style, making it suitable for formal occasions. The overall look is one of understated refinement.", "Bottoms"),
            ("POWERCOURT - Baskets basses, White, navy blue\n\nThese Lacoste POWERCOURT Baskets basses feature a clean, white-predominant design with accents of navy blue, notably at the heel which showcases a tri-color ribbon detail in red, white, and blue. The side of the shoe displays the iconic Lacoste crocodile logo in green with red. The flat heel shape and round toe cap contribute to a classic, sporty silhouette, while the lacing closure ensures a secure fit. Cutouts on the shoe's upper add a subtle textural variation, enhancing both aesthetics and breathability. The overall appearance is sleek and minimalist, with solid color blocking and a focus on understated style.", "Footwear"),
            ("Black, white, grey, orange, blue\n\nThe Jordan GFX SS CREW T-shirt features a classic black base color. Designed with a round neck, its short sleeves make it ideal for casual wear. The front is adorned with a small white, Jumpman logo on the chest, presenting a subtle branding element. The back of the shirt is more visually compelling, featuring a large, vivid print with bold lettering that reads \"FLY ABOVE,\" accompanied by an image of a basketball player in motion. This graphic is accented with gray and orange details, adding a dynamic and sporty touch to the overall design, with additional white text and logo enhancing its athletic appeal. The shirt's silhouette is traditional, with a relaxed fit that is common in sportswear and streetwear fashion.", "Tops"),
            ("BASIC PLAIN SUIT SLIM FIT - Costume, navy\n\nThe Isaac Dewhirst BASIC PLAIN SUIT SLIM FIT is a sophisticated navy suit. Its blazer features a sleek lapel collar and a button closure, offering a tailored silhouette with its slim fit design. Pockets add a functional element, while shoulder pads give structure to the jacket's refined shape. The suit trousers also exhibit a slim fit, complementing the streamlined aesthetic of the suit, with no visible pattern or graphics disrupting the solid navy color. It radiates a classic and modern vibe suitable for various formal occasions.", "Other"),
            ("""Olive green, black glitter.\n\nThe Vanessa Bruno Cabas tote features a sturdy olive-green canvas construction with sparkling black glitter trim. It has a practical and spacious open-top design, with an additional mobile phone compartment inside. Long handles allow for shoulder carrying, and the bottom panel provides a slight contrast in color, enhancing the bag's structure. It boasts a minimalist aesthetic with a dash of glamour, perfect for versatile daily use.""","Accessories"),
            ("""Black, gold.\n\nThe images show a black leather handbag with a solid color design. Its quilted texture and structured shape give it an elegant and timeless look. The bag features a distinctive gold-tone circular closure on the front, adding a touch of sophistication. The top handle is complemented by a detachable chain strap, offering versatility in carrying options. The interior, as revealed in one of the images, appears to be spacious with a cotton lining and includes practical compartments for organization. There are no visible graphics or text, maintaining the handbag's sleek and polished aesthetic.""", "Accessories"),
            ("An item that does not fit into any category.", "unknown"),
            ("Heather grey, white\n\nThe Tommy Jeans ORIGINAL TEE - T-shirt basique is a classic heather grey with a small, white logo embroidery on the left chest area, adding a subtle touch of branding. It features a round collar and short sleeves, providing a casual yet stylish look. The jersey fabric ensures a comfortable fit and breathability. Its versatile design makes it suitable for a range of occasions and easy to pair with various bottoms and shoes.", "Tops"),
            ("CORE BOOT - Derbies, brown\n\nThe Tommy Hilfiger CORE BOOT Derbies are brown suede boots featuring a round toe and block heel, giving them a classic and robust appearance. They have a lacing closure system with round, dark brown laces that complement the shoe's overall color. The boots exhibit a solid color design, maintaining simplicity and elegance. A distinctive feature is the subtle presence of a brand logo, which adds a touch of designer prestige while retaining the shoe's understated aesthetics. The synthetic outsole shows a thin, red stripe that subtly contrasts with the brown suede, enhancing the visual appeal of the boots. Overall, the design is clean and timeless, suitable for both casual and more dressed-up occasions.", "Footwear"),
            ("PREMIUM ESSENTIAL 3 PACK - Shorty, The garment is navy blue. It is a pair of men's boxer brief shorts with a snug fit and a short leg design, promoting a modern silhouette. The waistband is elastic and prominently features the Tommy Hilfiger brand with the name written in white on a red stripe above a white stripe, which adds a striking contrast to the solid navy blue body of the garment. There are no visible seams on the shorts, indicating a seamless design that probably enhances comfort. The fit appears normal, adhering closely to the body without being overly tight. There is no visible pattern or additional graphics besides the brand name on the waistband.", "Underwear"),
            ("Chemise, White\n\nThe showcased Pier One Chemise is a classic men's long-sleeved shirt in a bright white hue. It features a Kent collar and a front button closure, providing a clean and traditional look. The shirt's design is elegant and simple with no visible graphics or text, emphasizing its solid color and creating a pristine, professional appearance. It has a light transparency level, which contributes to its breathability and comfort. The shirt's tailored fit and lightweight fabric make it suitable for both formal and casual settings. The garment's environmental characteristics are not visible in the images.", "Tops"),
            ("574 UNISEX - Baskets basses, Navy blue, beige, white.\n\nThe New Balance 574 UNISEX sneakers feature a classic low-top design. The upper is predominantly navy blue, contrasted by a large, beige 'N' logo on the side and matching beige accents on the heel and outsole tread. The round shoe toe maintains a traditional and versatile look, while the flat heel ensures a stable, everyday wear. Its lacing closure promises a secure fit. The design encapsulates a timeless athletic aesthetic with a breathable upper, highlighted by tonal stitching and additional brand detailing on the tongue and heel in white text. The outsole is a light tan, complementing the overall color scheme.", "Footwear"),
            ("2 PACK - Legging, Black\n\nThe leggings displayed in the images are solid black in color and designed for maternity wear. They exhibit a high-waisted style, ensuring a comfortable fit for expecting mothers. The leggings feature an elastic waistband that provides an adjustable and secure fit. Owing to the high cotton content, the leggings likely offer a soft and breathable experience. The jersey material ensures added stretch and flexibility, courtesy of the elastane, which complements the body changes during pregnancy. The images do not show any visible graphics, prints, or text, highlighting the leggings' versatile and straightforward design. The overall appearance suggests practicality with a focus on comfort and adaptability for daily wear.", "Bottoms"),
            ("Survêtement, The adidas Sportswear Survêtement is predominantly black. The design is sleek and contemporary, maintaining a solid color theme with the brand's signature three stripes in white running down the sides of the sleeves and pants for a subtle contrast. It features a trucker-style collar on the zip-up jacket for a semi-formal touch and ribbed, elastic cuffs for comfort and fit. The jacket showcases a small, white adidas logo on the right chest, while the pants repeat the logo on the left thigh. The waist of the pants is elasticized for a custom fit, and both the jacket and pants are equipped with side pockets for functionality, adhering to a standard fitness aesthetic. The ensemble presents a unified sporty look suitable for fitness activities.", "Other"),
            ("EEMIL HALF ZIP NOOS - Pullover, The garment is solid black and features a half-zip closure at the front with an officer collar, providing a refined yet casual look. Its design is sleek and minimalistic, without any visible text or graphics, which emphasizes its versatility for various outfits. The pullover has a form-fitting silhouette, accentuated by elastic cuffs and waistband, enhancing its tailored appearance. It is breathable and can be styled as both a standalone piece, as seen in the first image, or layered under outerwear like the coat shown in the second image, demonstrating its functionality in diverse ensembles. The back view in the third image maintains the garment's clean lines and solid color, ensuring a consistent look all around.", "Tops"),
            ("Baskets montantes, Tan, black, white\n\nThe Pier One Baskets montantes are tan with black and white accents. The shoes feature a high-top design, with a round toe and flat heel. They have a lacing closure for a snug fit. The style is streamlined and practical, with a lack of graphics or text, highlighting their versatile solid color. The outsole has a contrasting white color with a distinct black stripe, and the soles appear to have a grip pattern for traction. The overall design presents a sturdy and robust aesthetic suitable for casual wear.", "Footwear"),
            ("ONLNEWKATY - Manteau d'hiver, Black\n\nThis ONLNEWKATY winter coat is black with a solid color pattern. It features a warm lined hood with removable faux fur trim, adding both function and an element of luxury. The coat closes with a zipper that may be concealed by a covering flap, offering an option between exposed and covered closure, added with a button placket for a stylish accent. The design includes practical elements like pockets on both sides, which enhance its utility. The coat's overall structure presents a sleek and clean outline that promises warmth and comfort without compromising on style. No visible graphics or text interrupt the simple elegance of the coat.", "Outerwear"),
            ("Black\n\nThe PULL&BEAR FORMAL - Pantalon classique is a high-waisted, solid black pant that features a classic and elegant design. Its straight-leg cut creates a streamlined silhouette, while the zip fly closure ensures a secure and smooth fit. The side pockets offer a functional detail while maintaining the pant's sleek appearance. The absence of any visible graphics or text preserves its sophisticated and versatile style, making it suitable for formal occasions. The overall look is one of understated refinement.", "Bottoms"),
            ("POWERCOURT - Baskets basses, White, navy blue\n\nThese Lacoste POWERCOURT Baskets basses feature a clean, white-predominant design with accents of navy blue, notably at the heel which showcases a tri-color ribbon detail in red, white, and blue. The side of the shoe displays the iconic Lacoste crocodile logo in green with red. The flat heel shape and round toe cap contribute to a classic, sporty silhouette, while the lacing closure ensures a secure fit. Cutouts on the shoe's upper add a subtle textural variation, enhancing both aesthetics and breathability. The overall appearance is sleek and minimalist, with solid color blocking and a focus on understated style.", "Footwear"),
            ("""White, orange, black\n\nThe Nike Sportswear COURT VINTAGE UNISEX - Baskets basses are predominantly white with subtle orange and black accents. These low-top sneakers feature a classic round toe and a flat heel, suitable for tennis. The closure is achieved with white laces. The side display perforations and cutouts contribute to the shoe’s breathability and design detail. A signature swoosh logo is visible on the shoe's side in a contrasting black with an orange outline. On the tongue and heel tab, branding completes the look, with a small orange swoosh and text against a black label. The outsole is white, maintaining a monochromatic base for an overall minimalist and retro aesthetic.""", "Footwear"),
            ("""The images depict a pair of Even&Odd Wide Fit Bottines in a solid black color. These ankle boots have a round toe design and feature a chunky block heel with a platform sole. The rugged outsole enhances its bold silhouette. The boots are of slip-on style, utilizing elastic straps on the sides for ease of fitting, along with pull-loops at the back to assist in wearing them. They are detailed with rivets, likely contributing to both the aesthetic and structure of the boots. The design is sleek and utilitarian, leaning towards a modern and edgy fashion statement. There are no visible graphics or text on the boots.""", "Footwear")
        ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                
                
                result = classify_type(description)
                if( expected not in {"Other","unknown"}):
                    if(result != expected):
                        print("for "+description[:60])
                        print("actual answer is :"+result)
                        print("expected = "+expected)
                        print()
                    self.assertTrue( result==expected or result =="Other")

    def test_composition_classification(self):
        test_cases = [
            ("Composition: 95% cotton, 5% elastane, Sleeve composition: 95% cotton, 5% elastane, Material: Ribbed", {"natural", "synthetic"}),
            ("Composition: 51% cotton, 49% polyester, Material: Sweat", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Jersey, Care instructions: Do not tumble dry, machine wash at 30°C, do not bleach", {"natural"}),
            ("Composition: 96% polyester, 4% polyurethane, Lining: 100% polyester, Care instructions: Do not tumble dry, dry clean, do not wash, do not iron", {"synthetic"}),
            ("Composition: 95% cotton, 5% elastane, Material: Jersey, Care instructions: Do not tumble dry, machine wash at 30°C, wash delicate fabrics", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Back composition: 100% cotton, Material: Denim", {"natural"}),
            ("Composition: 100% cotton, Material: Jersey, Care instructions: Do not tumble dry, wash delicate fabrics, machine wash at 30°C ", {"natural"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C, do not tumble dry, wash delicate fabrics", {"natural"}),
            ("Composition: 60% cotton, 20% nylon, 20% viscose, Material: Knit / mesh, Care instructions: Machine wash at 40°C, do not tumble dry, wash on delicate fabrics", {"natural", "synthetic","artificial"}),
            ("Composition: 98% cotton, 2% elastane, Material: Canvas, Care instructions: Machine wash at 30°C", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C", {"natural"}),
            ("Composition: 90% polyester, 10% elastane", {"synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C, do not tumble dry, wash delicate fabrics", {"natural"}),
            ("Composition: 60% cotton, 20% nylon, 20% viscose, Material: Knit / mesh, Care instructions: Machine wash at 40°C, do not tumble dry, wash on delicate fabrics", {"natural", "synthetic","artificial"}),
            ("Composition: 98% cotton, 2% elastane, Material: Canvas, Care instructions: Machine wash at 30°C", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C", {"natural"}),
            ("Composition: 90% polyester, 10% elastane", {"synthetic"}),
            ("Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather", {"synthetic"}),
            ("Composition: 70% cotton, 30% polyester, Material: Sweatshirt, Care instructions: Machine wash at 30°C, do not iron", {"natural","synthetic"}),
            ("Upper / Upper: Leather and textile, Lining: Imitation leather / textile, Insole: Imitation leather, Outsole: Synthetic material, Lining thickness: Lining to protect against the cold, Care instructions: Apply a waterproofer before first use ", {"natural","synthetic"}),
            ("Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather", {"synthetic"}),
            ("Composition: 100% polyester, Back composition: 100% polyester, Lower part composition: 100% polyester, Yoke composition: 100% polyester, Lining: 100% polyester", {"synthetic"}),
            ("Composition: 100% polyester, Material: Jersey, Technologies: Dri-Fit (Nike), Care instructions: Do not tumble dry, machine wash at 30°C ", {"synthetic"}),
            ("Composition: 70% cotton, 30% polyester, Material: Sweatshirt, Care instructions: Machine wash at 30°C, do not iron", {"natural","synthetic"}),
            ("Upper / Upper: Leather and textile, Lining: Imitation leather / textile, Insole: Imitation leather, Outsole: Synthetic material, Lining thickness: Lining to protect against the cold, Care instructions: Apply a waterproofer before first use ", {"natural","synthetic"}),
            ("Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather", {"synthetic"}),
            ("Composition: 100% polyester, Back composition: 100% polyester, Lower part composition: 100% polyester, Yoke composition: 100% polyester, Lining: 100% polyester", {"synthetic"}),
            ("Composition: 100% polyester, Material: Jersey, Technologies: Dri-Fit (Nike), Care instructions: Do not tumble dry, machine wash at 30°C ", {"synthetic"}),
            ("Composition: 55% nylon, 45% polyester, Padding material: 100% polyester, Lining: 100% polyester " , {"synthetic"}),
            ("Composition: 37% wool, 34% polyester, 29% polyamide, Lining thickness: Unlined, Material: Knit / mesh, Contains non-textile elements of animal origin: No ", {"natural", "synthetic"}),
            ]
        for description, expected in test_cases:
            with self.subTest(description=description):
                result = classify_composition(description)
                if(not(result==expected)):
                    print("for "+description[:40])
                    print("actual  :" )
                    print(result)
                    print("expected : ")
                    print(expected)
                self.assertTrue(result==expected)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestClassification('test_composition_classification'))
    runner = unittest.TextTestRunner()
    runner.run(suite)