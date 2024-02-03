from .scrapers import ShoesScraper,LuxeScraper,StreetwearScraper,ModeScraper,Scraper
class ScraperFactory:
    """
    Factory for creating scrapers based on URL.
    """
    @staticmethod
    def create_scraper(url,json_strategy):
        if "chaussures" in url:
            return ShoesScraper(url,json_strategy)
        elif "streetwear" in url:
            return StreetwearScraper(url,json_strategy)
        elif "luxe" in url:
            return LuxeScraper(url,json_strategy)
        elif "mode" in url:
            return ModeScraper(url,json_strategy)
        else:
            return Scraper(url,json_strategy)