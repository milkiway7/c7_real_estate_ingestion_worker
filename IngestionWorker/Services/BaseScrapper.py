import json
from Helpers.Logger import get_logger
from abc import ABC
from crawl4ai import (AsyncWebCrawler, BrowserConfig, 
                      JsonCssExtractionStrategy, CrawlerRunConfig, 
                      CacheMode, CrawlResult)

class BaseScrapper(ABC):
    def __init__(self, url: str, schema):
        self.logger = get_logger(self.__class__.__name__)
        self.page_number = None
        self.browser_cfg = BrowserConfig(headless=False)
        self.crawler_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            remove_overlay_elements=True,
            magic=True,                   
            verbose=True,
            extraction_strategy=JsonCssExtractionStrategy(schema)
        )
        self.url = url

    async def get_total_pages(self, wait_for: str):
        self.crawler_cfg.wait_for = wait_for
        offers_page_url = f"{self.url}/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow"
        self.logger.info(f"Getting total pages from {self.url}")
        async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
            result:CrawlResult = await crawler.arun(offers_page_url, config=self.crawler_cfg)
            if result.success:
                data = json.loads(result.extracted_content or [])
                if not data:
                    self.logger.info("Total pages: 0")
                    self.page_number = 0
                self.page_number = data[0]["numberOfPages"]
                self.logger.info(f"Successfully got total pages: {self.page_number}")
            else:
                self.logger.error(f"Failed to get total pages: {result.error_message}")

    def clean_url_duplicates(self):
        pass

    async def get_offers_urls(self, wait_for: str):
        self.crawler_cfg.wait_for = wait_for

    async def get_offer_info(self, wait_for: str):
        self.crawler_cfg.wait_for = wait_for
