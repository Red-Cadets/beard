import asyncio
import uuid


from .scrapers.forcad import ForcADScraper

workers = dict()

def is_worker_exists(ctfname):
    for k in workers.keys():
        if workers[k].get('ctfname') == ctfname:
            return True
    return False

async def http_create_scraper(ctfname, url, stype, interval):
    if is_worker_exists(ctfname):
        return ""
    
    scraper = dict()
    if stype == 'forcad':
        scraper = ForcADScraper(ctfname, url)
    else:
        raise Exception(f"CTF board {stype} unavailable")
    await scraper.prepare()

    worker_task = asyncio.create_task(scrape_worker(scraper, interval))
    worker_id = str(uuid.uuid4())
    workers[worker_id] = {
        "task": worker_task,
        "ctfname": ctfname,
        "url": url
        }
    return worker_id


async def http_stop_scraper(worker_id):
    if worker_id in workers.keys():
        workers[worker_id].get("task").cancel()
        workers.pop(worker_id, None)
        return True
    return False


async def scrape_worker(scraper, interval):
    while True:
        await scraper.scrape()
        await asyncio.sleep(interval)


async def http_list_scrapers():
    workers_list = []
    for worker_id in workers:
        workers_list.append({
            "worker_id": worker_id,
            "ctfname": workers[worker_id].get('ctfname'),
            "url": workers[worker_id].get('url')
        })
    return workers_list
