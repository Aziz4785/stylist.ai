import openai
import sys
import os
from openai import OpenAI
import json
import re
from metadata_generator_util import *
from abc import ABC, abstractmethod
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
script_dir = os.path.dirname(os.path.abspath(__file__))
baseline_path = os.path.join(script_dir, '..',  'MAIN_DATA', 'baseline_data6.json')

class Config:
    @staticmethod
    def get_api_key():
        return config.OPENAI_API_KEY

class OpenAIClient:
    def __init__(self):
        self.api_key = Config.get_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)

    def query(self, prompt, model="gpt-3.5-turbo", max_tokens=60):
        return self.client.Completion.create(model=model, prompt=prompt, max_tokens=max_tokens)

    def chat_query(self, messages, model="gpt-3.5-turbo", max_tokens=60):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
    
class ClassifierService(ABC):
    @abstractmethod
    def classify(self, text):
        pass

class GarmentTypeClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
        """
        Classify the type of a garment based on its text description.
        """

        prompt_template = f"Based on the following description, determine the garment type: Tops, Bottoms, Outerwear, Underwear, Footwear, Accessories, One-Pieces, Other, or unknown. If the garment type (or any specific garment-related terms) are not explicitly mentioned in the description, respond with 'unknown'.\n\nDescription: {description}"
        prompt = prompt_template.format(description=description)
        messages=[
                {"role": "system", "content": "You are a helpful assistant. Your primary task is to categorize garments strictly based on their description. Only if a garment type (or any specific garment-related terms) are explicitly mentioned in the description, identify its category. For any description that does not explicitly state the garment type, you must classify it as 'unknown', regardless of any implied or suggestive details in the description."},
                {"role": "user", "content": prompt}
            ]
        
        response = self.api_client.chat_query(messages)
        garment_type = self.extract_garment_type(response.choices[0].message['content'])

        # Validate the garment type to ensure it's one of the predefined types
        valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "Other", "One-Pieces", "unknown"]
        return garment_type if garment_type in valid_types else "unknown"

class BWClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
  
        prompt_template = """You are a smart assistant. When given a description of a garment, determine if it contains the colors black and/or white. Respond with 'Black: Yes', 'White: Yes', 'Black: No', 'White: No', or 'Unknown' for each color. If there is no indication or if you are not sure, return 'Unknown'. Your response should be in a format that is easy to parse using Python.
                            Here is a garment description: {description} """

        prompt = prompt_template.format(description=description)
        
        response = self.api_client.query(prompt)
        raw_answer = response.choices[0].text.lower().strip()

        return extract_blackwhite(raw_answer)

class CompositionClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
  
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

        response = self.api_client.query(prompt2, model="gpt-3.5-turbo-instruct")
        raw_answer = response.choices[0].text.lower().strip()
        return res.union(extract_composition(raw_answer))
    
class JsonProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process(self, classifier, handle_item):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            keyvalues = handle_item(item, classifier)
            if(keyvalues):
                for key, value in keyvalues:
                    if key:
                        item[key] = value

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class OtherColorClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
  
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your task is to read a garment description and determine if the garment contains any color other than black and white. If the garment includes any other color, respond 'yes'. If the garment is only black, white, or a combination of these two colors, respond 'no'. If the color of the garment is not mentioned or is unclear in the description, respond with 'unknown'."},
            {"role": "user", "content": description},
            {"role": "assistant", "content": ""}  # The model will fill this in with 'yes', 'no', or 'unknown' based on the color description.
        ]
        
        response = self.api_client.chat_query(messages)

        raw_answer = response.choices[0].message.content.lower()

        return extract_otherColor(raw_answer)

def handle_garment_type(item, classifier):
    if "visual description" in item:
        classification = classifier.classify(item["visual description"])
        return [('type', classification)]
    return [(None, None)]

def handle_composition(item, classifier):
    if "details about that item" in item:
        details = item["details about that item"]
        details_parts = details.split('\n')
        if len(details_parts) >= 2:
            part1 = details_parts[0].strip()
            classification = classifier.classify(part1)
            return [('composition', classification)]
    return [(None, None)]

def handle_bw(item,classifier):
    if "visual description" in item:
        bw_list = classifier.classify(item["visual description"])
        return [('contains_black', bw_list[0]),('contains_white' , bw_list[1])]
    return [(None, None)]

def handle_otherColor(item,classifier):
    if "visual description" in item and "contains_other_color" not in item :
        answer = classifier.classify(item["visual description"])
        return [("contains_other_color", answer)]
    return [(None, None)]

if __name__ == '__main__':
    print("modifiying baseline ...")
    api_client = OpenAIClient()

    type_classifier = GarmentTypeClassifier(api_client)
    composition_classifier = CompositionClassifier(api_client)
    bw_classifier = BWClassifier(api_client)
    otherColor_classifier = OtherColorClassifier(api_client)
    json_processor = JsonProcessor("../MAIN_DATA/baseline_data6.json")

    print("Classifying garment types...")
    #json_processor.process(type_classifier, handle_garment_type)

    print("Classifying composition...")
    #json_processor.process(composition_classifier, handle_composition)
    print("classfiying other color...")
    json_processor.process(otherColor_classifier, handle_otherColor)


