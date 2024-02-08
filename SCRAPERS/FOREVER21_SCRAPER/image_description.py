# Importing libraries
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import requests
import os
import logging
import math
import pymongo
from openai import OpenAI
import openai
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

import config_server
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def describe_clothing_multi(name, brand,composition, description, size_fit,images):
    """
    Generate a description from up to 3 images of the same product.
    """
    client = openai.OpenAI(api_key=config_server.OPENAI_API_KEY)
    maxtokens = 60
    if images and isinstance(images, list):
        images = images[:3]  # Use a maximum of 3 images
    else:
        images = []  # If images is None or not a list, use an empty list
        return ""

    garment = "garment"
    if name:
        garment = name

    if name and brand:
        garment = brand + " " + name

     # Base message
    message = f"Here are some images of a garment named '{garment}'."
    if description:
        message += f" Additionally, here is a description of that garment: '{description}'. Could you analyze the image and provide additional details or aspects that are not included in my current description?"
    else:
        message += " Please provide a detailed description of the garment shown in these images. Begin by directly listing its colors, for example: blue, brown, red."
    
    if composition:
        message += f" Alongside your description, consider the following additional information about the item: ({composition})."

    message += "Avoid repeating any details about the material composition, care instructions, or other information already provided."
    
    if description:
        message +=" Focus on aspects such as the garment's design, style, colors, unique features, overall appearance, or any graphics or text that are not included in my current description."
    else:
        message += "Focus on aspects such as the garment's design, style, colors, unique features, and overall appearance. If there is any graphics or text on it please dessribe it."
    
    if size_fit:
        message += f" Here is some additional information about the images: '{size_fit}'."

    if description:
        message+= "Please be concise and limit the response to less than 50 words."
    else:
        message += "Please be concise and limit the response to less than 130 words."
        maxtokens=150

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
    ]

    # Add image URLs to the messages
    for img_url in images:
        if requests.head(img_url).status_code == 200:
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": img_url,
                }
            })
        else:
            print(f"Invalid or inaccessible URL: {img_url}")

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=maxtokens,
        )

        return response.choices[0].message.content
    
    except openai.BadRequestError as e:
        # Handle the error here
        print("An error occurred: ", e)
        return None

def generate_catalog_single_elem(entry):
    """
        catalogue elem has this format :
        {
        "id": <id>,
        "gender": <gender>
        "type": <type>
        "name of the product : "", 
        "brand" :, 
        "materials" : ,
        source : forever21,
        details about that item : "", 
        visual description : ""
        }
    """
    images=entry.get("images")

    id = entry.get("id")
    gender = entry.get("gender")
    type = entry.get("type")
    name = entry.get("name")
    brand = entry.get("brand")
    size_fit = entry.get("size + fit (en)")
    composition = entry.get("composition and care (en)")
    details = entry.get("more details (en)")

    if details:
        if details.strip()[-1] !='.':
            details+='.'

    description = describe_clothing_multi(name, brand,composition, details, size_fit,images)
    #description = "test description"
    elem = {}
    if id:
        elem["id"] = id
    if gender:
        elem["gender"] = gender
    if type:
        elem["type"]=type
    if name:
        elem["name of the product"] = name
    if brand:
        elem["brand"] = brand
    if composition:
        elem["materials"] = composition
    if description:
        elem["visual description"] = details + '\n' +description
    elem["source"] = "forever21"
    return elem

def generate_reference_single_elem(scraped_data_doc):
    # get images array from the document
    images = []

    if 'images' in scraped_data_doc and scraped_data_doc['images']:
        images = scraped_data_doc['images']

    scraped_url = ""
    if("url" in scraped_data_doc):
        scraped_url = scraped_data_doc['url']

    reference_elem = {
        'id': scraped_data_doc['id'],
        'url': scraped_url,
        'images': images 
    }

    return reference_elem


def iD_is_in_Catalogue(catalogue_name,id_to_check):
    #catalogue_name is the collection name
    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[catalogue_name]

    if collection.find_one({"id": id_to_check}):
        client.close()
        return True
    else:
        client.close()
        return False


def add_to_Catalogue(catalogue_elem, catalogue_name):
    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[catalogue_name]

    try:
        if isinstance(catalogue_elem, dict):
            result = collection.insert_one(catalogue_elem)
            return result.acknowledged
        elif isinstance(catalogue_elem, list):
            result = collection.insert_many(catalogue_elem)
            return result.acknowledged
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        client.close()

def add_to_Reference(reference_elem, reference_name):
    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[reference_name]

    try:
        if isinstance(reference_elem, dict):
            result = collection.insert_one(reference_elem)
            return result.acknowledged
        elif isinstance(reference_elem, list):
            result = collection.insert_many(reference_elem)
            return result.acknowledged
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        client.close()


def convert_Collection_to_Catalog_and_Reference(scraped_data_collection_name, catalogue_name, reference_name):
    items_added_to_catalogue = 0
    items_added_to_reference = 0

    db_uri = config_server.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    scraped_data_collection = db[scraped_data_collection_name]
    scraped_data_length = scraped_data_collection.count_documents({})
    
    for scraped_data_doc in scraped_data_collection.find():
        if "id" in scraped_data_doc:
            if iD_is_in_Catalogue(catalogue_name, scraped_data_doc["id"]):
                continue

        catalogue_elem = generate_catalog_single_elem(scraped_data_doc)
        if(add_to_Catalogue(catalogue_elem, catalogue_name)):
            items_added_to_catalogue += 1

        reference_elem = generate_reference_single_elem(scraped_data_doc)
        if(add_to_Reference(reference_elem, reference_name)):
            items_added_to_reference += 1
       

        if items_added_to_catalogue % 5 == 0:
            print(str(math.ceil(items_added_to_catalogue * 100 / scraped_data_length)) + "% done ")

    print(str(items_added_to_catalogue)+" items have been added to catalogue")
    print(str(items_added_to_reference)+" items have been added to reference")


def generate_Catalog_and_Reference(reference_name, catalogue_name):
    
    client = pymongo.MongoClient(config.db_uri)
    db = client[config_server.db_name]

    for collection_name in db.list_collection_names():
        # Check if the collection name starts with 'data_'
        if collection_name.startswith(config.collection_name_start_with):
            print(collection_name)
            if collection_name in {"data_f21_mens-tops","data_f21_outerwear_coats-and-jackets","data_f21_sweater","data_f21_mens-shirts"}:
                print("Processing " + str(collection_name) + " ...")
                convert_Collection_to_Catalog_and_Reference(collection_name, catalogue_name, reference_name)
 

generate_Catalog_and_Reference("reference8", "Catalogue1")