from SERVER.META.metadata_utils import *
import openai
import re
def gpt35_type_output(description):
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

    return response.choices[0].message.content.strip()
   

def gpt35_composition_ouput(query):
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
    
   # print("raw result from gpt : ")
    return response.choices[0].text.lower().strip()


def mixtral_composition_output(query):

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


    return output['output']['choices'][0]['text'].lower()

def extract_otherColor(text):
    # Split the text by whitespace to get individual words
    pattern_yes = r'\byes\b'
    pattern_no = r'\bno\b'
    pattern_unknown = r'\bunknown\b'
    # Use regular expression to find all matches
    yes_count = len(re.findall(pattern_yes, text))
    no_count = len(re.findall(pattern_no, text))
    unknown_count = len(re.findall(pattern_unknown, text))

    if(yes_count>no_count and yes_count>unknown_count):
        return "yes"
    elif(no_count>yes_count and no_count > unknown_count):
        return "no"
    else:
        return "unknown"
    
def starling_otherColor_ouput(query):
    # do this before : $env:REPLICATE_API_TOKEN="<api_key>" 
    prompt_template = """GPT4 Correct User: You are a helpful assistant. Your primary task is to determine whether the garment described here contains a color other than black and white. Respond 'yes' only if the garment contains a color other than black and white. Respond 'no' if it explicitly states the garment is only black, white, or a combination of these two colors. If the description is ambiguous about color,  respond with 'unknown'. Avoid making assumptions based on incomplete color information. Avoid making assumptions based on incomplete color information. Black is a color and white is a color.Consider Black and White as colors ! Consider Black and White as colors !
Description : {query}  <|end_of_turn|>GPT4 Correct Assistant:"""
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

    return output.lower()
def gpt35_otherColor_ouput(query):
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

    messages=[
        {"role": "system", "content": "You are a helpful assistant. Your primary task is to determine whether the garment described here contains a color other than black and white. Respond 'yes' only if the garment contains a color other than black and white. Respond 'no' if it explicitly states the garment is only black, white, or a combination of these two colors. If the description is ambiguous about color,  respond with 'unknown'. Avoid making assumptions based on incomplete color information. Avoid making assumptions based on incomplete color information. Black is a color and white is a color."},
        {"role": "user", "content": "Description : "+query},
        {"role": "assistant", "content": ""}  # The model will fill this in with 'yes', 'no', or 'unknown' based on the color description.
    ]

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            top_p=1,
            messages=messages,
            max_tokens=60
        )

    raw_answer = response.choices[0].message.content.lower()

    return raw_answer

def gpt35_bw_ouput(query):
    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )

    prompt_template = """You are a smart assistant. Analyze the provided garment description and determine if it explicitly mentions the colors black and/or white. Only respond with 'Black: Yes' or 'White: Yes' if these colors are directly and clearly stated in the description. If there is any ambiguity or if the colors black or white are not explicitly mentioned, respond with 'Unknown' for each color.
                        If there is no indication or if you are not sure, return 'Unknown'. 
                        Do not complete the description or make assumptions. 
                        Your response should be in a format that is easy to parse using Python.
                        Here is a garment description: {description} """

    prompt = prompt_template.format(description = query)

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=60,
        temperature=0.5,
    )

    raw_answer = response.choices[0].text.lower().strip()

    return raw_answer



def starling_composition_output(query):
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

    return output.lower()
