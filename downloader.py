import os
import shutil
from argparse import ArgumentParser

from utils.http import SessionTHU, get_file_list
from utils.concurrent import concurrent_download
from utils.cookie import get_cookie

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def get_base_url(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('/index.html')):
        raise Exception('Invalid URL')
    url = url[7:]  # 'http://'
    url = url.replace('//', '/')
    url = url[:url.find('book') + 15]
    return 'http://' + url


def claw(url: str, gen_pdf=True, save_img=False, retry=10, concurrent=8) -> None:

    print('Preparing...')

    url = get_base_url(url)
    book_id = url[url[:-1].rfind('/') + 1:-1]

    need_cookie = ('//' not in url)  # magic
    cookie = get_cookie() if need_cookie else {}
    session = SessionTHU(cookie, retry)

    print('Fetching chapters...')

    chapter_list = get_file_list(url, session)
    print(f'Found {len(chapter_list)} chapters')

    print('Clawing...')

    total_page = 0
    imgs = {}
    for chapter_url in chapter_list:
        chapter_id = chapter_url[-12:-1]
        print(f'Clawing chapter id: {chapter_id}')
        page_list = [
            'http://reserves.lib.tsinghua.edu.cn' + url for url in get_file_list(
                'http://reserves.lib.tsinghua.edu.cn' + chapter_url + 'files/mobile/', session
            )
        ]
        img_list = []
        concurrent_download(page_list, img_list, session, concurrent)
        total_page += len(img_list)
        imgs[chapter_id] = img_list
        print(f'Clawed {len(img_list)} pages')

    print(f'Clawed {total_page} pages in total')

    if gen_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        print(f'PDF path: {pdf_path}')

    if save_img:
        img_dir = 'clawed_' + book_id
        os.makedirs(img_dir, exist_ok=True)
        print(f'Image folder path: {img_dir}')

    print('Done')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='See README.md for help; '
        'Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader'
    )
    parser.add_argument('--url', type=str, help='input target URL')
    parser.add_argument('--no-pdf', action='store_true', help='disable generating PDF')
    parser.add_argument('--saveimg', action='store_true', help='keep downloaded images')
    parser.add_argument('--retry', type=int, default=10, help='max number of retries')
    parser.add_argument('--concurrent', type=str, default=8, help='max number of threads')
    args = parser.parse_args()
    url = args.url

    if url is None:
        url = input('INPUT URL:')
    claw(url, not args.no_pdf, args.saveimg, args.retry, args.concurrent)
