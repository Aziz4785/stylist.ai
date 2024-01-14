from ScraperFactory import *
from JsonWritingImpl import *
import os

def main():
    print("Current Working Directory: " + os.getcwd())
    with open("zalando_links", "r") as file:
        links = file.readlines()
    
    links = ["https://www.zalando.fr/streetwear-homme/","https://www.zalando.fr/luxe-homme/","https://www.zalando.fr/sport-homme/"]
    for link in links:
        print("scraping link "+link)
        collection_name=f"data_{link.split('/')[-2]}"
        scraper = ScraperFactory.create_scraper(link.strip(),IncrementalJsonWritingStrategy(collection_name))
        data = scraper.scrape(max_pages=1,half_of_last_page = False)
        

if __name__ == "__main__":
    main()