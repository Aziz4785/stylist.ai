import openai
import sys
import os
import json
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
openai.api_key = config.OPENAI_API_KEY
script_dir = os.path.dirname(os.path.abspath(__file__))
baseline_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'baseline_data6.json')



def extract_composition(txt):
    categories = ["synthetic", "natural", "artificial"]
    res = set()
    # Check if any of the keywords are in the text
    for category in categories:
        if category in txt:
            res.add(category)

    # Return "unknown" if no matching category is found
    return res

def extract_garment_type(txt):
    # THIS FUNCTION IS DUPLICATED IN SERVER UTIL
    categories = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces","Other","unknown"]

    # Check if any of the keywords are in the text
    for category in categories:
        if category in txt:
            return category

    # Return "unknown" if no matching category is found
    return "unknown"
def classify_garment_type(description):
    """
    this function is duplicated in server
    Classify the type of a garment based on its text description.
    """

    prompt = f"Based on the following description, determine the garment type: Tops, Bottoms, Outerwear, Underwear, Footwear, Accessories, One-Pieces, Other, or unknown. If the garment type (or any specific garment-related terms) are not explicitly mentioned in the description, respond with 'unknown'.\n\nDescription: {description}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your primary task is to categorize garments strictly based on their description. Only if a garment type (or any specific garment-related terms) are explicitly mentioned in the description, identify its category. For any description that does not explicitly state the garment type, you must classify it as 'unknown', regardless of any implied or suggestive details in the description."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60
    )
    # Extract and return the garment type from the response
    garment_type = extract_garment_type(response.choices[0].message['content'])

    # Validate the garment type to ensure it's one of the predefined types
    valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "Other", "One-Pieces", "unknown"]
    return garment_type if garment_type in valid_types else "unknown"

def add_type_to_json(json_file_path):
    with open(json_file_path, 'r' , encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        if "visual description" in item:
            item['type'] = classify_garment_type(item["visual description"])

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_composition_to_json(json_file_path):
    with open(json_file_path, 'r' , encoding='utf-8') as file:
        data = json.load(file)

    i = 0
    for item in data:
        i+=1
        if "details about that item" in item:
            details = item["details about that item"]
            details_parts = details.split('\n')
            if(len(details_parts)>=2):
                part1 = details_parts[0].strip()
                item['composition'] = ', '.join(classify_materials(part1))
        if(i%12 ==0):
            print(i)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def remove_artificial_fabric(text):
    words_to_replace = ["viscose", "acetate", "rayon", "Viscose", "Acetate", "Rayon"]
    found = False
    new_text = text

    for word in words_to_replace:
        if word in new_text:
            found = True
            new_text = new_text.replace(word, "unknown")

    return found, new_text

def classify_materials(description):

    # prompt_template = """I am an AI trained to categorize fabrics in garment descriptions into four categories: natural, synthetic, artificial, and unknown. Natural fabrics are those like cotton or wool. Synthetic fabrics include materials like polyester or elastane. Artificial fabrics are specifically viscose, acetate, or rayon. If I am unsure about the category of a fabric, I will classify it as unknown. I will list all the categories present in a given garment description.

    #         I will don't consider a material "articifial" if viscose, acetate, or rayon are not explicitly written.

    #         Examples:
    #         - Description: "Composition: 60% cotton, 20% nylon, 20% viscose, Material: Knit / mesh"
    #         Categories: "natural", "synthetic", "artificial"
    #         - Description: "Composition: 98% cotton, 2% elastane, Material: Canvas"
    #         Categories: "natural", "synthetic"
    #         - Description: "Composition: 100% cotton, Material: Piqué"
    #         Categories: "natural"

    #         Now, analyze the following garment description and categorize the fabrics:

    #         {description}"""
    res = set()
    contain_artificial, description = remove_artificial_fabric(description)
    if contain_artificial:
        res.add("artificial")

    prompt_without_aritifical = """I am an AI trained to categorize fabrics in garment descriptions into three categories: natural, synthetic, and unknown. Natural fabrics are those like cotton, linen, hemp, jute, wool or silk. Synthetic fabrics include materials like nylon, polyester, polyamide, acrylic or elastane. If I am unsure about the category of a fabric, I will classify it as unknown. I will list all the categories present in a given garment description.
            Examples:
            - Description: "Composition: 60% cotton, 20% nylon, 20% unknown, Material: Knit / mesh"
            Categories: "natural", "synthetic", "unknown"
            - Description: "Composition: 98% cotton, 2% elastane, Material: Canvas"
            Categories: "natural", "synthetic"
            - Description: "Composition: 100% cotton, Material: Piqué"
            Categories: "natural"

            Now, analyze the following garment description and categorize the fabrics:

            {description}"""
    prompt2 = prompt_without_aritifical.format(description=description)
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        #prompt="""You are a helpful assistant. Analyze descriptions of clothing materials and classify each component of the material as 'natural', 'synthetic', 'artificial', or 'unknown'. Pay particular attention to mixed materials. For example, a fabric containing both cotton (a natural material) and elastane (a synthetic material) should be classified as both 'natural' and 'synthetic'. Your response must strictly follow the format: 'composition_in: <type_1>, <type_2>, ...,<type_n> ;'. For instance, respond with 'composition_in: natural, synthetic;' for a material that is 95% cotton and 5% elastane. Examples for classification: natural materials include cotton, linen, hemp, jute, wool, silk; synthetic materials include nylon, polyester, polyamide, acrylic, elastane, and explicitly imitation leather. Don't classify a material as "artificial" if it is not one of these : (viscose, acetate, rayon) (one of those materials should be explicitly written !! otherwise classify it as "unknown"). A material is considered 'artificial' only if it's viscose, acetate, rayon. If the material composition is not indicated or is unclear, classify it as 'unknown'. Always adhere to the specified response format. If you are not sure about the category of a given material, put unknown and always adhere to the specified response format. \n\nMaterial Description: """ + description,
        prompt = prompt2,
        max_tokens=60,
        temperature=0.6,
        )
 
    # response = openai.Completion.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt="""Carefully categorize each material listed in the clothing item's composition as 'natural', 'synthetic', 'artificial',  or 'unknown'. If a material does not clearly fit into these categories or if there is any uncertainty, categorize it as 'unknown'. Follow these guidelines:

    #     - natural: Derived from vegetable or animal products. Examples: cotton, linen, hemp, jute, wool, silk.
    #     - synthetic: Produced by chemical synthesis (polymerization). Examples: nylon, polyester, polyamide, acrylic, elastane.
    #     - artificial: Derived from natural materials (cellulose, vegetable proteins) and chemically transformed. The only know articial fibers are : viscose, acetate, rayon.

    #     # Don't classify a material as "artificial" if it is not one of these : (viscose, acetate, rayon)
    #     Pay close attention to each material, even in mixed compositions. If a material categorization is not clear, mark it as 'unknown'. Provide a precise categorization for each material.
    #     Keep the answer short

    #     Clothing details: """ + description,
    #     max_tokens=60,
    #     temperature=0.6,
    # )
    
    print("raw result from gpt : ")
    print(response.choices[0].text.lower().strip())

    
    return res.union(extract_composition(response.choices[0].text.lower().strip()))


if __name__ == '__main__':
    print("modifiying baseline ...")
    #add_type_to_json("../MAIN_DATA/baseline_data6.json")
    add_composition_to_json("../MAIN_DATA/baseline_data6.json")
    #description = "Composition: 82% cotton, 18% polyester, Material: Fleece, Care instructions: Machine wash at 30°C"
    # description = "Composition: 100% polyurethane, Padding material: 100% polyester, Lining: 100% polyester, Lining thickness: Warm lining "
    # result = classify_materials(description)
    # print(result)