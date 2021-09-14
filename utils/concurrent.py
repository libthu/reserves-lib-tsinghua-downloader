import asyncio
import sys

import aiohttp
import requests


async def fetch(url: str, session: aiohttp.ClientSession, order: int):
    async with session.get(url) as ret:
        return (await ret.content.read(), order)


async def fetch_concurrent(urls, cookies, headers):
    loop = asyncio.get_event_loop()
    imgs = [None] * len(urls)
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for i, u in enumerate(urls):
            tasks.append(loop.create_task(fetch(u, session, i)))
        for ret in asyncio.as_completed(tasks):
            img_with_order = await ret
            imgs[img_with_order[1]] = img_with_order[0]

    return imgs


def concurrent_download(file_list, img_list, session: requests.Session, concurrent: int) -> None:
    cookies = session.cookies
    headers = session.headers
    urls_generator = (file_list[i:i + concurrent] for i in range(0, len(file_list), concurrent))
    for urls in urls_generator:
        img_list += asyncio.run(fetch_concurrent(urls, cookies, headers))
        sys.stdout.write(f'Downloaded Page #{len(img_list)}')
        sys.stdout.write('\r')
        sys.stdout.flush()
