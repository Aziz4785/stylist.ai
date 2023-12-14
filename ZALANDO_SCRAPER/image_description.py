# Importing libraries
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests
import os
import logging
import openai
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY


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
    generate a description from 3 images of the same product
    """
    images = images[:3]  # max 3 images
    garment = "garment"
    if(name):
        garment = name

    if name and brand:
        garment = brand + " " + name

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": "Please provide a detailed description of the garment shown in these images. The garment's "
                         "name is ("+garment+"). Alongside your description, "
                         "consider the following additional information about the item: ("+infos_from_site+"). Focus on"
                         "aspects such as the garment's design, style, unique features, and overall appearance. Avoid "
                         "repeating any details about the material composition, care instructions, "
                         "or other information already provided. Aim to capture the essence and distinct qualities of "
                         "this garment that are visible in the images. Please be concise and generate less than 130 words"}
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

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=180,
    )
    return response.choices[0].message.content

"""
def scrap_images_from_link(driver, url):

    return the list of images of a product page 

    try:
        driver.get(url)
        print("URL successfully opened.")
    except Exception as e:
        print(f"Error occurred while opening URL: {e}")
        return []

    # Handling cookie acceptance
    try:
        print("Looking for cookie accept button...")
        wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
        cookie_accept_button = wait.until(EC.element_to_be_clickable((By.ID, "uc-btn-accept-banner")))
        cookie_accept_button.click()
        print("Cookie accept button clicked.")
    except NoSuchElementException:
        print("Cookie accept button not found.")
    except TimeoutException:
        print("Timed out waiting for cookie accept button.")
    except Exception as e:
        print(f"An unexpected error occurred while handling cookies: {e}")

    # Find images
    try:
        div_class = "_5qdMrS WzZ4iu _01vVuu _6GQ88b WdG8Bv"
        print(f"Searching for images with class: {div_class}")
        images = driver.find_elements(By.CSS_SELECTOR, f'div.{div_class.replace(" ", ".")} img')
        print(f"Found {len(images)} images.")
    except Exception as e:
        print(f"Error occurred while searching for images: {e}")
        return []

    try:
        srcs = [img.get_attribute('src') for img in images]
        print("Image sources extracted successfully.")
    except Exception as e:
        print(f"Error occurred while extracting image sources: {e}")

    # Extract the src attributes and encode images
    encoded_images = []
    try:
        for img in images:
            img_url = img.get_attribute('src')
            encoded_image = encode_image_from_url(img_url)
            if encoded_image:
                encoded_images.append(encoded_image)
        print("Image sources encoded successfully.")
    except Exception as e:
        print(f"Error occurred while encoding image sources: {e}")

    return srcs,encoded_images
"""
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
def generate_baseline_single_elem(entry):
    """
        baseline elem has this format :
        {
        "id": <id>,
        "name of the product : "", 
        "brand" :, 
        details about that item : "", 
        visual description : ""
        }
    """
    images=entry.get("images")
    #encoded_images = encode_imagesURLS(images)

    id = entry.get("id")
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
    if name:
        elem["name of the product"] = name
    if brand:
        elem["brand"] = brand
    if composition or details:
        elem["details about that item"] = " \n ".join(filter(None, [composition, details]))
    if description:
        elem["visual description"] = description

    return elem


def iD_is_in_baseline_file(file_path, id_to_check):

    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the ID exists in the data
    for item in data:
        if item.get("id") == id_to_check:
            return True

    return False


def add_to_baseline_file(baseline_elem, filename):
    """
    Appends the given element to a JSON file.

    :param baseline_elem: The element to be added.
    :param filename: Name of the JSON file to which the element is added.
    """
    try:
        # Read the existing data from the file
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(baseline_elem)

        # Write the updated data back to the file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"An error occurred: {e}")

def process_json_file_incr(scraped_textInfos_filepath, reference_file_path, baseline_filepath):
    """
    simulatenously generate The reference and the baseline from the scrapedText_data
    """

    item_processed = 0
    with open(scraped_textInfos_filepath, 'r', encoding='utf-8') as file:
        scraped_textInfos = json.load(file)

    # Check if reference file exists and is not empty
    if os.path.exists(reference_file_path) and os.path.getsize(reference_file_path) > 0:
        with open(reference_file_path, 'r+') as reference_file:
            reference_file.seek(0, os.SEEK_END)    # Go to the end of file
            # Move back one position to overwrite the closing bracket ']'
            # Using reference_file.tell() instead of file.tell()
            pos = reference_file.tell() - 1
            reference_file.seek(pos, os.SEEK_SET)
            if len(scraped_textInfos) > 0:
                reference_file.write(',')  # Add a comma to separate new data from existing data

            for i, singleItem_text_info in enumerate(scraped_textInfos):
                if iD_is_in_baseline_file(baseline_filepath, singleItem_text_info["id"]):
                    continue
                item_processed+=1
                baseline_elem = generate_baseline_single_elem(singleItem_text_info)
                add_to_baseline_file(baseline_elem,baseline_filepath)
            
                reference_elem = json.dumps({
                    'id': singleItem_text_info['id'],
                    'url': singleItem_text_info['url'],
                    'images': singleItem_text_info['images']
                })
                reference_file.write(reference_elem)
                if i < len(scraped_textInfos) - 1:
                    reference_file.write(',\n')

                if(item_processed%5==0):
                    print(str(item_processed*100/len(scraped_textInfos)) + " done ")
            reference_file.write(']')  # End of JSON array

    else:
        # File doesn't exist or is empty, write as new
        with open(reference_file_path, 'w') as reference_file:
            reference_file.write('[')  # Start of JSON array

            for i, singleItem_text_info in enumerate(scraped_textInfos):
                if iD_is_in_baseline_file(baseline_filepath, singleItem_text_info["id"]):
                    continue
                item_processed+=1
                baseline_elem = generate_baseline_single_elem(singleItem_text_info)
                add_to_baseline_file(baseline_elem,baseline_filepath)
                reference_elem = json.dumps({
                    'id': singleItem_text_info['id'],
                    'url': singleItem_text_info['url'],
                    'images': singleItem_text_info['images']
                })
                reference_file.write(reference_elem)
                if i < len(scraped_textInfos) - 1:
                    reference_file.write(',\n')
                if(item_processed%5==0):
                    print(str(item_processed*100/len(scraped_textInfos)) + " done ")
            reference_file.write(']')  # End of JSON array


def process_json_files_in_folder(folder_path, output_json_filename, output_baseline_filename):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            if (filename == "data_luxe-homme.json" or filename == "data_mode-femme.json" or filename =="data_sport-homme.json"):
                #service = Service(ChromeDriverManager().install())
                #driver = webdriver.Chrome(service=service)
                print("processing " + str(filename) + " ...")
                json_file_path = os.path.join(folder_path, filename)
                process_json_file_incr(json_file_path, output_json_filename, output_baseline_filename)
 

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate two levels up and then into the MAIN_DATA directory
output_reference_path = os.path.join(script_dir, '..', 'MAIN_DATA', 'Reference6.json')

output_baseline = os.path.join(script_dir, '..', 'MAIN_DATA', 'baseline_data6.json')

folder_path_of_scraped_text = os.path.join(script_dir,'zalando_text_scraper', 'output_json')
print("Current Working Directory:", os.getcwd())
process_json_files_in_folder(folder_path_of_scraped_text, output_reference_path, output_baseline)