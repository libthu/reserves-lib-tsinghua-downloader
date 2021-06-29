import os
import time
from argparse import ArgumentParser

import requests

from utils.http import get_file_list
from utils.concurrent import concurrent_download
from utils.cookie import get_cookie
from utils.pdf import generate_pdf

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/mobile/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def get_base_url(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('/index.html')):
        raise Exception('Invalid URL')
    url = url[7:]  # 'http://'
    url = url.replace('//', '/')
    url = url[:url.find('book') + 15]
    return 'http://' + url


def claw(url: str, gen_pdf=True, save_img=False, concurrent=8, resume=False) -> None:

    print('Preparing...')

    url = get_base_url(url)
    book_id = url[url[:-1].rfind('/') + 1:-1]
    img_dir = 'clawed_' + book_id

    need_cookie = ('//' not in url)  # magic
    cookie = get_cookie() if need_cookie else {}

    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie)
    session.headers.update({
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    })

    print('Fetching chapters...')

    chapter_list = get_file_list(url, session)
    print(f'Found {len(chapter_list)} chapters')

    if resume:
        print('Resuming...')
        resumed_list = [f for f in os.listdir(img_dir) if os.path.isfile(f'{img_dir}/{f}')]
        resumed_list.sort()
        resumed = {}
        for chapter_url in chapter_list:
            chapter_id = chapter_url[-12:-1]
            resumed[chapter_id] = []
        for f in resumed_list:
            chapter_id, file_name = f.split('_')
            resumed[chapter_id].append(file_name)

    print('Clawing...')

    total_page = 0
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
        if resume:
            resumed_set = set(resumed[chapter_id])
            download_list = [url for url in page_list if url[url.rfind('/') + 1:] in resumed_set]
        else:
            download_list = page_list

        img_list = []
        concurrent_download(download_list, img_list, session, concurrent)
        assert len(download_list) == len(img_list)

        total_page += len(img_list)
        time_usage = time.time() - time_usage
        if resume:
            imgs[chapter_id] = [
                open(f'{img_dir}/{chapter_id}_{f}', 'rb').read() for f in resumed[chapter_id]
            ] + img_list
            print(f'Resumed {len(page_list)-len(download_list)} pages')
        else:
            imgs[chapter_id] = img_list
        print(f'Clawed {len(img_list)} pages, time usage: {time_usage: .3f}s')
        print('*' * 20)

    print(f'Clawed {total_page} pages in total')

    # TODO: image resize

    if gen_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        generate_pdf(pdf_path, imgs)
        print(f'PDF path: {pdf_path}')

    if save_img:
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
    parser.add_argument('--saveimg', action='store_true', help='save downloaded images')
    parser.add_argument('--concurrent', type=str, default=8, help='max number of threads')
    parser.add_argument(
        '--resume', action='store_true', help='skip saved images (only works for some situations)'
    )
    args = parser.parse_args()
    url = args.url

    if url is None:
        url = input('INPUT URL:')
    claw(url, not args.no_pdf, args.saveimg, args.concurrent, args.resume)
