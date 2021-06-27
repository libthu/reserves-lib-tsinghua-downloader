import asyncio
import aiohttp
from utils.http import SessionTHU


def fetch_concurrent(files):
    pass


def concurrent_download(
    file_list, session: SessionTHU, concurrent: int, dir: str, chapter_id: str
) -> None:
    files_generator = (file_list[i:i + concurrent] for i in range(0, len(file_list), concurrent))
    for files in files_generator:
        asyncio.run(fetch_concurrent(files))
