from dotenv import load_dotenv
load_dotenv()
from Helpers.Logger import get_logger
import asyncio
from IngestionWorker.Services.OtoDomScrapper import OtoDomScrapper

async def main():
    try:
        scrapper = OtoDomScrapper()
        scrapped_data = await scrapper.start()
    except Exception as e:
        get_logger().error(f"Error in main: {e}")

    
if __name__ == "__main__":
    asyncio.run(main())




