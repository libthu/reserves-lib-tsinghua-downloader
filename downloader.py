import os
import shutil
from argparse import ArgumentParser

from utils.html import get_chapter_list, get_page_list
from utils.parallel import parallel_download
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


def claw(url: str, save_pdf=True, keep_img=True, retry=10, parallel=8) -> None:

    print('Preparing...')

    url = get_base_url(url)
    book_id = url[url.rfind('/') + 1:]

    img_folder_path = 'clawed_' + book_id
    os.makedirs(img_folder_path, exist_ok=True)

    need_cookie = ('//' not in url)  # magic
    cookie = get_cookie() if need_cookie else {}

    print('Fetching chapters...')

    chapter_list = get_chapter_list(url)
    # print

    print('Clawing...')

    total_page = 0
    for chapter_id in chapter_list:
        pass

    print(f'Clawed {total_page} pages in total')

    if save_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        print(f'PDF path: {pdf_path}')

    if keep_img:
        print(f'Image folder path: {img_folder_path}')
    else:
        shutil.rmtree(img_folder_path)

    print('Done')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='See README.md for help; '
        'Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader'
    )
    parser.add_argument('--url', type=str, help='input target URL')
    args = parser.parse_args()
    url = args.url

    if url is None:
        url = input('INPUT URL:')
    claw(url)
