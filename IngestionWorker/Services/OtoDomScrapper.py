import os
from IngestionWorker.Services.BaseScrapper import BaseScrapper
from IngestionWorker.Schema.OtodomSchema import OFFERS_SCHEMA, TOTAL_PAGES_SCHEMA, OFFER_SCHEMA
class OtoDomScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(os.getenv("OTODOM_URL"),TOTAL_PAGES_SCHEMA)

    async def start(self):
        self.logger.info("Starting OtoDom Scrapper")
        await self.get_total_pages(wait_for="css:ul[data-cy='nexus-pagination-component']")