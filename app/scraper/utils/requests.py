async def fetch(session, url):
    async with session.get(url) as resp:
        try:
          result = await resp.json()
          return result, resp.status
        except Exception as e:
          return {}, resp.status
