import websockets
import threading
import asyncio
import json

CLIENTS = set()


async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
        except:
            return
        if data.get('type') == 'connect':
            CLIENTS.add(websocket)
        if data.get('type') == 'updated':
            for ws in CLIENTS:
                try:
                    await ws.send(json.dumps(data.get('data')))
                except:
                    continue


async def main():
    async with websockets.serve(handler, "0.0.0.0", 9090):
        await asyncio.Future()


async def updated(info='', team_info=''):
    async with websockets.connect('ws://127.0.0.1:9090') as websocket:
        if team_info.get('_id'):
            del(team_info['_id'])
        if info.get('_id'):
            del(info['_id'])
        await websocket.send(json.dumps({'type': 'updated', 'data': {'team_info': team_info, 'info': info}}))

ws_server = threading.Thread(target=asyncio.run, args=(main(),), daemon=True)
ws_server.start()
