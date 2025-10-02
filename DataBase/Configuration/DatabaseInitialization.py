from DataBase.Configuration.Database import Database
from Helpers.Logger import get_logger
from DataBase.TableModels.SecondaryMarketTableModel import Base
import asyncio

class DatabaseInitialization:
    def __init__(self):
        self.max_retries = 5
        self.retry_delay = 5
        self.db = Database()
        
    async def initialize_dB(self)-> Database:
        for attempt in range(self.max_retries):
            try:
                get_logger().info("Starting dB initialization")
                async with self.db.engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                get_logger().info("dB initialization success")
                return self.db
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                get_logger().error(f"Database initialization failed on attempt {attempt + 1}: {e}")

    async def close_dB_connection(self):
        try:
            
            await self.db.engine.dispose()
            get_logger().info("dB connection closed succesfully")
        except Exception as e:
            get_logger().error(f"Failed to close dB connection: {e}")