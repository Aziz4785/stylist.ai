import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scraper_util.ScraperFactory import ScraperFactory
from scraper_util.WritingImpl import IncrementalWritingStrategy
import requests
import config

def main():
    
    with open("forever21_links", "r") as file:
        lines = file.readlines()
    
    for line in lines:
            parts = line.strip().split(' ')
            link = parts[0]
            type = parts[1]
            gender = parts[2]
            collection_name=config.collection_name_start_with+f"_{link.split('/')[-1]}"
            scraper = ScraperFactory.create_scraper(link.strip(),IncrementalWritingStrategy(collection_name))
            data = scraper.scrape(nbr_items=20,type=type,gender=gender)
        

if __name__ == "__main__":
    main()