import asyncio
import logging

import aiohttp
import backoff


@backoff.on_exception(backoff.expo,
                      aiohttp.errors.ClientError,
                      max_tries=8)
async def get_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

@backoff.on_exception(backoff.expo,
                      aiohttp.errors.ClientError,
                      max_tries=8)
@asyncio.coroutine
def get_url_py34(url):
    with aiohttp.ClientSession() as session:
        response = yield from session.get(url)
        try:
            return (yield from response.text())
        except Exception:
            response.close()
            raise
        finally:
            yield from response.release()


format_string = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(format=format_string, level=logging.DEBUG)

url = 'http://python.org/'
#url = 'http://localhost:34534/'

loop = asyncio.get_event_loop()
print(loop.run_until_complete(get_url_py34(url))[:100])
print(loop.run_until_complete(get_url(url))[:100])
