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
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#import ZALANDO_SCRAPER.config as config
import config
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def encode_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return None

def describe_clothing_multi(name, brand, infos_from_site, images):
    """
    Generate a description from up to 3 images of the same product.
    """
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    # Check if images is not None and is a list
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

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please provide a detailed description of the garment shown in these images. The garment's name is (" + garment + "). Begin by directly listing its colors, for example: blue, brown, red. Alongside your description, consider the following additional information about the item: (" + infos_from_site + "). Focus on aspects such as the garment's design, style, colors, unique features, and overall appearance. If there is any graphics or text on it please dessribe it. Avoid repeating any details about the material composition, care instructions, or other information already provided. Aim to capture the essence and distinct qualities of this garment that are visible in the images. Please be concise and generate less than 130 words."
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
            max_tokens=180,
        )

        return response.choices[0].message.content
    
    except openai.BadRequestError as e:
        # Handle the error here
        print("An error occurred: ", e)
        return None
    
def encode_imagesURLS(images_urls):
    encoded_images = []
    try:
        for img_url in images_urls:
            encoded_image = encode_image_from_url(img_url)
            if encoded_image:
                encoded_images.append(encoded_image)
        print("Image sources encoded successfully.")
    except Exception as e:
        print(f"Error occurred while encoding image sources: {e}")

    return encoded_images
def generate_catalog_single_elem(entry):
    """
        catalogue elem has this format :
        {
        "id": <id>,
        "gender": <gender>
        "name of the product : "", 
        "brand" :, 
        details about that item : "", 
        visual description : ""
        }
    """
    images=entry.get("images")
    #encoded_images = encode_imagesURLS(images)

    id = entry.get("id")
    gender = entry.get("gender")
    name = entry.get("name")
    brand = entry.get("brand")
    composition = entry.get("composition and care (en)")
    details = entry.get("more details (en)")

    components = [name, brand, composition, details]
    total = " \n ".join([comp for comp in components if comp])

    description = describe_clothing_multi(name, brand, total, images)
    #description = "test description"
    elem = {}
    if id:
        elem["id"] = id
    if gender:
        elem["gender"] = gender
    if name:
        elem["name of the product"] = name
    if brand:
        elem["brand"] = brand
    if composition or details:
        elem["details about that item"] = " \n ".join(filter(None, [composition, details]))
    if description:
        elem["visual description"] = description

    return elem


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
    """
    Appends the given element to a JSON file.

    :param catalogue_elem: The element to be added.
    :param filename: Name of the JSON file to which the element is added.
    """
    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[catalogue_name]

    if isinstance(catalogue_elem, dict):
        collection.insert_one(catalogue_elem)
    elif isinstance(catalogue_elem, list):
        collection.insert_many(catalogue_elem)

    client.close()

def convert_Collection_to_Catalog_and_Reference(scraped_data_collection_name, catalogue_name, reference_name):
    item_processed = 0

    db_uri = config.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    scraped_data_collection = db[scraped_data_collection_name]
    reference_collection = db[reference_name]

    scraped_data_length = scraped_data_collection.count_documents({})
    for scraped_data_doc in scraped_data_collection.find():
        if "id" in scraped_data_doc:
            if iD_is_in_Catalogue(catalogue_name, scraped_data_doc["id"]):
                continue
        item_processed += 1

        # Check for 'images' key
        images = []

        if 'images' in scraped_data_doc and scraped_data_doc['images']:
            images = scraped_data_doc['images']

        catalogue_elem = generate_catalog_single_elem(scraped_data_doc)
        add_to_Catalogue(catalogue_elem, catalogue_name)

        scraped_url = ""
        if("url" in scraped_data_doc):
            scraped_url = scraped_data_doc['url']

        reference_elem = {
            'id': scraped_data_doc['id'],
            'url': scraped_url,
            'images': images 
        }

        reference_collection.insert_one(reference_elem)

        if item_processed % 5 == 0:
            print(str(math.ceil(item_processed * 100 / scraped_data_length)) + "% done ")


def generate_Catalog_and_Reference(reference_name, catalogue_name):
    
    client = pymongo.MongoClient(config.db_uri)
    db = client[config.db_name]

    for collection_name in db.list_collection_names():
        # Check if the collection name starts with 'data_'
        if collection_name.startswith("data_"):
            if collection_name in {"data_luxe-homme"}:
                print("Processing " + str(collection_name) + " ...")
                convert_Collection_to_Catalog_and_Reference(collection_name, catalogue_name, reference_name)
 

generate_Catalog_and_Reference("reference8", "Catalogue1")