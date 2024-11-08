from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from translate import Translator
from deep_translator import GoogleTranslator
from .dal import *
import sys
import os
import config_zalando
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#from SCRAPERS.id_generator import *

# Calculate the absolute path to the SCRAPER directory
current_script_path = os.path.dirname(os.path.abspath(__file__))
scrapers_dir_path = os.path.abspath(os.path.join(current_script_path, '..', '..'))

# Add the SCRAPER directory to the path if not already included
if scrapers_dir_path not in sys.path:
    sys.path.insert(0, scrapers_dir_path)

# Now you should be able to import id_generator directly
from id_generator import *
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
        product_Brand= ""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "FtrEr_"))
            )
            product_Brand = self.driver.find_element(By.CLASS_NAME, "FtrEr_").text
        except:
            print(f"Product brand not found for URL: {url}")

        return product_Brand
    
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
            div_class = "_5qdMrS WzZ4iu _01vVuu _6GQ88b WdG8Bv"
            images = self.driver.find_elements(By.CSS_SELECTOR, f'div.{div_class.replace(" ", ".")} img')
        except Exception as e:
            print(f"Error occurred while searching for images: {e}")
            return []

        srcs=[]
        try:
            srcs = [img.get_attribute('src') for img in images]
            #print("Image sources extracted successfully.")
        except Exception as e:
            print(f"Error occurred while extracting image sources: {e}")

        return srcs
    
    def extract_name(self,url):
        product_name=""
        try:
            product_name = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'sDq_FX')]").text
        except:
            print(f"Product name not found for URL: {url}")
        return product_name
    
    def extract_material_and_care(self, url):
        material_and_care_text = ""
        # Expand the material and care accordion and wait for content
        try:
            WebDriverWait(self.driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='pdp-accordion-material_care']/h2/button"))
            )
            accordion_button = self.driver.find_element(By.XPATH, "//div[@data-testid='pdp-accordion-material_care']/h2/button")
            accordion_button.click()
        except Exception as e:
            print(f"Material Accordion button not found for URL: {url}, Error: {e}")


        #extract material and care
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='pdp-accordion-material_care']/div"))
            )
            time.sleep(1)
            Material_and_care = self.driver.find_element(By.XPATH, "//div[@data-testid='pdp-accordion-material_care']/div")
            material_and_care_text = Material_and_care.text.replace("\n", ", ")
        except:
            print(f"Matiere et entretien not found for URL: {url}")
        return material_and_care_text
    
    def extract_details(self,url):
        product_details_text=""
         # Expand the accordion to reveal the details of the product
        try:
            accordion_button = self.driver.find_element(By.XPATH, "//div[@data-testid='pdp-accordion-details']/h2/button")
            accordion_button.click()
        except Exception as e:
            print(f" Details Accordion button not found for URL: {url}, Error: {e}")

        #extract details of the product
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='pdp-accordion-details']/div"))
            )
            time.sleep(1)
            product_details = self.driver.find_element(By.XPATH, "//div[@data-testid='pdp-accordion-details']/div")
            product_details_text = product_details.text
            product_details_text = product_details.text.replace("\n", ", ")
        except:
            print(f"product details not found for URL: {url}")
        
        return product_details_text

    def scrap_product_page(self, url):
        product_data = {"url": url} #document to store in the mongod colleciton
        self.driver.get(url)
        time.sleep(2)
        
        self.handle_cookie_consent()

        product_brand = self.extract_brand(url)
        if product_brand and len(product_brand)>0:
           product_data["brand"] = product_brand
           if("total_brands" not in self.scraping_report):
               self.scraping_report["total_brands"]=0
           self.scraping_report["total_brands"]+=1
        else:
            if("missing brands" not in self.scraping_report):
               self.scraping_report["missing brands"]=0
            self.scraping_report["missing brands"]+=1

        
        product_name = self.extract_name(url)
        if product_name and len(product_name)>0:
            product_data["name"] = product_name
            if("total name" not in self.scraping_report):
                self.scraping_report["total name"]=0
            self.scraping_report["total name"]+=1
        else:
            if("missing name" not in self.scraping_report):
                self.scraping_report["missing name"]=0
            self.scraping_report["missing name"]+=1


        
        material_and_care_text = self.extract_material_and_care(url)
        if material_and_care_text and len(material_and_care_text)>0:
            product_data["composition and care (fr)"] = material_and_care_text
            product_data["composition and care (en)"] = self.translator.translate(material_and_care_text)
            if("total material" not in self.scraping_report):
               self.scraping_report["total material"]=0
            self.scraping_report["total material"]+=1
        else:
            if("missing material" not in self.scraping_report):
               self.scraping_report["missing material"]=0
            self.scraping_report["missing material"]+=1
       
        product_details_text = self.extract_details(url)
        if product_details_text:
            product_data["more details (fr)"] = product_details_text
            product_data["more details (en)"] = self.translator.translate(product_details_text)
            if("total details" not in self.scraping_report):
               self.scraping_report["total details"]=0
            self.scraping_report["total details"]+=1
        else:
            if("missing details" not in self.scraping_report):
               self.scraping_report["missing details"]=0
            self.scraping_report["missing details"]+=1

        images = self.extract_images(url)
        if(len(images)>0):
            product_data["images"] = images
        else:
            if("missing images" not in self.scraping_report):
               self.scraping_report["missing images"]=0
            self.scraping_report["missing images"]+=1

        return product_data

class LuxeProductPageScraper(ProductPageScraper):
    def extract_brand(self,url):
        product_Brand= ""
        try :
            product_Brand = self.driver.find_element(By.XPATH, "//x-wrapper-re-1-4[@re-hydration-id='re-1-4']//h3[1]").text
            #product_Brand = self.driver.find_element(By.XPATH, "//div[contains(@class, '_5qdMrS')]//h3[1]").text
            #product_Brand2 = self.driver.find_element(By.XPATH, "//div[contains(@class, '_5qdMrS VHXqc_ rceRmQ _4NtqZU mIlIve')]//h3[1]").text
        except:
            pass

        return product_Brand
      
        
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
            div_class = "I7OI1O C3wGFf L5YdXz _0xLoFW _7ckuOK mROyo1 _5qdMrS"
            images = self.driver.find_elements(By.CSS_SELECTOR, f'div.{div_class.replace(" ", ".")} img')
        except Exception as e:
            print(f"Error occurred while searching for images: {e}")
            return []

        srcs=[]
        try:
            srcs = [img.get_attribute('src') for img in images]
        except Exception as e:
            print(f"Error occurred while extracting image sources: {e}")

        return srcs
    
    def extract_name(self,url):
        product_name= ""
        try :
            product_name = self.driver.find_element(By.XPATH, "//div[contains(@class, '_5qdMrS')]//h1[1]").text
        except:
            pass

        return product_name


# class StreetwearProductPageScraper(ProductPageScraper):
#     def extract_details(self,url):
#         print("extract_details for streetwear")
#         product_details_text=""
#         #extract details of the product
#         try:
#             WebDriverWait(self.driver, 5).until(
#                 EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='pdp-accordion-details']/div"))
#             )
#             time.sleep(1)
#             product_details = self.driver.find_element(By.XPATH, "//div[@data-testid='pdp-accordion-details']/div")
#             product_details_text = product_details.text
#             product_details_text = product_details.text.replace("\n", ", ")
#             if(product_details_text.strip() ==""):
#                 print("details are empty")
#             else:
#                 print("details : "+product_details_text)
#         except:
#             print(f"product details not found for URL: {url}")
        
#         return product_details_text

def add_hardcoded_metadata(product_data,type="-",gender="-"):
    if(type!="-" and type is not None and type!="null"):
        product_data["type"]=type
    if(gender!="-" and gender is not None and gender!="null"):
        product_data["gender"]=gender
    return product_data
  
class Scraper:
    """
    Base class for all scrapers.
    """
    def __init__(self, url,json_strategy):
        self.url = url
        self.driver = webdriver.Chrome()  # or any other driver
        self.cookies_accepted = False
        self.json_strategy = json_strategy
        self.product_page_scraper = ProductPageScraper(self.driver)
        self.scraping_report = {}

    def extract_links_from_whole_page(self):
        unique_links = set()
        item_divs = self.driver.find_elements(By.XPATH, "//div[contains(@class, '_5qdMrS w8MdNG cYylcv BaerYO _75qWlu iOzucJ JT3_zV _Qe9k6')]")
        for div in item_divs:
            children = div.find_elements(By.XPATH, "./*")
            if len(children) == 1 and children[0].tag_name == 'article':
                continue  # Skip ads
            if children[0].get_attribute('data-experiment-hint') == 'none':
                continue  # Skip creator ads

            links = div.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute('href')
                _id = generate_ID(href)
                if href:
                    if not inReference(config_zalando.reference_name,_id):
                        unique_links.add(href)
                    else:
                        print("item already in reference")
        
        return unique_links
    
    def accept_cookies(self):
        try:
            cookie_accept_button = self.driver.find_element(By.ID, "uc-btn-accept-banner")
            cookie_accept_button.click()
            self.cookies_accepted = True
            time.sleep(2)
        except Exception as e:
            pass
    
    def go_to_next_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@title='page suivante']"))
            )
            next_page_button = self.driver.find_element(By.XPATH, "//a[@title='page suivante']")
            next_page_button.click()
            time.sleep(4)
            return True
        except Exception as e:
            print(f"Could not find the next page button  Error: {e}")
            return False
        
    def collect_links_from_pages(self, nbr_items=20):
        all_unique_links = set()
        current_page = 1

        self.driver.get(self.url)
        time.sleep(2)
        while len(all_unique_links) < nbr_items and current_page<10:
            print("so far we've collected : "+str(len(all_unique_links))+" links which is less than "+str(nbr_items))
            # Extract links from the current page
            all_unique_links.update(self.extract_links_from_whole_page())

            if not self.cookies_accepted:
                self.accept_cookies()

            if(len(all_unique_links) < nbr_items):
                if not self.go_to_next_page():
                    break

            current_page += 1
        if(len(all_unique_links) > nbr_items ):
            my_list = list(all_unique_links)

            my_list = my_list[:nbr_items]

            # Convert the list back to a set
            all_unique_links = set(my_list)

        print(f"Total unique links extracted: {len(all_unique_links)}")
        return all_unique_links
    
    def scrape(self, nbr_items=20,type="-",gender="-"):
        all_unique_links = self.collect_links_from_pages(nbr_items=nbr_items)#len(all_unique_links) ~<= nbr_items
        for i, href in enumerate(all_unique_links):
            product_data = self.product_page_scraper.scrap_product_page(href)
            product_data = add_id_to_document(product_data)
            product_data = add_hardcoded_metadata(product_data,type=type,gender=gender)
            self.json_strategy.write_json(product_data)
        self.scraping_report=self.product_page_scraper.scraping_report


class ModeScraper(Scraper):
    def parse_html(self, html):
        pass

class LuxeScraper(Scraper):
    def __init__(self, url, json_strategy):
        print("Initializing LuxeScraper with URL:", url)
        super().__init__(url, json_strategy)
        self.product_page_scraper = LuxeProductPageScraper(self.driver)


class ShoesScraper(Scraper):
    """
    Scraper for shoe sections.
    """
    def parse_html(self, html):
        pass


class StreetwearScraper(Scraper):
    def __init__(self, url, json_strategy):
        print("Initializing StreetwearScraper with URL:", url)
        super().__init__(url, json_strategy)
        #self.product_page_scraper = StreetwearProductPageScraper(self.driver)


