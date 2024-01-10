import sys
from openai import OpenAI
import os
#import together
import replicate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
#openai.api_key = config.OPENAI_API_KEY
#together.api_key = config.TOGETHER_API_KEY

def extract_blackwhite(text):
    # Split the text into words
    words = text.replace(':', ' ').replace('-', ' ').split()

    # Initialize the list with None values
    mylist = ["unknown", "unknown"]

   # Find and analyze the word after "black"
    if "black" in words:
        index_black = words.index("black")
        for word in words[index_black + 1:]:
            #print("word after black : "+word)
            if word in ["yes", "no"]:
                mylist[0] = word
                break
            elif word == "white":
                break

    # Find and analyze the word after "white"
    if "white" in words:
        index_white = words.index("white")
        for word in words[index_white + 1:]:
            if word in ["yes", "no"]:
                mylist[1] = word
                break
            elif word == "black":
                break

    return mylist


def extract_composition_in_out(llm_output):
    """
    extract the key words "synthetic", "natural", "artificial" in the llm_ouput
    """
    categories = ["synthetic", "natural", "artificial"]
    res_in = set()
    res_out = set()
    lines = llm_output.split('\n')
    for line in lines:
        if 'composition_in:' in line or 'composition\_in' in line:
            for category in categories:
                if category in line:
                    res_in.add(category)
        elif 'composition_out:' in line or 'composition\_out' in line:
            for category in categories:
                if category in line:
                    res_out.add(category)
    
    if(len(res_in)==0 ):
        res_in.add("unknown")
    if(len(res_out)==0 ):
        res_out.add("unknown")

    if(len(res_in)==len(categories)):
        res_in={"unknown"}
    if(len(res_out)==len(categories)):
        res_out={"unknown"}
    return res_in,res_out

def convert_to_set(input_string):
    return {item.strip() for item in input_string.split(',')}

def extract_garment_type(llm_output):
    """
    extract the keywords "Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories" etc .. in llm_output
    """
    categories = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces","Other","unknown"]
    garment_type = "unknown"
    # Check if any of the keywords are in the text
    for category in categories:
        if category in llm_output:
            garment_type = category
            break


     # Validate the garment type to ensure it's one of the predefined types
    valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "Other", "One-Pieces", "unknown"]
    return garment_type if garment_type in valid_types else "unknown"