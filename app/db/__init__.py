import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger("uvicorn")

class MongoManager():
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client.main_db
        logger.info("Connected to MongoDB")

    async def close_database_connection(self):
        logger.info("Closing connection with MongoDB")
        self.client.close()
        logger.info("Closed connection with MongoDB")

db = MongoManager()


async def get_database() -> MongoManager:
    return db