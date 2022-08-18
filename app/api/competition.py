from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from db import get_database
from schemas.config import Config

router = APIRouter()

# TODO: Расширить схему конфига цтф
@router.get('/config', response_model=Config)
async def get_config(ctfname: str = "RC CTF", db_manager = Depends(get_database)):
    db = db_manager.client[ctfname.replace(" ", "_")]
    collection = db.config
    data = await collection.find_one({}, {"_id":0})
    config_obj = Config.parse_obj(data)
    return config_obj

@router.get('/teams')
async def get_teams(ctfname: str = "RC CTF", db_manager = Depends(get_database)):
    db = db_manager.client[ctfname.replace(" ", "_")]
    collection = db.teams
    cur = collection.find({}, {"_id":0})
    data = await cur.to_list(None)
    print(data)
    return JSONResponse(data)

@router.get('/teams/{team_id:int}')
async def get_teams(team_id, ctfname: str = "RC CTF", db_manager = Depends(get_database)):
    db = db_manager.client[ctfname.replace(" ", "_")]
    collection = db.teams
    cur = await collection.find_one({"id": team_id}, {"_id":0})
    return JSONResponse(cur)
