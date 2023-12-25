
import sys
from openai import OpenAI
import os
from llama_index.llms import MistralAI
import together
import replicate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
#openai.api_key = config.OPENAI_API_KEY
together.api_key = config.TOGETHER_API_KEY

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

def extract_garment_type(llm_output):
    """
    extract the keywords "Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories" etc .. in llm_output
    """
    categories = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces","Other","unknown"]

    # Check if any of the keywords are in the text
    for category in categories:
        if category in llm_output:
            return category

    # Return "unknown" if no matching category is found
    return "unknown"

def extract_meta_Type(description):
    """
    Classify the type of a garment based on its text description.
    returns one of these categories  ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces","Other","unknown"]
    """

    prompt = f"Based on the following description, determine the garment type: Tops, Bottoms, Outerwear, Underwear, Footwear, Accessories, One-Pieces, Other, or unknown. If the garment type (or any specific garment-related terms) are not explicitly mentioned in the description, respond with 'unknown'.\n\nDescription: {description}"

    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Your primary task is to categorize garments strictly based on their description. Only if a garment type (or any specific garment-related terms) are explicitly mentioned in the description, identify its category. For any description that does not explicitly state the garment type, you must classify it as 'unknown', regardless of any implied or suggestive details in the description."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60
    )
    # Extract and return the garment type from the response
    garment_type = extract_garment_type(response.choices[0].message.content.strip())

    # Validate the garment type to ensure it's one of the predefined types
    valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "Other", "One-Pieces", "unknown"]
    return garment_type if garment_type in valid_types else "unknown"

def gpt35_ouput(query):
    prompt_template = """Based on user queries about garment preferences, categorize the materials into 'composition_in' and 'composition_out'. Categories are as follows:
        - Natural fibers: cotton, linen, hemp, jute, wool, silk.
        - Artificial fibers: viscose, acetate, rayon.
        - Synthetic fibers: nylon, polyester, polyamide, acrylic.

        User Query: {query}

        Extract and categorize the materials in the following format:
        - composition_in: List the categories that include the mentioned materials. If no materials are mentioned, categorize as 'unknown'.
        - composition_out: List the categories that should not be included in the garment. If the user query does not specify or does not mention materials, default to 'unknown'.

        Do not make assumptions about material types if they are not explicitly stated in the query. Do not make assumptions about material types if they are not explicitly stated in the query. Provide the composition categories accordingly.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Note: For a query where the materials are not explicitly stated the correct response is 'composition_in: unknown\ncomposition_out: unknown'"""
    prompt = prompt_template.format(query=query)
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens=60,
        temperature=0.5,
        )
    
    print("raw result from gpt : ")
    return response.choices[0].text.lower().strip()

def starling_output(query):
    # do this before : $env:REPLICATE_API_TOKEN="<api_key>"
    prompt_template = """GPT4 Correct User: Based on user queries about garment preferences, categorize the materials into 'composition_in' and 'composition_out'. Categories are as follows:
        - Natural fibers: cotton, linen, hemp, jute, wool, silk.
        - Artificial fibers: viscose, acetate, rayon.
        - Synthetic fibers: nylon, polyester, polyamide, acrylic.

        User Query: {query}

        Extract and categorize the materials in the following format:
        - composition_in: List the categories that include the mentioned materials. If no materials are mentioned, categorize as 'unknown'.
        - composition_out: List the categories that should not be included in the garment. If the user query does not specify or does not mention materials, default to 'unknown'.

        Do not make assumptions about material types if they are not explicitly stated in the query. Do not make assumptions about material types if they are not explicitly stated in the query. Provide the composition categories accordingly.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.

        Focus on the general category of fibers. Do not separate the materials within each category
        Don't modify and don't make assumptions on the user query
        Note: For a query where the materials are not explicitly stated the correct response is 'composition_in: unknown\ncomposition_out: unknown'  <|end_of_turn|>GPT4 Correct Assistant:"""
    prompt = prompt_template.format(query=query)

    output = replicate.run(
    "tomasmcm/starling-lm-7b-alpha:1cee13652378fac04fe10dedd4c15d3024a0958c3e52f97a1aa7c4d05b99ef99",
    input={
        "top_p": 1,
        "top_k": 36,
        "prompt": prompt,
        "max_tokens": 128,
        "temperature": 0.3,
        "presence_penalty": 0,
        "frequency_penalty": 0.1
    }
    )
    # print("raw input form starling : ")
    # print(output.lower())

    return output.lower()


def mixtral_output(query):

    prompt_template = """<s> [INST] Based on user queries about garment preferences, categorize the materials into 'composition_in' and 'composition_out'. Categories are as follows:
        - Natural fibers: cotton, linen, hemp, jute, wool, silk.
        - Artificial fibers: viscose, acetate, rayon.
        - Synthetic fibers: nylon, polyester, polyamide, acrylic.

        User Query: {query}

        Extract and categorize the materials in the following format:
        - composition_in: List the categories that include the mentioned materials. If no materials are mentioned, categorize as 'unknown'.
        - composition_out: List the categories that should not be included in the garment. If the user query does not specify or does not mention materials, default to 'unknown'.

        Do not make assumptions about material types if they are not explicitly stated in the query. Do not make assumptions about material types if they are not explicitly stated in the query. Provide the composition categories accordingly.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        Do not make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.
        DO NOT make assumptions about material types if they are not explicitly stated in the query.

        Focus on the general category of fibers. Do not separate the materials within each category
        Don't modify and don't make assumptions on the user query
        Note: For a query where the materials are not explicitly stated the correct response is 'composition_in: unknown\ncomposition_out: unknown' [/INST] </s>"""
    prompt = prompt_template.format(query=query)

    output = together.Complete.create(
    prompt = prompt, 
    model = "mistralai/Mixtral-8x7B-Instruct-v0.1", 
    max_tokens = 50,
    temperature = 0.3,
    top_k = 40,
    top_p = 0.6,
    repetition_penalty = 1.1,
    stop = ['<human>']
    )

    print("raw input form mistral : ")
    print(output['output']['choices'][0]['text'].lower())

    return output['output']['choices'][0]['text'].lower()

def extract_meta_composition(query):
    
    #result = gpt35_ouput(query)
    #result = mixtral_output(query)
    result = starling_output(query)

    return extract_composition_in_out(result)

class MetaDataCard:
    def __init__(self):
        self.type = "unknown"
        self.composition_in = {"unknown"}
        self.composition_out = {"unknown"}

    def __str__(self):
        return f"MetaDataCard(Type: {self.type}, Composition In: {self.composition_in}, Composition Out: {self.composition_out})"

def generate_metadata_card_from_query(query):
    metadata_card = MetaDataCard()
    metadata_card.type = extract_meta_Type(query)
    metadata_card.composition_in, metadata_card.composition_out = extract_meta_composition(query)
    return metadata_card

def is_type_match(app,json_elem,metadata_card):
    if json_elem is None:
        print("error in is_type_match ")
        return False
    
    if "type" not in json_elem:
        return True
    if(json_elem["type"]==""):
        return True
    if metadata_card.type is None or metadata_card.type =="":
        return True
    if(json_elem["type"] in app.corresponding_categories[metadata_card.type]):
        return True
    return False

def convert_to_set(input_string):
    return {item.strip() for item in input_string.split(',')}


def is_composition_match(json_elem,metadata_card):
    if "composition" not in json_elem  or json_elem["composition"]=="" or json_elem["composition"]=="unknown":
        return True
    if metadata_card.composition_in is None or metadata_card.composition_in =="" or metadata_card.composition_out is None or metadata_card.composition_out =="":
        return True
    
    composition_of_json = convert_to_set(json_elem["composition"])
    composition_in_set = metadata_card.composition_in
    composition_out_set = metadata_card.composition_out

    if(composition_in_set =={"unknown"} and composition_out_set =={"unknown"}):
        return True
    
    if((composition_in_set =={"unknown"} or composition_in_set.issubset(composition_of_json)) and (composition_out_set =={"unknown"} or not bool(composition_out_set.intersection(composition_of_json)))):
        return True
    return False

def meta_match(app,json_elem,metadata_card):
    type_match = is_type_match(app,json_elem,metadata_card)
    composition_matcth = is_composition_match(json_elem,metadata_card)

    return type_match and composition_matcth