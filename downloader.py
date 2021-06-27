import os
from io import BytesIO
try:
    import requests
    from PIL import Image
except ModuleNotFoundError:
    print('*' * 20)
    print('Error: Module Not Found')
    print('Please RUN: pip install -r requirements.txt')
    print('*' * 20)
    raise

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def is_available(url: str, cookie={}, retry=1) -> bool:
    status_code = -1
    for _ in range(retry):
        ret = requests.get(url, cookies=cookie)
        status_code = ret.status_code
        if status_code in [200, 404]:
            return status_code == 200
    raise Exception(f'HTTP error {status_code}')


def get_image(url: str, cookie={}, retry=1) -> requests.Response:
    status_code = -1
    for _ in range(retry):
        ret = requests.get(url, cookies=cookie)
        status_code = ret.status_code
        if status_code in [200, 404]:
            return ret
    raise Exception(f'HTTP error {status_code}')


def cookie_init() -> dict:
    COOKIE_PATH = 'cookie.txt'
    cookie = {}

    if not os.path.exists(COOKIE_PATH):
        raise Exception(f'File not found: "{COOKIE_PATH}"\nSee README.md for help.')
    with open(COOKIE_PATH) as f:
        _data = [v.strip() for v in f.read().splitlines()]
        if len(_data) != 2:
            raise Exception('Cookie data error: too many or too few lines')
        cookie['.ASPXAUTH'] = _data[0]
        cookie['ASP.NET_SessionId'] = _data[1]
    return cookie


def trim(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('index.html')):
        raise Exception('Invalid URL')
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]  # '000'
    return url


def claw(
    url: str,
    retry=10,
    resume=None,
    make_pdf=True,
    save_img=False,
) -> None:

    # modify url
    url = trim(url)
    index_url = 'http://' + url + '{:03d}/index.html'
    image_url_base = 'http://' + url.replace('//', '/')

    # prepare variables
    book_id = url[url.rfind('/') + 1:]
    pdf_name = book_id + '.pdf'
    path = './clawed_' + book_id
    if save_img:
        os.makedirs(path, exist_ok=True)

    chapter_id = 0
    page_num = 0
    if resume is not None:
        chapter_id = resume['chapter_id']

    # process cookie
    cookie = {}
    need_cookie = ('//' not in url)  # magic
    if need_cookie:
        cookie = cookie_init()

    print('Start clawing...')
    while chapter_id <= 999 and is_available(index_url.format(chapter_id), retry):
        image_url = image_url_base + f'{chapter_id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)

        cnt = 0
        if resume is not None and chapter_id == resume['chapter_id']:
            cnt = resume['cnt']
        while True:
            try:
                ret = get_image(image_url.format(cnt + 1), cookie, retry)
            except Exception:
                # HTTP error occurred, print variables for resuming
                print('*' * 10)
                print('Network error occurred')
                print(f'Clawed page number: {page_num}\n{chapter_id=}\n{cnt=}')
                print('*' * 10)
                raise

            # finished clawing a chapter
            if ret.status_code == 404:
                print(f'Clawed: {chapter_id=}, {cnt=}')
                break

            # a login html (~7kB) is downloaded when cookie is invalid.
            if need_cookie and len(ret.content) < 10 * 1024:
                raise Exception('Invalid cookie')

            if save_img:
                with open(f'{path}/{page_num:05d}.jpg', 'wb+') as f:
                    f.write(ret.content)

            if make_pdf:
                img = Image.open(BytesIO(ret.content))
                img.convert('RGB').save(pdf_name, append=bool(page_num))

            cnt += 1
            page_num += 1
        chapter_id += 1
    print(f'Total page number: {page_num}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
