import aiohttp
from scraper.utils.requests import fetch
from scraper.scrapers import ADScraper
import asyncio
import logging
from itertools import groupby


logger = logging.getLogger("uvicorn")


class ForcADScraper(ADScraper):
    def __init__(self, ctfname, url) -> None:
        super().__init__(ctfname, url)
        self.ctf_config = dict()
        self.status = "offline"
        self.session = aiohttp.ClientSession(headers={'User-Agent': 'Scraper'})

    async def load_config(self):
        async with await self.db_client.start_session() as s:
            self.ctf_config, status_code = await fetch(self.session, self.url + '/api/client/config/')
            if status_code != 200:
                error_msg = "failed to load config"
                self.ctf_config["last_check_status"] = error_msg
            self.ctf_config["status"] = self.status
            await self.db.config.insert_one(self.ctf_config, session=s)

    async def update_config_status(self):
        async with await self.db_client.start_session() as s:
            self.ctf_config["status"] = self.status
            await self.db.config.find_one_and_update({}, {'$set': {'status': self.status}}, session=s)

    async def check_status(self):
        self.status, _ = await fetch(self.session, self.url + '/api/client/health/')
        self.status = "online" if self.status else "offline"
        await self.update_config_status()
        return self.status

    async def insert_or_update_team(self, team):
        async with await self.db_client.start_session() as s:
            id = team.get('id')
            old_team = await self.db.teams.find_one({'id': id}, session=s)
            new_team = {**old_team, **team} if old_team else team
            await self.db.teams.replace_one({'id': id}, new_team, upsert=True, session=s)

    async def load_teams(self):
        self.teams, _ = await fetch(self.session, self.url + '/api/client/teams/')
        await asyncio.gather(*map(self.insert_or_update_team, self.teams))

# TODO: создать отдельное поле с последним раундом "last_round": [{'task_id': 1, ...}, {'task_id': 2, ...}]
    async def load_team_rounds(self, team):
        async with await self.db_client.start_session() as s:
            id = team.get('id')
            rounds, status_code = await fetch(self.session, self.url + f'/api/client/teams/{id}/')
            if status_code != 200:
                error_msg = "failed to load team rounds"
                await self.db.teams.update_one({'id': id}, {'$set': {'last_check_status': error_msg}}, session=s)
                return
            grouped_rounds = group_dicts_by_task_id(rounds)
            await self.db.teams.update_one({'id': id}, {'$set': {'rounds': grouped_rounds, 'last_check_status': 'ok'}}, session=s)

    async def load_rounds(self):
        await asyncio.gather(*map(self.load_team_rounds, self.teams))

    async def update_team_rating(self, team):
        async with await self.db_client.start_session() as s:
            name = team.get('team')
            await self.db.teams.update_one({'name': name}, {'$set':
                                                            {
                                                                'pos': team.get('pos'),
                                                                'score': team.get('score'),
                                                            }
                                                            }, session=s)

    async def load_standing(self):
        self.standing, _ = await fetch(self.session, self.url + '/api/client/ctftime/')
        await asyncio.gather(*map(self.update_team_rating, self.standing))

    async def insert_or_update_service(self, service):
        id = service.get('id')
        await self.db.services.replace_one({'id': id}, service, upsert=True)

    async def load_services(self):
        self.services, _ = await fetch(self.session, self.url + '/api/client/tasks/')
        await asyncio.gather(*map(self.insert_or_update_service, self.services))

    async def scrape(self):
        if await self.check_status() == "online":
            logger.info(f'Scraping data from [{self.ctfname}] - [{self.url}]')
            await self.load_config()
            await self.load_teams()
            await self.load_standing()
            await self.load_services()
            await self.load_rounds()


def return_by_task_id(el): return el['task_id']
def return_by_timestamp(el): return el['timestamp']


def group_dicts_by_task_id(data):
    result = []
    sorted_list = sorted(data, key=return_by_task_id)
    for key, value in groupby(sorted_list, return_by_task_id):
        result.append(
            {"task_id": key, "values": sorted(
                list(value), key=return_by_timestamp)}
        )
    return result
