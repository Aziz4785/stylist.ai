from .scrapers import Scraper
class ScraperFactory:
    """
    Factory for creating scrapers based on URL.
    """
    @staticmethod
    def create_scraper(url,writing_strategy):
        return Scraper(url,writing_strategy)