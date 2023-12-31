import openai
import sys
import os
from openai import OpenAI
import json
import re
import together
from .metadata_generator_util import *

from abc import ABC, abstractmethod
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
script_dir = os.path.dirname(os.path.abspath(__file__))
baseline_path = os.path.join(script_dir, '..', '..', 'MAIN_DATA', 'baseline_data7.json')

class Config:
    @staticmethod
    def get_OPENAI_api_key():
        return config.OPENAI_API_KEY
    def get_MISTRAL_api_key():
        return config.TOGETHER_API_KEY

class MistralClient:
    def __init__(self):
        together.api_key = Config.get_MISTRAL_api_key()
    def query(self, prompt):
        output = together.Complete.create(
            prompt = prompt, 
            model = "mistralai/Mixtral-8x7B-Instruct-v0.1", 
            max_tokens = 50,
            temperature = 0.7,
            top_p = 1,
            stop = ['<human>']
            )
        return output['output']['choices'][0]['text'].lower()

class OpenAIClient:
    def __init__(self):
        self.api_key = Config.get_OPENAI_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)

    def query(self, prompt, model="gpt-3.5-turbo", max_tokens=60):
        return self.client.Completion.create(model=model, prompt=prompt, max_tokens=max_tokens)

    def chat_query(self, messages, model="gpt-3.5-turbo", max_tokens=60,temperature=-1,top_p=-1):
        if(temperature>0 and top_p >0):
            return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
            )
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

        prompt_template = (
        "Based on the following description, determine the garment type: "
        "Tops, Bottoms, Outerwear, Underwear, Footwear, Accessories, One-Pieces, Other, or Unknown. "
        "If the garment type (or any specific garment-related terms) are not explicitly mentioned in the description, "
        "respond with 'Unknown'. If more than one garment type is mentioned in the description, classify it as 'Other'.\n\n"
        "Description begins: {description}\nDescription ends."
        )
        prompt = prompt_template.format(description=description)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Your primary task is to categorize garments strictly based on their description. "
                    "Only if a garment type (or any specific garment-related terms) are explicitly mentioned in the description, identify its category. "
                    "Pullovers are considered Tops "
                    "For any description that does not explicitly state the garment type, classify it as 'Unknown'. "
                    "If the description contains more than one garment type, classify it as 'Other'. "
                    "Here's an example:\n\n"
                    "Description: 'A blue cotton t-shirt and leather boots.'\n"
                    "Classification: Other."
                )
            },
            {"role": "user", "content": prompt}
        ]
        
        response = self.api_client.chat_query(messages,temperature=0.7,top_p=1)
        garment_type = extract_garment_type(response.choices[0].message.content)

        # Validate the garment type to ensure it's one of the predefined types
        valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "Other", "One-Pieces", "unknown"]
        return garment_type if garment_type in valid_types else "unknown"

class BWClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
        messages=[
            {"role": "system", "content": "You are a smart assistant. hen given a description of a garment, determine if it contains the colors black and/or white. Respond with 'Black: Yes', 'White: Yes', 'Black: No', 'White: No', or 'Unknown' for each color. If there is no indication or if you are not sure, return 'Unknown'. Your response should be in a format that is easy to parse using Python."},
            {"role": "user", "content": "Here is a garment description: " +description}
            ]
        
        response = self.api_client.chat_query(messages,temperature=0.7,top_p=1)
        raw_answer = response.choices[0].message.content.lower().strip()
        return extract_blackwhite(raw_answer)

class CompositionClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
  
        res = set()
        contain_artificial, description = remove_artificial_fabric(description)
        if contain_artificial:
            res.add("artificial")

        messages=[
            {"role": "system", "content": "You are an AI trained to categorize fabrics in garment descriptions into three categories: natural, synthetic, and unknown. Natural fabrics are those like cotton, linen, hemp, jute, wool or silk. Synthetic fabrics include materials like nylon, polyester, polyamide, acrylic or elastane. If you are unsure about the category of a fabric, classify it as unknown. List all categories present in a given garment description."},
            {"role": "user", "content": "Analyze this garment description: 'Composition: 60% cotton, 20% nylon, 20% unknown, Material: Knit / mesh'."},
            {"role": "assistant", "content": "Categories: 'natural', 'synthetic', 'unknown'."},
            {"role": "user", "content": "What about this one: 'Composition: 98% cotton, 2% elastane, Material: Canvas'."},
            {"role": "assistant", "content": "Categories: 'natural', 'synthetic'."},
            {"role": "user", "content": "And for 'Composition: 100% cotton, Material: Piqué'?"},
            {"role": "assistant", "content": "Categories: 'natural'."},
            {"role": "user", "content": "Now, analyze the following garment description and categorize the fabrics: "+description}
        ]
        # prompt_without_aritifical = """I am an AI trained to categorize fabrics in garment descriptions into three categories: natural, synthetic, and unknown. Natural fabrics are those like cotton, linen, hemp, jute, wool or silk. Synthetic fabrics include materials like nylon, polyester, polyamide, acrylic or elastane. If I am unsure about the category of a fabric, I will classify it as unknown. I will list all the categories present in a given garment description.
        #         Examples:
        #         - Description: "Composition: 60% cotton, 20% nylon, 20% unknown, Material: Knit / mesh"
        #         Categories: "natural", "synthetic", "unknown"
        #         - Description: "Composition: 98% cotton, 2% elastane, Material: Canvas"
        #         Categories: "natural", "synthetic"
        #         - Description: "Composition: 100% cotton, Material: Piqué"
        #         Categories: "natural"

        #         Now, analyze the following garment description and categorize the fabrics:

        #         {description}"""
        # prompt2 = prompt_without_aritifical.format(description=description)

        #response = self.api_client.query(prompt2, model="gpt-3.5-turbo-instruct")
        response = self.api_client.chat_query(messages,temperature=0.7,top_p=1)
        raw_answer = response.choices[0].message.content.lower().strip()
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
                        if isinstance(value, set):
                            item[key] = ', '.join(map(str, value))
                        else:
                            item[key] = value

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class OtherColorClassifier(ClassifierService):
    def __init__(self, api_client):
        self.api_client = api_client

    def classify(self, description):
  
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your task is to read a garment description and determine if the garment contains any color other than black and white. If the garment includes any other color, respond 'yes'. If the garment is only black, white, or a combination of these two colors, respond 'no'. If the garment description describes a garment only with colors black and white, repsond 'no'. If the color of the garment is not mentioned or is unclear in the description, respond with 'unknown'."},
            {"role": "user","content": "description of the garment : a pair of shoes that masterfully blend black and white elements to create a stylish and eye-catching design. The base of the shoes is white, giving them a clean and sharp appearance. This white base is complemented with black detailing, creating a striking contrast that adds to their visual appeal.The toe box and the heel counter of the shoes are accented in black, framing the white central part and providing a sleek look. The laces are also black, which stands out against the white tongue and adds a dynamic element to the design. "},
            {"role": "assistant", "content": "no"} ,
            {"role": "user", "content": "description of the garment : "+description},
            {"role": "assistant", "content": ""}  
        ]
        
       

        #mistral_prompt_temp =" <s> [INST] You are a helpful assistant. Your task is to read a garment description and determine if the garment contains any color other than black and white. If the garment includes any other color, respond 'yes'. If the garment is only black, white, or a combination of these two colors, respond 'no'. If the color of the garment is not mentioned or is unclear in the description, respond with 'unknown'. {description} [/INST] </s>"
        #mistral_prompt = mistral_prompt_temp.format(description=description)

        #raw_answer_mistral = self.api_client.query(mistral_prompt)
        response = self.api_client.chat_query(messages,temperature=0.7,top_p=1)

        raw_answer = response.choices[0].message.content.lower()

        return extract_otherColor(raw_answer)

def handle_garment_type(item, classifier):
    complete_description=""
    if "type" not in item:
        if "name of the product" in item :
            complete_description = item["name of the product"]
        if "visual description" in item:
            classification = classifier.classify(complete_description + ", "+item["visual description"])
            return [('type', classification)]
    return [(None, None)]

def handle_composition(item, classifier):
    if("composition" not in item ):
        if "details about that item" in item:
            details = item["details about that item"]
            details_parts = details.split('\n')
            if len(details_parts) >= 2:
                part1 = details_parts[0].strip()
                classification = classifier.classify(part1)
                return [('composition', classification)]
    return [(None, None)]

def handle_bw(item,classifier):
    if("contains_black" not in item and 'contains_white' not in item):
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
    #RUN py -m ZALANDO_SCRAPER.META.metadata_generator at root
    print("modifiying baseline ...")
    api_client = OpenAIClient()

    type_classifier = GarmentTypeClassifier(api_client)
    composition_classifier = CompositionClassifier(api_client)
    bw_classifier = BWClassifier(api_client)
    otherColor_classifier = OtherColorClassifier(api_client)
    json_processor = JsonProcessor("MAIN_DATA/baseline_data7.json")

    print("Classifying garment types...")
    json_processor.process(type_classifier, handle_garment_type)

    print("Classifying composition...")
    json_processor.process(composition_classifier, handle_composition)

    print("Classifying bw...")
    json_processor.process(bw_classifier, handle_bw)
    # print("classfiying other color...")
    # json_processor.process(otherColor_classifier, handle_otherColor)


