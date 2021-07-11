import os
import time
from argparse import ArgumentParser

import requests

from utils.http import get_file_list
from utils.concurrent import concurrent_download
from utils.cookie import get_cookie
from utils.pdf import generate_pdf

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
        print(f'Clawing chapter id: {chapter_id}')
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
        print(f'Clawed {len(img_list)} pages, time usage: {time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total, time usage: {total_time: .3f}s')
    return imgs


def claw():
    pass


def download(url: str, gen_pdf=True, save_img=True, concurrent=6, resume=False) -> None:

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

    if '/book4/' in url:
        imgs = claw_book4(url, concurrent, session)
    else:
        imgs = claw(url)

    # TODO: image resize

    if gen_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        generate_pdf(pdf_path, imgs)
        print(f'PDF path: {pdf_path}')

    if save_img:
        print('Saving images...')
        os.makedirs(img_dir, exist_ok=True)
        for chapter_id, img_list in imgs.items():
            for i, img in enumerate(img_list):
                with open(img_dir + f'/{chapter_id}_{i:04d}.jpg', 'wb') as f:
                    f.write(img)
        print(f'Image folder path: {img_dir}')

    print('Done')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='See README.md for help; '
        'Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader'
    )
    parser.add_argument('--url', type=str, help='input target URL')
    parser.add_argument('--no-pdf', action='store_true', help='disable generating PDF')
    parser.add_argument('--no-img', action='store_true', help='disable saving images')
    parser.add_argument('--concurrent', type=str, default=6, help='max number of threads')
    parser.add_argument('--resume', action='store_true', help='skip downloading images (for testing)')
    args = parser.parse_args()
    url = args.url

    if url is None:
        print('GitHub repo: https://github.com/i207M/reserves-lib-tsinghua-downloader')
        print('Thanks for using. See README.md for help.')
        print('Try running "downloader -h" in terminal for advanced settings.')
        url = input('INPUT URL:')
    download(url, not args.no_pdf, not args.no_img, int(args.concurrent), args.resume)
