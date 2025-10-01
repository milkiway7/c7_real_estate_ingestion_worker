from DataBase.Configuration.Database import Database
from Helpers.Logger import get_logger

MAX_RETRIES = 5
MAX_DELAY = 5

async def initialize_dB():
    for attempt in MAX_RETRIES:
        try:
            get_logger().info("Starting dB initialization")
            db = Database()
            async with db.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            get_logger().info("dB initialization success")
        except Exception as e:
            get_logger().error("db initialization failed")
            raise