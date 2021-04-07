import os
import requests
from PIL import Image

__author__ = 'i207M'

# URL_example = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# URL_image_example = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# URL_need_cookie_example = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


cookie = {}


def url_available(url: str) -> bool:
    # print(url)
    ret = requests.get(url, cookies=cookie)
    return ret.status_code == 200


def url_shape(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('index.html')):
        raise Exception('Invalid URL')
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]  # '000'
    return url


def cookie_init() -> None:
    COOKIE_PATH = 'cookie.txt'

    if not os.path.exists(COOKIE_PATH):
        raise Exception(f'No cookie data in "{COOKIE_PATH}". See README.md for help.')
    with open(COOKIE_PATH) as f:
        _data = [v.strip() for v in f.read().splitlines()]
        if len(_data) != 2:
            raise Exception('Cookie data error')
        global cookie
        cookie['.ASPXAUTH'] = _data[0]
        cookie['ASP.NET_SessionId'] = _data[1]


def claw(url: str) -> None:

    # modify url
    url = url_shape(url)
    index_url = 'http://' + url + '{:03d}/index.html'
    image_url_base = 'http://' + url.replace('//', '/')
    path = './clawed_' + url[url.rfind('/') + 1:]
    mkdir(path)

    pdf_name = "temp.pdf"
    pdf_path = os.path.join(path, pdf_name)

    # process cookies
    need_cookie = ('//' not in url)
    if need_cookie:
        cookie_init()

    # claw
    id = 0
    page_num = 0
    print('Start clawing...')
    while id <= 999 and url_available(index_url.format(id)):
        image_url = image_url_base + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 0
        while True:
            ret = requests.get(image_url.format(cnt + 1), cookies=cookie)
            if ret.status_code != 200:
                if ret.status_code == 404:
                    print(f'Clawed: {id=}, {cnt=}')
                    break
                raise Exception(f'HTTP error {ret.status_code}')
            # A login html (~7kB) is downloaded when cookies are invalid.
            if need_cookie and len(ret.content) < 10 * 1024:
                raise Exception('Unable to download. Perhaps due to invalid cookies.')
            with open(f'{path}/{page_num:05d}.jpg', 'wb+') as f:
                f.write(ret.content)

            with Image.open(os.path.join(path, f"{page_num:05d}.jpg")) as jpg:
                jpg.convert("RGB").save(pdf_path, append=bool(page_num))

            cnt += 1
            page_num += 1
        id += 1
    print(f'Total page number: {page_num}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
