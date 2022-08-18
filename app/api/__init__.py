from fastapi import APIRouter
from api import competition, scraper

router = APIRouter()
router.include_router(competition.router, prefix='', tags=['competition'])
router.include_router(scraper.router, prefix='/scraper', tags=['scraper'])
