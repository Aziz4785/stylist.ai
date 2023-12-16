
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json
import re
import openai
import os
import nltk
import sys
import config
#import spacy
from nltk.tokenize import sent_tokenize

# Load spaCy's English language model
#nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
def extract_Ids_from_text(text):
    """
    Extract the pattern '#I' followed by exactly 6  alphanumeric characters,
    and excludes cases where '#I' is followed by more than 6  alphanumeric characters.
    """
    if text is None:
        return []
    
    pattern = r"#I[0-9A-Za-z]{6}(?![0-9A-Za-z])"
    matches = re.findall(pattern, text)
    return matches

def remove_outer_quotes(text):
    if text is None:
        return None
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def filter_json_By_Id(json_name,list_of_ids):
    """
    Generates a JSON object that filters entries based on a list of IDs.

    """
    with open(json_name, 'r', encoding='utf-8') as file:
      data = json.load(file)

    filtered_json = [entry for entry in data if entry['id'] in list_of_ids]

    return filtered_json

def mock_process(list_of_ids):
    json_filename = "Reference4.json"
    #list_of_ids = ["#I000004", "#I000005" , "#I000006", "#I000007"]
    with open(json_filename, 'r') as file:
      data = json.load(file)

    filtered_json = [entry for entry in data if entry['id'] in list_of_ids]

    return filtered_json

def read_json(filename):
     with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
     
def create_embedding(baseline_chunks):
    print("creating embedding ...")
    if(baseline_chunks is None):
        return None
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(baseline_chunks, embeddings)
    print("done")
    return docsearch

def extract_sentences(paragraph):
    sentences = sent_tokenize(paragraph)
    return sentences

def divide_into_tiny_chunks(json_data):
    """
    return a hash table where key = (a single sentence from "item description") or (name+brand+details )
    and value = id
    """
    print("dividing baseline into tiny chunks ...")
    hashtable={}
    for item in json_data:
        brand= ""
        name= ""
        details= ""
        sentences= []
        if("visual description" in item):
            sentences = extract_sentences(item["visual description"])
        if("brand" in  item):
            brand = "brand : "+item["brand"]+", "
        if("name of the product" in item):
            name = item["name of the product"]+", "
        if("details about that item" in item):
           details = item["details about that item"]

        hashtable[name +" "+brand]=item["id"]
        hashtable[details]=item["id"]

        for sentence in sentences:
            hashtable[sentence]=item["id"]
        if("visual description" in item):
            hashtable[replace_double_newlines(item["visual description"])]=item["id"]
    print("done")
    return hashtable

def ask_embedding_qa_langchain(docsearch,query):
    chain = load_qa_chain(OpenAI(),
                      chain_type="stuff") # we are going to stuff all the docs in at once
    
    custom_template = """Based on the provided description, identify the clothing items from the list that best align with the criteria. Please include their IDs for easy reference.

    List of Clothes:
    {context}

    Description:
    {question}

    Please analyze the list and description carefully to ensure the recommendations are highly relevant and specific to the described needs"""
    chain.llm_chain.prompt.template = custom_template
    docs = docsearch.similarity_search(query,k=10)
    print(" "+str(len(docs))+" 10 similar embedding found")
    print(docs)
    results = chain.run(input_documents=docs, question=query)
    return results

def get_similar_doc_from_embedding(docsearch,query,k=10):
    print("getting "+str(k)+" most similar docs for query : "+str(query))
    docs = docsearch.similarity_search(query,k)
    return docs


"""  
def get_similar_doc_from_embedding(docsearch,query,k):
    query_parts= separate_sentence(query)
    docs_main = docsearch.similarity_search(query,k)
    docs_second = docsearch.similarity_search(query_parts[1],k)
    return docs_main.extend(docs_second)
""" 
def get_Ids_from_hashmap(docs,hashtable):
    # each doc contain a "part" of the baseline of a single item
    #in this function, we get the id of the item corresponding to that "part"
    ids_set_gpt4 = set()
    ids_set_gpt3 = set()
    print("getting ids for docs :")
    print(docs)
    counter = 0
    for item in docs:
        content =  item.page_content
        if content in hashtable:
            if(counter<=9):
                ids_set_gpt4.add(hashtable[content])
            else:
                ids_set_gpt3.add(hashtable[content])
        else:
            print(f"ERROR! no id found in hashtable for content: {content}")

        counter+=1

    return ids_set_gpt4,ids_set_gpt3

def replace_double_newlines(text):
    return text.replace("\n\n", "\n")

def convert_to_proper_string(items):
    formatted_string = ""
    for product in items:
        formatted_string += f"id: {product['id']}\n"
        if('name of the product' in product):
            formatted_string += f"name of the product: '{product['name of the product']}'\n"
        if("brand" in product):
            formatted_string += f"brand: '{product['brand']}'\n"
        if('details about that item' in product):
            details = replace_double_newlines(product['details about that item'])
            formatted_string += f"details about that item: '{details}'\n"
        if('visual description' in product):
            description = replace_double_newlines(product['visual description'])
            formatted_string += f"visual description: '{description}'\n\n"
    return formatted_string

def get_chatgpt_response(context, question, with_analysis=False):
    # Your OpenAI API key
    openai.api_key = config.OPENAI_API_KEY

    if not isinstance(context, str):
        context = convert_to_proper_string(context)

    analysis = " Return only the corresponding IDs, nothing else"
    if(with_analysis):
        analysis = " Follow this with an analysis of the list and description to ensure the recommendations are highly relevant and specific to the described needs."
    
    custom_template2 = """"Based on the provided description, first identify and list the clothing items from the list that perfectly align with the criteria. Treat any shade of a specified color as meeting the color requirement unless the description explicitly demands a specific shade. Do not consider black or white as a shade of another color. Please include their IDs for easy reference.

List of Clothes:
{context}

Description:
"{question}"

Begin your response by listing IDs of the specific clothing items that 100% match the description, considering any shade of a specified color as meeting the requirement. {analysis}
"""

    custom_template3 = """"Here is a list of clothes (each associated with an ID), first identify and list the clothing items from the list that perfectly align with the user input. Treat any shade of a specified color as meeting the color requirement unless the description explicitly demands a specific shade. Do not consider black or white as a shade of another color. Please include their IDs for easy reference.

List of Clothes:
{context}

user input:
"{question}"

Begin your response by listing IDs of the specific clothing items that 100% match the user input , do not include IDs of clothes that don't match the user input
"""
    prompt = custom_template3.format(context=context, question=question, analysis=analysis)
    print("prompt : ")
    print(prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[{"role": "system", "content": "You specialize in fashion and apparel, offering personalized clothing recommendations based on user input."}, 
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)
    
def get_all_GPT3_response(context, question, with_analysis=False):
     # Process every two elements in the context
    final_response=""
    for i in range(0, len(context), 2):
        sublist = context[i:i + 2]  # Get two elements
        gpt3_response = get_GPT3_response(sublist,question,with_analysis)
        final_response+=(" "+gpt3_response)
    return final_response

def get_GPT3_response(context, question, with_analysis=False):
    # Your OpenAI API key
    openai.api_key = config.OPENAI_API_KEY

    if not isinstance(context, str):
        context = convert_to_proper_string(context)

    analysis = " Return only the corresponding IDs, nothing else"
    if(with_analysis):
        analysis = " Follow this with an analysis of the list and description to ensure the recommendations are highly relevant and specific to the described needs."
    
    custom_template2 = """"Based on the provided description, first identify and list the clothing items from the list that perfectly align with the criteria. Treat any shade of a specified color as meeting the color requirement unless the description explicitly demands a specific shade. Do not consider black or white as a shade of another color. Please include their IDs for easy reference.

List of Clothes:
{context}

Description:
"{question}"

Begin your response by listing IDs of the specific clothing items that 100% match the description, considering any shade of a specified color as meeting the requirement. {analysis}
"""
    custom_template3 = """"From the following list of clothes, each with a unique ID, identify and list only the IDs of the clothing items that precisely meet the specified criteria. It is crucial to exclude any IDs of items that do not match the criteria. Treat any shade of a specified color as meeting the color requirement unless a specific shade is explicitly required. Black and white should not be considered as shades of other colors. Your response should only include the IDs of the items that are a 100% match.

List of Clothes:
{context}

criteria:
"{question}"

Please provide a response that strictly lists the IDs of the clothing items meeting this exact criterion, without mentioning or including the IDs of any items that do not.
"""
    prompt = custom_template3.format(context=context, question=question, analysis=analysis)
    print("prompt : ")
    print(prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)
    
"""
def separate_sentence(sentence):
    # Parse the sentence
    doc = nlp(sentence)

    # Try to find the main noun phrase
    noun_phrases = list(doc.noun_chunks)
    if noun_phrases:
        main_noun_phrase = noun_phrases[0].text
        rest_of_sentence = sentence.replace(main_noun_phrase, '').strip()
        return main_noun_phrase, rest_of_sentence
    else:
        return sentence, ''
"""