from selenium import webdriver
import time
from .dal import inReference
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from translate import Translator
from deep_translator import GoogleTranslator
import config
import sys
import os

# Calculate the absolute path to the SCRAPER directory
current_script_path = os.path.dirname(os.path.abspath(__file__))
scrapers_dir_path = os.path.abspath(os.path.join(current_script_path, '..', '..'))

# Add the SCRAPER directory to the path if not already included
if scrapers_dir_path not in sys.path:
    sys.path.insert(0, scrapers_dir_path)

# Now you should be able to import id_generator directly
from id_generator import *

def add_hardcoded_metadata(product_data,type="-",gender="-"):
    if(type!="-" and type is not None and type!="null"):
        product_data["type"]=type
    if(gender!="-" and gender is not None and gender!="null"):
        product_data["gender"]=gender
    return product_data
  

class ProductPageScraper:
    """
    Class dedicated to scraping individual product pages.
    """
    def __init__(self, driver):
        self.driver = driver
        self.cookies_accepted = False
        #self.translator = Translator(to_lang="en", from_lang="fr")
        self.translator = GoogleTranslator(source='fr', target='en')
        self.scraping_report = {}

    def handle_cookie_consent(self):
        if not self.cookies_accepted:
            try:
                cookie_accept_button = self.driver.find_element(By.ID, "uc-btn-accept-banner")
                cookie_accept_button.click()
                self.cookies_accepted = True
                time.sleep(2)  # Wait for the overlay to disappear
            except NoSuchElementException:
                self.cookies_accepted = True
            except Exception as e:
                print(f"Error handling cookie consent: {e}")
    
    def extract_brand(self,url):
        return "Forever 21"
    
    def extract_images(self,url):
        """
        return the list of images of a product page 
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Error occurred while opening URL: {e}")
            return []

        # Find images
        try:
            container = self.driver.find_element(By.CLASS_NAME, 'product-thumbs')
            images = container.find_elements(By.TAG_NAME, 'img')
        except Exception as e:
            print(f"Error occurred while searching for images: {e}")
            return []

        srcs=[]
        try:
            srcs = [img.get_attribute('src') for img in images]
            if(len(srcs)>0):
                print("Image sources extracted successfully.")
        except Exception as e:
            print(f"Error occurred while extracting image sources: {e}")

        return srcs
    
    def extract_name(self,url):
        product_name=""
        try:
            product_name = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'pdp__name')]").text
        except:
            print(f"Product name not found for URL: {url}")
        return product_name
    
    def extract_material_and_care(self, url):
        metrialcare_text = ""

        try:
            # Wait for the div containing the details to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp__description .d_wrapper"))
            )

            # Find all d_wrapper sections
            d_wrappers = self.driver.find_elements(By.CLASS_NAME, 'd_wrapper')

            for wrapper in d_wrappers:
                # Check if the section contains <h3>Details</h3>
                h3 = wrapper.find_element(By.TAG_NAME, 'h3')
                if "Content" in h3.text or "Care" in h3.text:
                    # Extract the text from the corresponding d_content div
                    d_content = wrapper.find_element(By.CLASS_NAME, 'd_content')
                    metrialcare_text = d_content.text
                    break
        except Exception as e:
            print(f"An error occurred: {e}")

        return metrialcare_text
    
    def extract_sizefit(self, url):
        sizefit_text = ""

        try:
            # Wait for the div containing the details to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp__description .d_wrapper"))
            )

            # Find all d_wrapper sections
            d_wrappers = self.driver.find_elements(By.CLASS_NAME, 'd_wrapper')

            for wrapper in d_wrappers:
                # Check if the section contains <h3>Details</h3>
                h3 = wrapper.find_element(By.TAG_NAME, 'h3')
                if "Size" in h3.text or "Fit" in h3.text:
                    # Extract the text from the corresponding d_content div
                    d_content = wrapper.find_element(By.CLASS_NAME, 'd_content')
                    sizefit_text = d_content.text
                    break
        except Exception as e:
            print(f"An error occurred: {e}")

        return sizefit_text
    
    def extract_details(self,url):
        details_text = ""

        try:
            # Wait for the div containing the details to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp__description .d_wrapper"))
            )

            # Find all d_wrapper sections
            d_wrappers = self.driver.find_elements(By.CLASS_NAME, 'd_wrapper')

            for wrapper in d_wrappers:
                # Check if the section contains <h3>Details</h3>
                h3 = wrapper.find_element(By.TAG_NAME, 'h3')
                if "details" in h3.text.lower():
                    # Extract the text from the corresponding d_content div
                    d_content = wrapper.find_element(By.CLASS_NAME, 'd_content')
                    details_text = d_content.text
                    break
        except Exception as e:
            print(f"An error occurred: {e}")

        if details_text == "":
            print("cannot retrieve details from : "+str(url))
        return details_text

    def scrap_product_page(self, url):
        product_data = {"url": url} #object to store in the mongodb collection
        self.driver.get(url)
        time.sleep(2)
        
        #self.handle_cookie_consent()

        product_brand = self.extract_brand(url)
        if product_brand and len(product_brand)>0:
           product_data["brand"] = product_brand
        
        product_name = self.extract_name(url)
        if product_name and len(product_name)>0:
            product_data["name"] = product_name
        else:
            if("missing name" not in self.scraping_report):
                self.scraping_report["missing name"]=0
            self.scraping_report["missing name"]+=1

        material_and_care_text = self.extract_material_and_care(url)
        if material_and_care_text and len(material_and_care_text)>0:
            product_data["composition and care (en)"] = material_and_care_text
        else:
            if("missing composition" not in self.scraping_report):
                self.scraping_report["missing composition"]=0
            self.scraping_report["missing composition"]+=1

        product_details_text = self.extract_details(url)
        if product_details_text and len(product_details_text)>0:
            product_data["more details (en)"] = product_details_text
        else:
            if("missing details" not in self.scraping_report):
                self.scraping_report["missing details"]=0
            self.scraping_report["missing details"]+=1

        product_sizefit_text = self.extract_sizefit(url)
        if product_sizefit_text and len(product_sizefit_text)>0:
            product_data["size + fit (en)"] = product_sizefit_text
        else:
            if("missing fit" not in self.scraping_report):
                self.scraping_report["missing fit"]=0
            self.scraping_report["missing fit"]+=1

        images = self.extract_images(url)
        if(len(images)>0):
            product_data["images"] = images
        else:
            if("missing images" not in self.scraping_report):
                self.scraping_report["missing images"]=0
            self.scraping_report["missing images"]+=1

        return product_data

class Scraper:
    """
    Base class for all scrapers.
    """
    def __init__(self, url,writing_strategy):
        self.url = url
        self.driver = webdriver.Chrome()  # or any other driver
        self.cookies_accepted = False
        self.writing_strategy = writing_strategy
        self.product_page_scraper = ProductPageScraper(self.driver)
        self.scraping_report = {}
    
    def extract_links_from_page(self):
        print("now, we will extract links from a certain part of the page")
        unique_links = set()
        product_items = self.driver.find_elements(By.CSS_SELECTOR, ".product-grid__item .product-tile__anchor")
        print(" in this part of the page there are "+str(len(product_items))+" products we will iterate through them :")
        for item in product_items:
            href = item.get_attribute('href')
            _id = generate_ID(href)
            if href:
                if not inReference(config.reference_name,_id):
                    unique_links.add(href)
                else:
                    print("item already in reference")
        print(" we finally extracted "+str(len(unique_links))+" products")
        return unique_links

    def accept_cookies(self):
        try:
            cookie_accept_button = self.driver.find_element(By.ID, "uc-btn-accept-banner")
            cookie_accept_button.click()
            self.cookies_accepted = True
            time.sleep(2)
        except Exception as e:
            pass
    
    def expand(self,nbr_of_times=1):
        print("we will click on show-more "+str(nbr_of_times)+" times")
        for _ in range(nbr_of_times):
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'search-show-more'))
                )
                show_more_button = self.driver.find_element(By.CLASS_NAME, 'search-show-more')
                show_more_button.click()

                # Wait for a while to allow page to load new content
                WebDriverWait(self.driver, 5).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
            except TimeoutException:
                print("Timeout while waiting for the 'Show More' button.")
                return False
            except Exception as e:
                print(f"Could not find the button search-show-more. Error: {e}")
                return False
        
    def collect_products_link(self, nbr_items=20):
        all_unique_links = set()

        self.driver.get(self.url)
        time.sleep(2)

        k=1

        while len(all_unique_links) < nbr_items and k<20:
            print("so far we've collected : "+str(len(all_unique_links))+" links which is less than "+str(nbr_items))
            # Extract links from the current page
            all_unique_links.update(self.extract_links_from_page())

            #if not self.cookies_accepted:
                #self.accept_cookies()

            if(len(all_unique_links) < nbr_items):
                if not self.expand(nbr_of_times=k):
                    break
            
            k*=2

        if(len(all_unique_links) > nbr_items ):
            my_list = list(all_unique_links)

            my_list = my_list[:nbr_items]

            # Convert the list back to a set
            all_unique_links = set(my_list)

        print(f"Total item extracted: {len(all_unique_links)}")
        return all_unique_links
    
    def scrape(self, nbr_items=20,type="-",gender="-"):
        all_unique_links = self.collect_products_link(nbr_items=nbr_items) #len(all_unique_links) ~<= nbr_items
        for i, href in enumerate(all_unique_links):
            print("we scrape product n° "+str(i))
            product_data = self.product_page_scraper.scrap_product_page(href)
            product_data = add_id_to_document(product_data)
            product_data = add_hardcoded_metadata(product_data,type=type,gender=gender)
            self.writing_strategy.write(product_data)
        self.scraping_report=self.product_page_scraper.scraping_report



