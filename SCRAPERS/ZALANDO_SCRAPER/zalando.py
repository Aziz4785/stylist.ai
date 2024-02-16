from scraper_util.ScraperFactory import *
from scraper_util.JsonWritingImpl import *
import sys, os
import argparse
import config
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def process_line(link, type, gender, nbr_items):
    collection_name = config.collection_name_start_with + f"_{link.split('/')[-2]}"
    scraper = ScraperFactory.create_scraper(link, IncrementalJsonWritingStrategy(collection_name))
    data = scraper.scrape(nbr_items=nbr_items, type=type, gender=gender)
    print("scraping report : ")
    print(scraper.scraping_report)

def divide_equally(number, nbr_of_parts):
    # Handle edge cases first
    if nbr_of_parts == 0:
        return []
    if number == 0:
        return [0] * nbr_of_parts

    # Calculate quotient and remainder
    quotient, remainder = divmod(number, nbr_of_parts)

    # Create the initial list with all elements set to quotient
    parts = [quotient] * nbr_of_parts

    # Distribute the remainder across the first N elements
    for i in range(remainder):
        parts[i] += 1

    random.shuffle(parts)
    return parts

def main(nbr_items, link=None, item_type=None, gender=None):
    print("Current Working Directory: " + os.getcwd())
    lines = []

    if link:
        process_line(link, item_type, gender, nbr_items)
    else:
        with open("./zalando_links", "r") as file:
            lines = file.readlines()
            product_by_page = divide_equally(nbr_items,len(lines))
            for i,line in enumerate(lines):
                parts = line.strip().split(' ')
                link = parts[0]
                type = parts[1]
                gender = parts[2]
                print("we will extract "+str(product_by_page[i])+" items from "+str(link))
                print("and we will pu gender = "+str(gender))
                print()
                process_line(link, type, gender, product_by_page[i])
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape data from Zalando.')
    parser.add_argument('nbr_items', type=int, help='Number of items to scrape')
    parser.add_argument('--link', type=str, help='Optional link for scraping', default=None)
    parser.add_argument('--type', dest='item_type', type=str, help='type of the scraped items', default=None)
    parser.add_argument('--gender', type=str, help='Gender of the scraped items', default=None)

    args = parser.parse_args()

    main(args.nbr_items, args.link, args.item_type, args.gender)
    #example : python zalando.py 20 to get 20 items from zalando
    #python zalando.py 20 --link "your_specific_link" --type="men" to get 20 item from the specific link and put "men" in their metadata