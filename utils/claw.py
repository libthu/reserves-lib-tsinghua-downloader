import time
import sys

import requests

from utils.concurrent import concurrent_download
from utils.http import get_file_list


def claw_book4(url: str, concurrent: int, session: requests.Session):

    print('Fetching chapters...')

    chapter_list = get_file_list(url, session)
    print(f'Found {len(chapter_list)} chapters.')

    print(f'Clawing with {concurrent} thread(s)...')

    total_page = 0
    total_time = 0
    imgs = {}
    for chapter_url in chapter_list:
        chapter_id = chapter_url[-12:-1]
        print(f'Clawing chapter {chapter_id}')
        time_usage = time.time()
        page_list = [
            'http://reserves.lib.tsinghua.edu.cn' + url
            for url in get_file_list('http://reserves.lib.tsinghua.edu.cn' + chapter_url + 'files/mobile/', session)
        ]
        page_list.sort(key=lambda url: int(url[76:-4]))

        img_list = []
        concurrent_download(page_list, img_list, session, concurrent)

        imgs[chapter_id] = img_list
        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += len(img_list)
        print(f'Clawed {len(img_list)} pages, time usage:{time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total, time usage:{total_time: .3f}s')
    return imgs


def is_available(url: str, session: requests.Session) -> bool:
    ret = session.get(url)
    if ret.status_code in [200, 404]:
        return ret.status_code == 200
    print('Bad Internet connection')
    print('*' * 20)
    ret.raise_for_status()


def get_image(url: str, session: requests.Session) -> requests.Response:
    ret = session.get(url)
    if ret.status_code in [200, 404]:
        return ret
    print('Bad Internet connection')
    print('*' * 20)
    ret.raise_for_status()


def claw(url: str, session: requests.Session):

    print('Clawing...')

    chapter_id = int(url[-3:])
    url = url[7:-3]
    index_url = 'http://' + url + '{:03d}/index.html'
    image_base_url = 'http://' + url.replace('//', '/')

    total_page = 0
    total_time = 0
    imgs = {}
    while chapter_id <= 999:
        if not is_available(index_url.format(chapter_id), session):
            # In case the index is not continuous.
            for _ in range(20):
                chapter_id += 1
                if is_available(index_url.format(chapter_id), session):
                    break
            else:
                break
        print(f'Clawing chapter {chapter_id}')
        image_url = image_base_url + f'{chapter_id:03d}/files/mobile/{{}}.jpg'
        time_usage = time.time()

        cnt = 0
        img_list = []
        while True:
            ret = get_image(image_url.format(cnt + 1), session)
            if ret.status_code == 404:
                # Finished clawing a chapter.
                break
            img_list.append(ret.content)
            cnt += 1
            sys.stdout.write(f'Downloaded Page #{cnt}')
            sys.stdout.write('\r')
            sys.stdout.flush()

        imgs[chapter_id] = img_list
        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += len(img_list)
        print(f'Clawed {len(img_list)} pages, time usage:{time_usage: .3f}s')
        print('*' * 20)
        chapter_id += 1

    print(f'Clawed {total_page} pages in total, time usage:{total_time: .3f}s')
    return imgs
