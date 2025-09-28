import os
from IngestionWorker.Services.BaseScrapper import BaseScrapper
from IngestionWorker.Schema.OtodomSchema import OFFERS_SCHEMA, TOTAL_PAGES_SCHEMA, OFFER_SCHEMA
from crawl4ai import JsonCssExtractionStrategy

class OtoDomScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(os.getenv("OTODOM_URL"),"/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow?page=")

    async def start(self):
        self.logger.info("Starting OtoDom Scrapper")
        await self.get_total_pages(JsonCssExtractionStrategy(TOTAL_PAGES_SCHEMA),wait_for="css:ul[data-cy='nexus-pagination-component']")
        self.prepare_offers_page_url()
        await self.get_offers_urls(JsonCssExtractionStrategy(OFFERS_SCHEMA), wait_for="css:a[data-cy='listing-item-link']")
        await self.get_offer_info(JsonCssExtractionStrategy(OFFER_SCHEMA), wait_for="css:main")