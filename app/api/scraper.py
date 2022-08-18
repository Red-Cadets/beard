from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from scraper import http_create_scraper, http_stop_scraper, http_list_scrapers

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_scraper(ctfname: str = "RC CTF", url: str = "http://redcadets.ru/ctf", stype: str = "ctfd", interval: int = 60):
    worker_id = await http_create_scraper(ctfname, url, stype, interval)
    if not worker_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "worker for this CTF already exists"})
    return {"worker_id": worker_id}

@router.delete('/', status_code=status.HTTP_200_OK)
async def stop_scraper(worker_id: str):
    result = await http_stop_scraper(worker_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "no such worker id"})

@router.get('/all')
async def get_all_workers():
    workers_list = await http_list_scrapers()
    return workers_list
