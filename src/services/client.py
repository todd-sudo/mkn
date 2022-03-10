import asyncio
from typing import Optional, Any

import aiohttp
from .logger import logger


async def async_get(
        session: aiohttp.ClientSession,
        url: str,
        headers=None,
        cookies=None
):
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    # for proxy in random.sample(proxy_list, len(proxy_list)):
    #     try:
    async with session.get(
        url=url, headers=headers, cookies=cookies,  # proxy=proxy
    ) as res:
        print(res.status)
        if res.status != 200:
            logger.error(f"Status code {res.status} != 200")
        return await res.text()
        # except Exception as e:
        #     logger.error(e)
        #     continue


async def async_post(
        session: aiohttp.ClientSession,
        url: str,
        json: Any,
        headers=None,
        cookies=None
):
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    async with session.post(
        url=url, json=json, headers=headers, cookies=cookies,
    ) as res:
        print(f"Status code = {res.status}")
        if res.status != 200:
            logger.error(f"Status code {res.status} != 200")
            await asyncio.sleep(10)
        return await res.text()
