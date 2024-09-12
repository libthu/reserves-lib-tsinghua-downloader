import asyncio
import time

import aiohttp
import requests
from tqdm import tqdm


async def fetch(file, session: aiohttp.ClientSession, order: int) -> tuple[bytes, int]:
    async with session.get(
        "https://ereserves.lib.tsinghua.edu.cn/readkernel/JPGFile/DownJPGJsNetPage",
        params={"filePath": file["hfsKey"]},
    ) as ret:
        return (await ret.content.read(), order)


async def fetch_concurrent(files: list, cookies, headers) -> list[bytes]:
    loop = asyncio.get_event_loop()
    imgs = [None] * len(files)

    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for i, u in enumerate(files):
            tasks.append(loop.create_task(fetch(u, session, i)))
        for ret in asyncio.as_completed(tasks):
            img, order = await ret
            imgs[order] = img

    return imgs


def concurrent_download(
    file_list: list, session: requests.Session, concurrent: int, interval: float
) -> list[bytes]:
    cookies = session.cookies
    headers = session.headers
    urls_generator = (
        file_list[i : i + concurrent] for i in range(0, len(file_list), concurrent)
    )

    img_list = []
    with tqdm(total=len(file_list), desc="Downloading", unit="page", ncols=100) as pbar:
        for files in urls_generator:
            loop = asyncio.get_event_loop()
            img_list += loop.run_until_complete(
                fetch_concurrent(files, cookies, headers)
            )
            pbar.update(len(files))
            time.sleep(interval)

    return img_list
