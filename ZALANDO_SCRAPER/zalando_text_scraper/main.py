from ScraperFactory import *
from JsonWritingImpl import *
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def main():
    print("Current Working Directory: " + os.getcwd())
    with open("zalando_links", "r") as file:
        links = file.readlines()
    
    links = ["https://www.zalando.fr/streetwear-femme/","https://www.zalando.fr/luxe-femme/","https://www.zalando.fr/sport-femme/"]
    for link in links:
        print("scraping link "+link)
        collection_name=f"data_{link.split('/')[-2]}"
        scraper = ScraperFactory.create_scraper(link.strip(),IncrementalJsonWritingStrategy(collection_name))
        data = scraper.scrape(max_pages=1,half_of_last_page = False)
        

if __name__ == "__main__":
    main()