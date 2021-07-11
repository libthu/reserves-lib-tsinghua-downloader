import os
import time
from argparse import ArgumentParser
from distutils.util import strtobool

import requests

from utils.http import get_file_list
from utils.concurrent import concurrent_download
from utils.cookie import get_cookie
from utils.pdf import generate_pdf
from utils.image import resize

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book6/00009127/00009127000/mobile/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def get_base_url(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('/index.html')):
        raise Exception('Invalid URL')
    url = url[7:]  # 'http://'
    url = url.replace('//', '/')
    url = url[:url.find('book') + 15]
    return 'http://' + url


def claw_book4(url: str, concurrent: int, session: requests.Session):

    print('Fetching chapters...')

    chapter_list = get_file_list(url, session)
    print(f'Found {len(chapter_list)} chapters')

    print('Clawing...')

    total_page = 0
    total_time = 0
    imgs = {}
    for chapter_url in chapter_list:
        chapter_id = chapter_url[-12:-1]
        print(f'Clawing chapter {chapter_id}')
        time_usage = time.time()
        page_list = [
            'http://reserves.lib.tsinghua.edu.cn' + url for url in get_file_list(
                'http://reserves.lib.tsinghua.edu.cn' + chapter_url + 'files/mobile/', session
            )
        ]

        img_list = []
        concurrent_download(page_list, img_list, session, concurrent)

        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += len(img_list)
        imgs[chapter_id] = img_list
        print(f'Clawed {len(img_list)} pages, time usage:{time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total, time usage:{total_time: .3f}s')
    return imgs


def is_available(url: str, session: requests.Session) -> bool:
    ret = requests.get(url)
    if ret.status_code in [200, 404]:
        return ret.status_code == 200
    print('*' * 20)
    print('Error: Bad Internet connection')
    print('*' * 20)
    ret.raise_for_status()


def claw(url: str, session: requests.Session):

    print('Fetching chapters...')

    chapter_list = get_file_list(url, session)
    print(f'Found {len(chapter_list)} chapters')

    print('Clawing...')

    total_page = 0
    total_time = 0
    imgs = {}
    for chapter_url in chapter_list:
        chapter_id = chapter_url[-12:-1]
        print(f'Clawing chapter {chapter_id}')
        time_usage = time.time()
        page_list = [
            'http://reserves.lib.tsinghua.edu.cn' + url for url in get_file_list(
                'http://reserves.lib.tsinghua.edu.cn' + chapter_url + 'files/mobile/', session
            )
        ]

        img_list = []
        concurrent_download(page_list, img_list, session, concurrent)

        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += len(img_list)
        imgs[chapter_id] = img_list
        print(f'Clawed {len(img_list)} pages, time usage:{time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total, time usage:{total_time: .3f}s')
    return imgs


def download(url: str, gen_pdf=True, save_img=True, quality=96, concurrent=6, resume=False) -> None:

    print('Preparing...')

    url = get_base_url(url)
    book_id = url[url[:-1].rfind('/') + 1:-1]
    img_dir = 'clawed_' + book_id

    need_cookie = ('/books/' in url)  # magic
    cookie = get_cookie() if need_cookie else {}

    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie)
    session.headers.update({
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    })

    if resume:
        imgs = {}
        for file in os.listdir(img_dir):
            chapter_id = file.split('_')[0]
            with open(f'{img_dir}/{file}', 'rb') as f:
                img = f.read()
            try:
                imgs[chapter_id].append(img)
            except KeyError:
                imgs[chapter_id] = [img]
    elif '/book4/' in url:
        imgs = claw_book4(url, concurrent, session)
    else:
        print('Unable to download concurrently due to limitations')
        imgs = claw(url, session)

    if quality < 96:
        for img_list in imgs.values():
            resize(img_list, quality)

    if save_img:
        print('Saving images...')
        os.makedirs(img_dir, exist_ok=True)
        for chapter_id, img_list in imgs.items():
            for i, img in enumerate(img_list):
                with open(img_dir + f'/{chapter_id}_{i:04d}.jpg', 'wb') as file:
                    file.write(img)
        print(f'Image folder path: {img_dir}')

    if gen_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        generate_pdf(pdf_path, imgs)
        print(f'PDF path: {pdf_path}')

    print('Done')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='See README.md for help; '
        'Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader'
    )
    parser.add_argument('--url', type=str, help='input target URL')
    parser.add_argument('--no-pdf', action='store_true', help='disable generating PDF')
    parser.add_argument('--no-img', action='store_true', help='disable saving images')
    parser.add_argument(
        '--quality',
        type=int,
        default=96,
        help='reduce file size, [1, 96] (85 by recommendation, 96 by default)'
    )
    parser.add_argument(
        '--con', type=int, default=6, help='the number of concurrent downloads (6 by default)'
    )
    parser.add_argument('--resume', action='store_true', help='skip downloading images (for testing)')
    args = parser.parse_args()
    url = args.url
    quality = args.quality

    if url is None:
        print('GitHub Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader')
        print('Thanks for using. Please see README.md for help.')
        print('Try running "downloader -h" in terminal for advanced settings.')
        print('*' * 20)
        url = input('INPUT URL: ')
        quality = input('Reduce file size? y/[n] ')
        if quality != '' and strtobool(quality):
            quality = input('Please input quality ratio in [1, 96] (85 by recommendation): ')
            if quality == '':
                quality = 85
            quality = int(quality)
        elif quality == '':
            quality = 96

    if not (1 <= quality <= 96):
        raise ValueError('--quality [1, 96] out of bounds')

    download(url, not args.no_pdf, not args.no_img, quality, args.con, args.resume)
