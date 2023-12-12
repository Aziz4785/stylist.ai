from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests
import os
import openai
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

openai.api_key = config.OPENAI_API_KEY
def describe_clothing_multi(name,brand,infos_from_site, images):
    """
    generate a description from 3 images of the same product
    """
    images = images[:3] # max 3 images
    garment= "garment"

    if(name and brand):
        garment = brand + " "+name

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Directly describe this ("+garment+") represented in these images. Here are some additional informations about it: " + infos_from_site
         +"Please do not repeat the details already provided about the material composition, care instructions etc.."}
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
        max_tokens=200,
    )

    return response.choices[0].message.content

def scrap_images_from_link(driver, url):
    """
    return the list of images of a product page 
    """
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

    # Extract the src attributes
    try:
        srcs = [img.get_attribute('src') for img in images]
        print("Image sources extracted successfully.")
    except Exception as e:
        print(f"Error occurred while extracting image sources: {e}")
        srcs = []
   
    return srcs


def generate_baseline_single_elem(entry,image_sources):
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
    id = entry.get("id")
    name = entry.get("name")
    brand = entry.get("brand")
    composition = entry.get("composition and care (en)")
    details = entry.get("more details (en)")

    components = [name,brand,composition, details]
    total = " \n ".join([comp for comp in components if comp])

    description = describe_clothing_multi(name,brand,total, image_sources)

    elem ={}
    if id:
        elem["id"]= id
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
    :param filename: Name of the JSON file to which the element is added. Default is 'baseline_data.json'.
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
            json.dump(data, file, indent=4,ensure_ascii=False)

    except Exception as e:
        print(f"An error occurred: {e}")

def process_json_file_incr(driver, scrapedText_data, reference_file, baseline_filepath):
    """
    simulatenously generate The reference and the baseline from the scrapedText_data
    """

    item_processed = 0
    with open(scrapedText_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    try:
        # Check if reference file exists and is not empty
        if os.path.exists(reference_file) and os.path.getsize(reference_file) > 0:
            with open(reference_file, 'r+') as file:
                file.seek(0, os.SEEK_END)    # Go to the end of file
                file.seek(file.tell() - 1, os.SEEK_SET)  # Move back one position to overwrite the closing bracket ']'
                if len(data) > 0:
                    file.write(',')  # Add a comma to separate new data from existing data

                for i, entry in enumerate(data):
                    if iD_is_in_baseline_file(baseline_filepath, entry["id"]):
                        continue
                    else:
                        print("new id")
                    image_sources = scrap_images_from_link(driver, entry['url'])
                    baseline_elem = generate_baseline_single_elem(entry, image_sources)
                    item_processed += 1
                    add_to_baseline_file(baseline_elem,baseline_filepath)
                    json_entry = json.dumps({
                        'id': entry['id'],
                        'url': entry['url'],
                        'images': image_sources
                    })
                    file.write(json_entry)
                    if i < len(data) - 1:
                        file.write(',\n')

                file.write(']')  # End of JSON array

        else:
            # File doesn't exist or is empty, write as new
            with open(reference_file, 'w') as file:
                file.write('[')  # Start of JSON array

                for i, entry in enumerate(data):
                    if iD_is_in_baseline_file(baseline_filepath, entry["id"]):
                        continue
                    else:
                        print("new id")
                    image_sources = scrap_images_from_link(driver, entry['url'])
                    baseline_elem = generate_baseline_single_elem(entry, image_sources)
                    item_processed += 1
                    add_to_baseline_file(baseline_elem,baseline_filepath)
                    json_entry = json.dumps({
                        'id': entry['id'],
                        'url': entry['url'],
                        'images': image_sources
                    })
                    file.write(json_entry)
                    if i < len(data) - 1:
                        file.write(',\n')

                file.write(']')  # End of JSON array

        print(" item processed = " + str(item_processed))
    finally:
        driver.quit()

def process_json_files_in_folder(folder_path, output_json_filename, output_baseline_filename):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            try:
                print("processing " + str(filename) + " ...")
                json_file_path = os.path.join(folder_path, filename)
                if(filename == "data_streetwear-homme.json"):
                    process_json_file_incr(driver, json_file_path, output_json_filename, output_baseline_filename)
            finally:
                driver.quit()


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate two levels up and then into the MAIN_DATA directory
output_reference_path = os.path.join(script_dir, '..', '..', 'MAIN_DATA', 'Reference5.json')

output_baseline = os.path.join(script_dir, '..', '..', 'MAIN_DATA', 'baseline_data5.json')

folder_path_of_scraped_text = os.path.join(script_dir, '..', 'zalando_text_scraper', 'output_json')
print("Current Working Directory:", os.getcwd())
process_json_files_in_folder(folder_path_of_scraped_text, output_reference_path, output_baseline)