import aiohttp
import asyncio
import random
import logging; logger = logging.getLogger('REQUEST')

DEFAULT_HTTP_ATTEMPTS = 3
DEFAULT_TIMEOUTS = (1,3)

async def get(url, headers = {}):
    """ str ->> bool
    Run GET query with  the ability to specify a timeout
    Args:
        url (str): query URL
    return True- Returns true if execution succeeds.
           False - otherwise
    """
    global DEFAULT_HTTP_ATTEMPTS, DEFAULT_TIMEOUTS
    current_attempt = 0
    result={"code":None, "content":None, "json":None}
    async with aiohttp.ClientSession() as session:
        while current_attempt < DEFAULT_HTTP_ATTEMPTS:
            try:
                async with session.get(url=url, headers=headers) as response:
                    result["code"] = response.status
                    if 200 <= response.status <= 299:
                        result["content"] = await response.text()
                        result["json"] = None
                        break
                    else:
                        logger.error("~HTTP GET Query. Attempt:{} Url:{}  Error:{}".
                                     format(current_attempt, url, response.status))
                        current_attempt += 1
                        await asyncio.sleep(random.randint(*DEFAULT_TIMEOUTS))
                        continue
            except Exception as exc:
                logger.error("HTTP GET Query. Attempt:{} Url:{}  Error:{}".
                             format(current_attempt, url, exc))
                current_attempt+=1
                await asyncio.sleep(random.randint(*DEFAULT_TIMEOUTS))
                continue
    await asyncio.sleep(random.randint(*DEFAULT_TIMEOUTS))
    return result
