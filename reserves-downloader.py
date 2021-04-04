import os
import requests

__author__ = 'i207M'

# URL_example = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# URL_image_example = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# URL_cookie_example = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def url_available(url: str) -> bool:
    # print(url)
    res = requests.get(url)
    return res.status_code == 200


def mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def url_shape(url: str) -> str:
    if not (url.startswith('http://') and url.endswith('index.html')):
        raise Exception('Invalid URL')
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]  # '000'
    return url


def claw(url: str) -> None:

    # modify url
    url = url_shape(url)
    index_url = 'http://' + url + '{:03d}/index.html'
    image_url_base = 'http://' + url.replace('//', '/')
    path = './clawed_' + url[url.rfind('/') + 1:]
    mkdir(path)

    # read cookies
    need_cookie = ('//' in url)
    cookie = {}
    if need_cookie:
        with open('cookie.txt') as f:
            _data = [v.strip() for v in f.read().splitlines()]
            if len(_data) != 2:
                raise Exception('Cookie data error')
            cookie['ASPXAUTH'] = _data[0]
            cookie['ASP.NET_SessionId'] = _data[1]

    # claw
    id = 0
    page_num = 0
    print('Start clawing...')
    while id <= 999 and url_available(index_url.format(id)):
        image_url = image_url_base + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 0
        while True:
            res = requests.get(image_url.format(cnt), cookies=cookie)
            if res.status_code != 200:
                if res.status_code == 404:
                    print(f'Clawed: {id=}, {cnt=}')
                    break
                raise Exception('HTTP error')
            if len(res.content) < 10 * 1024:
                raise Exception('Unable to download, perhaps due to invalid cookie')
            with open(f'{path}/{page_num:05d}.jpg', 'wb+') as f:
                f.write(res.content)
            cnt += 1
            page_num += 1
        id += 1
    print(f'Total page number: {page_num}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
