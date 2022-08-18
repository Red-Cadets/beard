from config import get_config
from db import get_database


from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import CollectionInvalid


config = get_config()


class Scraper:
    db_client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    def __init__(self, ctfname, url) -> None:
        self.ctfname = ctfname.replace(" ", "_")
        self.url = url

    async def prepare(self):
        db_manager = await get_database()
        self.db_client = db_manager.client
        self.db = db_manager.client[self.ctfname]
        await self.create_config_collection()
        

    async def create_config_collection(self):
        async with await self.db_client.start_session() as s:
            try:
                await self.db.create_collection('config', capped=True, size=1000, max=1)
            except CollectionInvalid:
                pass


    async def scrap(self):
        print("SCRAPING DATA...")


class TaskBasedScraper(Scraper):
    def __init__(self, ctfname, url) -> None:
        super().__init__(ctfname, url)


class ADScraper(Scraper):
    def __init__(self, ctfname, url) -> None:
        super().__init__(ctfname, url)
