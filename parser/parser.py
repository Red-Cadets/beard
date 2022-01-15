#!/usr/bin/env python3

from datetime import datetime
from requestium import Session as Sess
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from pymongo import MongoClient
from bson.objectid import ObjectId
import asyncio
import coloredlogs
import logging
import os
import re
import time

from ws import ws
import game

coloredlogs.install()

def follow(game_obj, team_ip, driver, teamname):
    state = False
    while not state:
        state = game_obj.refresh(driver)
        time.sleep(2)
    if team_ip:
        return game_obj.get_delta_by_ip(team_ip)
    else:
        return game_obj.get_delta_by_name(teamname)

INFO = {}

SCOREBOARD = os.getenv('SCOREBOARD', 'http://6.0.0.1')
HEADLESS = True if os.getenv('TYPE', 'hackerdom') == "forcad" else False
TEAM = os.getenv('TEAM', 'Red Cadets')
MONGO_USER = os.getenv('MONGO_USER', 'parser')
MONGO_PASS = os.getenv('MONGO_PASS', 'parser')

if re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', TEAM) is None:
    TEAM_NAME = TEAM
    TEAM_IP = None
else:
    TEAM_NAME = None
    TEAM_IP = TEAM

if HEADLESS:
    s = Sess(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
        browser='chrome',
        default_timeout=15,
        webdriver_options={
                'arguments': [
                    'headless',
                    'disable-dev-shm-using',
                    'no-sandbox']})

    try:
        s.driver.get(SCOREBOARD)
    except Exception as e:
        logging.critical('Something went wrong: {} {}'.format(e, SCOREBOARD))
        exit(1)

    driver = s.driver
else:
    driver = None


mongo_client = MongoClient(
    "mongodb://{}:{}@mongo:27017/".format(MONGO_USER, MONGO_PASS))
db = mongo_client.parse

#? Данные всех команд
info = db.data

#? Данные отслеживаемой команды
teamInfo = db.team_info

AD = game.AD(TEAM_IP, driver, SCOREBOARD, TEAM_NAME)

# ? Получение информации по названию команды либо IP адресу
if TEAM_IP:
    AD.get_info_by_ip(TEAM_IP)
elif TEAM_NAME:
    AD.get_info_by_name(TEAM_NAME)

# ? Если нет информации о текущем раунде
res = info.find_one({"round": AD.round})
if not res:
    INFO['teams_info'] = AD.dump()
    INFO['round'] = AD.round
    INFO['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    INFO['_id'] = ObjectId()
    info.insert_one(INFO)
    logging.info('Inserted: {}'.format(AD.round))

    # ? Отправить всем клиентам изменения
    asyncio.run(ws.updated())

while True:
    try:
        team_info = follow(AD, TEAM_IP, driver, TEAM_NAME)
        INFO['teams_info'] = AD.dump()
        INFO['round'] = AD.round
        INFO['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        INFO['_id'] = ObjectId()
        info.insert_one(INFO)

        team_info['_id'] = ObjectId()
        teamInfo.insert_one(team_info)

        logging.info('Inserted: {}'.format(AD.round))

        asyncio.run(ws.updated(INFO, team_info))
    except Exception as e:
        logging.critical(e)
