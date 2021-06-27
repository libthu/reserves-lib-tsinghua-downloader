import os
from io import BytesIO

from utils.html import get_chapter_list, get_page_list
from utils.parallel import parallel_download
from utils.cookie import get_cookie

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def trim(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('index.html')):
        raise Exception('Invalid URL')
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]  # '000'
    return url


def get_base_url(url: str) -> str:
    pass


def claw(url: str, save_pdf=True, keep_img=True, retry=10, parallel=8) -> None:

    print('Preparing...')

    url = get_base_url(url)
    book_id = url[url.rfind('/') + 1:]

    img_folder_path = 'clawed_' + book_id
    os.makedirs(img_folder_path, exist_ok=True)

    need_cookie = ('//' not in url)  # magic
    cookie = get_cookie() if need_cookie else {}

    print('Fetching chapters')

    chapter_list = get_chapter_list(url)
    # print

    print('Clawing...')

    total_page = 0
    for chapter_id in chapter_list:
        pass

    if not keep_img:
        pass

    print('Finished')
    print(f'Clawed {total_page} pages')
    print(f'PDF path: {pdf_path}')
    if keep_img:
        print(f'Image folder path: {img_folder_path}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
