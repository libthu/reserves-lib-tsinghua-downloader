import asyncio
import aiohttp
from utils.http import SessionTHU


async def fetch(url: str, session: aiohttp.ClientSession) -> bytes:
    async with session.get(url) as ret:
        return await ret.content.read()


async def fetch_concurrent(urls, img_list, cookies, headers) -> None:
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for u in urls:
            tasks.append(loop.create_task(fetch(u, session)))
        for ret in asyncio.as_completed(tasks):
            img = await ret
            img_list.append(img)


def concurrent_download(file_list, img_list, session: SessionTHU, concurrent: int) -> None:
    cookies = session.s.cookies
    headers = session.s.headers
    urls_generator = (file_list[i:i + concurrent] for i in range(0, len(file_list), concurrent))
    for urls in urls_generator:
        asyncio.run(fetch_concurrent(urls, img_list, cookies, headers))
