from dotenv import load_dotenv
load_dotenv()
import asyncio
from IngestionWorker.Services.OtoDomScrapper import OtoDomScrapper

async def main():
    scrapper = OtoDomScrapper()
    await scrapper.start()
    scrapper.prepare_offers_page_url()

    
if __name__ == "__main__":
    asyncio.run(main())




