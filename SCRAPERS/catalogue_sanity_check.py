import config_server
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def IDinReference(id):
    db_uri = config_server.db_uri
    db_name = config.db_name

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[config_server.reference_name]

    found = collection.find_one({"id": id})
    client.close()
    return bool(found)

def getLinkFromReference(id):
    client = pymongo.MongoClient(config_server.db_uri)
    db = client[config.db_name]
    mongodb_collection = db[config_server.reference_name]
    link = None

    for entry in mongodb_collection.find():
        if entry['id'] == id:
            link = entry["url"]
            break

    return link

def isBrokenLink(link,source,driver):
    try:
        # Use GET request for specific sites known to handle HEAD requests differently
        if source in ["zalando", "anotherSiteWithIssues"]:
            response = requests.get(link, allow_redirects=True, timeout=5)
        else:
            response = requests.head(link, allow_redirects=True, timeout=5)

        if 400 <= response.status_code <= 599:
            print(f"  Broken link due to status code {response.status_code}: {link}")
            return True

    except requests.RequestException as e:
        print(f"Exception occurred: {e}")
        return True
    
    if source == "zalando":
        try:
            driver.get(link)
            # Rest of your code
        except TimeoutException:
            print("Page load timed out. Proceeding with the next link.")
            return True
        try:
            # Wait for the dynamic content to load
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_7-ncAO"))
            )

            # Find the target div
            target_div = driver.find_element(By.CLASS_NAME, "_7-ncAO")

            # Check if the required text is in the div or its children
            if "plus à la mode" in target_div.get_attribute('innerHTML'):
                print("  link "+str(link)+" because we can see plus à la mode")
                return True
        except:
            return False
    elif source == "forever21":
        return False
    else:
        return False

def sanity_check():
    client = pymongo.MongoClient(config_server.db_uri)
    db = client[config_server.db_name]
    catalogue = db[config.catalogue_name]
    item_without_id = 0
    elem_without_reference = 0
    elem_without_type = 0
    nbr_None_links =0
    elem_without_gender = 0
    nbr_items_by_gender = {}
    nbr_broken_links={}
    nbr_items_by_type={}
    broken_links={}
    driver = webdriver.Chrome() 
    driver.set_page_load_timeout(10)
    total_docs = catalogue.count_documents({})
    i = 0
    for item in catalogue.find():
        i+=1
        if(i%50==0):
            print(str(i*100/total_docs)+" %")
        if "id" not in item:
            item_without_id +=1
        else:
            id = item["id"]
            if IDinReference(id):
                link = getLinkFromReference(id)
                if link == None:
                    nbr_None_links +=1
                elif isBrokenLink(link,item["source"],driver):
                    nbr_broken_links[item["source"]] = nbr_broken_links.get(item["source"], 0) + 1
                    if(item["source"] not in broken_links):
                        broken_links[item["source"]]= set()
                    broken_links[item["source"]].add(link)
                else:
                    item_type = item.get("type")
                    if item_type is not None:
                        nbr_items_by_type[item_type] = nbr_items_by_type.get(item_type, 0) + 1
                    else:
                        elem_without_type+=1
                    
                    item_gender = item.get("gender")
                    if item_gender is not None:
                        nbr_items_by_gender[item_gender] = nbr_items_by_gender.get(item_gender, 0) + 1
                    else:
                        elem_without_gender+=1
            else:
                elem_without_reference+=1

    print("item_without_id")
    print(item_without_id)
    print("elem_without_reference")
    print(elem_without_reference)
    print("elem without type :")
    print(elem_without_type)
    print("elem without gender :")
    print(elem_without_gender)
    print("nbr_None_links")
    print(nbr_None_links)
    print("nbr_broken_links")
    print(nbr_broken_links)
    print("nbr_items_by_type")
    print(nbr_items_by_type)
    print("nbr_items_by_gender")
    print(nbr_items_by_gender)
    print("Do you want to fix broken links ? ")
    driver.quit()

    with open('broken_links.pickle', 'wb') as handle:
        pickle.dump(broken_links, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return broken_links

def delete_documents_by_link(collection_name,link):
    client = pymongo.MongoClient(config.db_uri)
    db = client[config.db_name]  
    collection = db[collection_name]  
    query = {"link": link}
    result = collection.delete_many(query)
    query2 = {"url": link}
    result2 = collection.delete_many(query2)
    # Print how many documents were deleted
    print(f"Documents deleted: {result.deleted_count+result2.deleted_count}")
    return result.deleted_count+result2.deleted_count

def fix_zalando_links(list_of_links):
    deleted_docs =0
    deleted_docs2 =0
    for link in list_of_links:
        deleted_docs = delete_documents_by_link(config_server.catalogue_name, link)
        deleted_docs2 = delete_documents_by_link(config_server.reference_name, link)
    if(deleted_docs ==0 and deleted_docs2==0):
        print("links already fixed")
        return 0
    client = pymongo.MongoClient(config_server.db_uri)
    db = client[config_server.db_name]
    collection = db[config_server.reference_name]
    total_documents_before_fix = collection.count_documents({})
    number_of_links = str(len(list_of_links)) 
    command = ['python', 'ZALANDO_SCRAPER/zalando.py', number_of_links]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # You can check result.returncode, result.stdout, result.stderr for the command execution status and output
    if result.returncode == 0:
        print("Zalando script executed successfully")
    else:
        print("Error executing Zalando script:", result.stderr)
    total_documents_after_fix = collection.count_documents({})
    return total_documents_after_fix-total_documents_before_fix

def fix_forever21_links(list_of_links):
    for link in list_of_links:
        delete_documents_by_link(config_server.catalogue_name, link)
        delete_documents_by_link(config_server.reference_name, link)
    client = pymongo.MongoClient(config_server.db_uri)
    db = client[config_server.db_name]
    collection = db[config_server.reference_name]
    total_documents_before_fix = collection.count_documents({})
    number_of_links = str(len(list_of_links)) 
    command = ['python', 'FOREVER21_SCRAPER/forever21.py', number_of_links]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # You can check result.returncode, result.stdout, result.stderr for the command execution status and output
    if result.returncode == 0:
        print("Forever21 script executed successfully")
    else:
        print("Error executing Forever21 script:", result.stderr)
    total_documents_after_fix = collection.count_documents({})
    return total_documents_after_fix-total_documents_before_fix

def fix_broken_links():
    try:
        with open('broken_links.pickle', 'rb') as handle:
            broken_links = pickle.load(handle)
    except FileNotFoundError:
        print("The file 'broken_links.pickle' was not found, please perform a sanity check first")
        return 0
    
    total_fixed_links = 0
    for source in broken_links:
        if source=="zalando":
            total_fixed_links+=fix_zalando_links(broken_links[source])
        elif source=="forever21":
            total_fixed_links+=fix_forever21_links(broken_links[source])
        else:
            print("unknown source")

    print(str(total_fixed_links)+" links have been fixed ! ")

def main():
    while True:
        print("\nChoose an option (enter the number):")
        print("1. catalogue sanity check ")
        print("2. fix broken links ")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            sanity_check()
        elif choice == 2:
            fix_broken_links()
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 3.")

if __name__ == "__main__":
    main()