from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Helpers.Logger import get_logger
import os

class Database:
    def __init__(self):
        self.logger = get_logger()
        self.engine = create_async_engine(
            os.getenv("DB_CONNECTION_STRING"),
            echo=True,
            fast_executemany=True,
            pool_size=7,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            connect_args={"timeout": 15} 
        )
        self.session_local= sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=True
        )

    def get_session(self):
        try:
            return self.session_local()
        except Exception as e:
            self.logger.error(f"Failed to create dB session: {e}")
            raise