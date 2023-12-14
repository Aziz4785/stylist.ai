from ScraperFactory import *
from JsonWritingImpl import *
import os

def main():
    print("Current Working Directory: " + os.getcwd())
    with open("zalando_links", "r") as file:
        links = file.readlines()

    links=["https://www.zalando.fr/streetwear-homme/","https://www.zalando.fr/luxe-homme/","https://www.zalando.fr/sport-homme/"]
    for link in links:
        print("scraping link "+link)
        scraper = ScraperFactory.create_scraper(link.strip(),IncrementalJsonWritingStrategy())
        data = scraper.scrape(1,f"output_json/data_{link.split('/')[-2]}.json")
        

if __name__ == "__main__":
    main()