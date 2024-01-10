
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json
import re
import openai
import os
import nltk
from SERVER.common_variables import *
from SERVER.META.metadata_card import *
import sys
import config
import spacy
from nltk.tokenize import sent_tokenize
openai.api_key = config.OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")
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

def find_product_by_id_in_file(file_path, product_id):
    """
    Find a product in a JSON file by its ID.

    :param file_path: Path to the JSON file.
    :param product_id: The ID of the product to find.
    :return: The product with the given ID, or None if not found.
    """
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            product_list = json.load(file)
            for product in product_list:
                if product['id'] == product_id:
                    return product
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    return None


def divide_description_into_smaller_chunks(baseline):
    print("dividing baseline into 4 words chunks ...")
    hashtable={}
    for item in baseline:
        sentences= []
        if("visual description" in item):
            sentences = extract_sentences(item["visual description"])
        for sentence in sentences:
            chunks = chunk_sentence(sentence, chunk_size=5, slide=3)
            for chunk in chunks:
                if(chunk not in hashtable):
                    hashtable[chunk] = set()
                hashtable[chunk].add(item["id"])  
    print("done")
    return hashtable

def divide_into_tiny_chunks(app,json_data,category="unknown"):
    print("dividing baseline into tiny chunks the category "+str(category)+" ...")
    hashtable={}
    for item in json_data:
        brand= ""
        name= ""
        details= ""
        sentences= []
        if("visual description" in item):
            sentences = extract_sentences(item["visual description"])
            description_without_newlines = replace_double_newlines(item["visual description"])
            if(description_without_newlines not in hashtable):
                hashtable[description_without_newlines] = set()
            hashtable[description_without_newlines].add(item["id"])

        if("brand" in  item):
            brand = item["brand"]
        if("name of the product" in item):
            name = item["name of the product"]+", "
        if("details about that item" in item):
            details = item["details about that item"]
            if details not in hashtable:
                hashtable[details] = set()
            hashtable[details].add(item["id"])

        name_key = name +" "+brand
        if name_key not in hashtable:
            hashtable[name_key] = set()
        if brand not in hashtable:
            hashtable[brand] = set()

        hashtable[name_key].add(item["id"])
        hashtable[brand].add(item["id"])

        details_parts = details.split('\n')
        if(len(details_parts)>=2):
            part1 = details_parts[0].strip()
            part2 = details_parts[1].strip()
            if part1 not in hashtable:
                hashtable[part1] = set()
            if part2 not in hashtable:
                hashtable[part2] = set()
            hashtable[part1].add(item["id"])
            hashtable[part2].add(item["id"])
            material_index = part1.find("Material:")
            if material_index != -1:
                composition_part1 = part1[:material_index].strip()
                composition_part2 = part1[material_index:].strip()
                if composition_part1 not in hashtable:
                    hashtable[composition_part1] = set()
                if composition_part2 not in hashtable:
                    hashtable[composition_part2] = set()
                hashtable[composition_part1].add(item["id"])
                hashtable[composition_part2].add(item["id"])

        for sentence in sentences:
            #sentence_without_noun = separate_sentence(sentence)[1] #comment this
            if(sentence not in hashtable):
                hashtable[sentence] = set()

            hashtable[sentence].add(item["id"])
            #if(sentence.count(',')==3):
                #separated_sentence = split_at_third_comma(sentence)
                #part1 = separated_sentence[0]
                #part2 = separated_sentence[1]
                #if(part1 not in hashtable):
                # hashtable[part1] = set()
                #if(part2 not in hashtable):
                # hashtable[part2] = set()
                #hashtable[part1].add(item["id"])
                #hashtable[part2].add(item["id"])
            #if(sentence_without_noun != ''):
                #if(sentence_without_noun not in hashtable):
                    #hashtable[sentence_without_noun] = set()
                #hashtable[sentence_without_noun].add(item["id"])

        
    print("done")
    return hashtable


def get_similar_doc_from_embedding(docsearch,query,k=10):
    print("getting "+str(k)+" most similar docs for query : "+str(query))
    docs = docsearch.similarity_search_with_score(query,k)
    #docs is a list of (doc, score)
    return docs

def get_similar_docs_from_small_embedding(app,feature_word,k=100):
    docs = app.embedding_of_small_chunks.similarity_search_with_score(feature_word,k)
    #docs is a list of (doc, score)
    return docs

def get_Ids_from_hashmap(list_of_docList,hashtable,set_sizes):
    #list_of_docList = [docs_1, docs_2 ,docs_3 ...] size = n
    #set_sizes = [a_1, a_2, a_3 ...]  size = n
    #we will extract the top a_1 UNIQUE Ids from docs_1 , then the top a_2 UNIQUE Ids from docs_2, etc ..
    #we return [set_1,set_2,set_3 ...set_n] where set_i contains the top a_i Ids from docs_i
    n = len(set_sizes)
    assert(len(set_sizes)==len(list_of_docList))
    list_of_sets = [set() for _ in range(n)]
    all_Ids =set()
    if(n==1):
        print("we need to return list containing only one set of size (+-) 20 ")
    for i in range(n):
        for item in list_of_docList[i]:
            content =  item.page_content
            if content in hashtable:
                if(len(list_of_sets[i])<set_sizes[i]):
                    if(len(hashtable[content])>7):
                        print("there are more than 7 ids having : "+str(content))
                    new_ids = hashtable[content].difference(all_Ids)
                    if(new_ids is not None):
                        list_of_sets[i] = list_of_sets[i].union(new_ids)
                else:
                    print("we stop adding Ids because we reached the maximum")
            else:
                print(f"ERROR! no id found in hashtable for content: {content}")
        all_Ids.union(list_of_sets[i])

    return list_of_sets

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
    
def is_single_word(s):
    words = s.split()
    return len(words) == 1 and words[0] != ""


def get_similar_doc_for_separated_input(app,correpsonding_embedding, user_input,separated_user_input,k):
    if(separated_user_input[0]!='' and separated_user_input[1]!=''):
        docs_with_score = get_similar_doc_from_embedding(correpsonding_embedding,user_input,k)
        print("top 6 docs for "+user_input+ " : ")
        print(docs_with_score[:7])
        docs2_with_score = get_similar_doc_from_embedding(correpsonding_embedding,separated_user_input[1],k)
        print("top 6 docs for "+separated_user_input[1]+ " : ")
        print(docs2_with_score[:7])
        docs_with_score.extend(docs2_with_score)
        return docs_with_score
    else:
        print("the input cant be separated ...")
        docs_with_score = get_similar_doc_from_embedding(correpsonding_embedding,user_input,2*k) #get the best k docs
        return docs_with_score

def filter_docs(app,docs_with_score,metadata_card,matching_controller):
    """
    return docs that match the metadata_card
    """
    filtered_docs = []
    for doc, score in docs_with_score:
        if(doc.page_content in app.hashtable):
            ids_of_elem = app.hashtable[doc.page_content]
        elif(doc.page_content in app.hashtable_small_chunks):
            ids_of_elem = app.hashtable_small_chunks[doc.page_content]
        else:
            print("ERROR IN HASHTABLE ")
        for id_of_elem in ids_of_elem:
            json_elem = find_product_by_id_in_file(app.config['BASELINE_PATH'],id_of_elem)
            if(matching_controller.meta_match(json_elem, metadata_card)):
                filtered_docs.append((doc,score))
                break
    return filtered_docs

def chunk_sentence(s, chunk_size=4, slide=2):
    # Split the sentence into words
    words = s.split()

    # Initialize a list to hold the chunks
    chunks = []

    # Iterate over the words with a sliding window
    for i in range(0, len(words), slide):
        # Create a chunk of 'chunk_size' words
        chunk = words[i:i + chunk_size]

        # Join the words to form a string chunk
        chunk_str = ' '.join(chunk)

        # Append the chunk to the list if it's not empty
        if chunk_str:
            chunks.append(chunk_str)

    return chunks

def get_topK_uniqueIds_from_docs(hashtable,meta_filtered_docs,k=24):
    sorted_docs = sorted(meta_filtered_docs, key=lambda pair: pair[1])
    print("20 first sorted docs : ")
    print(sorted_docs[:20])
    res =[]
    visited_ids=set()
    for elem,score in sorted_docs:
        if(len(res)<k):
            id_set = hashtable[elem.page_content]
            pair_list = create_list_of_pairs(id_set,score)
            for pair in pair_list:
                if(pair[0] not in visited_ids):
                    res.append(pair)
                visited_ids.add(pair[0])
    return res
        
def create_list_of_pairs(strings_set, score):
    return [(string, score) for string in strings_set]

def extract_feature_words_from_query(query):
    #extract keywords from query
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a garment analysis assistant. Your task is to identify and extract the most important features of the garment. Base your decision solely on the description provided. If the description does not explicitly mention a particular feature, respond with 'unknown'."},
            {"role": "user", "content": "do you have some vintage dark colored jacket for women? "},
            {"role": "assistant", "content": """vintage"""},  
            {"role": "user", "content": "something Kanye West could wear"},
            {"role": "assistant", "content": """Kanye West"""},  
            {"role": "user", "content": "black and white t-shirt (slim fit)"},
            {"role": "assistant", "content": """black and white,slim fit"""},  
            {"role": "user", "content": "a 100% cotton blue shirt for men"},
            {"role": "assistant", "content": """100% cotton,blue"""},  
            {"role": "user", "content": "different kind of accessories for a gothic style"},
            {"role": "assistant", "content": """gothic"""},  
            {"role": "user", "content": "I am looking for a military style shorts for men, do you have any ? "},
            {"role": "assistant", "content": """military"""},  
            {"role": "user", "content": "an item where the logo of the brand is printed/visible more than one time"},
            {"role": "assistant", "content": """logo"""},  
            {"role": "user", "content": 'a two-tone sweater, where the two colors are separated by a horizontal line throughout the sweater'},
            {"role": "assistant", "content": """two-tone,horizontal line"""},  
            {"role": "user", "content": query}
            # The assistant will process the input and respond based on the instructions given in the system message.
        ]
    )
    raw_answer =  response.choices[0].message.content.lower()
    return raw_answer

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
