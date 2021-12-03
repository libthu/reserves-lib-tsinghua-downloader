import time
import re

import requests

from utils.concurrent import concurrent_download


def is_available(url: str, session: requests.Session) -> bool:
    ret = session.get(url)
    if 'safedog' in ret.text:
        return False
    else:
        return True


def get_chapter_list(index_url: str, session: requests.Session) -> list[str]:
    id = 0
    chapter_list = []
    while True:
        if not is_available(index_url.format(id), session):
            # In case the index is not continuous.
            for _ in range(10):
                id += 1
                if is_available(index_url.format(id), session):
                    break
            else:
                break
        chapter_list.append(id)
        id += 1
    return chapter_list


# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/mobile/index.html'
# config.js: http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/mobile/javascript/config.js
def get_page_cnt(url: str, session: requests.Session) -> int:
    pattern = 'bookConfig.totalPageCount=(.*?);'
    js_url = url + '/mobile/javascript/config.js'
    ret = session.get(js_url)
    page_cnt = int(re.search(pattern, ret.text).group(1))
    return page_cnt


def claw(url: str, session: requests.Session, concurrent: int) -> dict[int, list[bytes]]:
    print('Clawing...')

    chapter_id = int(url[-3:])
    index_url = url[:-3] + '{:03d}/index.html'
    image_base_url = 'http://' + url[7:-3].replace('//', '/')

    total_page = 0
    total_time = 0
    imgs = {}
    chapter_list = get_chapter_list(index_url, session)
    for chapter_id in chapter_list:
        print(f'Clawing chapter {chapter_id}')
        image_url = image_base_url + f'{chapter_id:03d}/files/mobile/{{}}.jpg'
        time_usage = time.time()

        page_cnt = get_page_cnt(url, session)
        page_list = [image_url.format(i) for i in range(1, page_cnt + 1)]

        img_list = concurrent_download(page_list, session, concurrent)

        imgs[chapter_id] = img_list
        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += page_cnt
        print(f'Clawed {len(img_list)} pages, time usage:{time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total, time usage:{total_time: .3f}s')
    return imgs
