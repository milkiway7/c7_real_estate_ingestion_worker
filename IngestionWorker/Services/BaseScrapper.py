import json
from Helpers.Logger import get_logger
from abc import ABC
from crawl4ai import (AsyncWebCrawler, BrowserConfig, 
                      JsonCssExtractionStrategy, CrawlerRunConfig, 
                      CacheMode, CrawlResult, MemoryAdaptiveDispatcher)

class BaseScrapper(ABC):
    def __init__(self, domain: str, url_offers_page: str):
        self.logger = get_logger(self.__class__.__name__)
        self.page_number = None
        self.browser_cfg = BrowserConfig(headless=True)
        self.crawler_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            remove_overlay_elements=True,
            magic=True,                   
            verbose=True,
        )
        self.domain = domain
        self.url_offers_page = url_offers_page
        self.offers_page_urls = set()
        self.offers_urls = set()
        self.scrapped_data = []
        self.dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=80,
            max_session_permit=10
        )
    
    async def get_total_pages(self, extraction_strategy: JsonCssExtractionStrategy, wait_for: str):
        try:
            self.crawler_cfg.wait_for = wait_for
            self.crawler_cfg.extraction_strategy = extraction_strategy
            offers_page_url = f"{self.domain}{self.url_offers_page}1"
            self.logger.info(f"Getting number of total pages from {self.domain}")
            async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
                result:CrawlResult = await crawler.arun(offers_page_url, config=self.crawler_cfg)
                if result.success:
                    data = json.loads(result.extracted_content or [])
                    if not data:
                        self.logger.info("Number of total pages: 0")
                        self.page_number = 0
                    self.page_number = int(data[0]["numberOfPages"])
                    self.logger.info(f"Successfully got number of total pages: {self.page_number}")
                else:
                    self.logger.error(f"Failed to get number of total pages: {result.error_message}")
        except Exception as e:
            self.logger.error(f"Error in get_total_pages: {e}")
            raise
    
    def prepare_offers_page_url(self):
        try:
            if self.page_number is None:
                raise ValueError("Page number is not set. Call get_total_pages first.")
            # ZMIENIĆ NA for i in range(1, self.page_number + 1):
            for i in range(1, 51):  # Tymczasowo ograniczone do 1 stron dla testów
            # for i in range(1, self.page_number + 1):
                self.offers_page_urls.add(f"{self.domain}{self.url_offers_page}{i}")
            self.logger.info(f"Prepared {len(self.offers_page_urls)} offers page URLs.")
        except Exception as e:
            self.logger.error(f"Error in prepare_offers_page_url: {e}")
            raise

    async def get_offers_urls(self, extraction_strategy: JsonCssExtractionStrategy, wait_for: str):
        try:
            self.crawler_cfg.wait_for = wait_for
            self.crawler_cfg.extraction_strategy = extraction_strategy
            async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
                results = await crawler.arun_many(
                    urls = list(self.offers_page_urls),
                    config = self.crawler_cfg,
                    dispatcher = self.dispatcher
                )
            # TO NIE DZIAŁA BO NIE MA success NA LISTACH
            # if not results.success: 
            #     self.logger.error("Failed to get offers URLs")
            for result in results:
                data = json.loads(result.extracted_content or "[]")
                scrapped_urls = {f"{self.domain}{row["offerUrl"]}" for row in data if row.get("offerUrl")}
                self.offers_urls.update(scrapped_urls)
            self.logger.info(f"Total unique offers URLs collected: {len(self.offers_urls)}")
        except Exception as e:
            self.logger.error(f"Error in get_offers_urls: {e}")
            raise
    
    async def get_offer_info(self, extraction_strategy: JsonCssExtractionStrategy, wait_for: str):
        try:
            
            self.crawler_cfg.wait_for = wait_for
            self.crawler_cfg.extraction_strategy = extraction_strategy
            async with AsyncWebCrawler(config=self.browser_cfg) as crawler:
                results = await crawler.arun_many(
                    urls = list(self.offers_urls),
                    config = self.crawler_cfg,
                    dispatcher = self.dispatcher
                )
            for result in results:
                # Pojedyńcza oferta
                data = json.loads(result.extracted_content or "[]")
                if data:
                    self.scrapped_data.append({"data":data[0],
                                               "url": result.url})
            self.logger.info(f"Total data collected: {len(self.scrapped_data)}")
            return self.scrapped_data
        except Exception as e:
            self.logger.error(f"Error in get_offer_info: {e}")
            raise
            
