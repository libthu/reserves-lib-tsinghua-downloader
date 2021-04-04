import os
import urllib
from urllib import request

__author__ = 'i207M'

# URL_example = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# URL_image_example = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'


def url_available(url: str) -> bool:
    # print(url)
    try:
        request.urlopen(url)
    except urllib.error.HTTPError:
        return False
    return True


def mkdir(path: str) -> None:
    # print(path)
    if not os.path.exists(path):
        os.makedirs(path)


def url_shape(url: str) -> str:
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]  # '000'
    return url


def claw(url: str) -> None:
    if not url.endswith('index.html'):
        raise Exception('URL Invalid!')
    url = url_shape(url)
    index_url = 'http://' + url + '{:03d}/index.html'
    image_url_base = 'http://' + url.replace('//', '/')
    path = './clawed_' + url[url.rfind('/') + 1:]
    mkdir(path)

    id = 0
    page_num = 0
    print('Start clawing...')
    while id <= 999 and url_available(index_url.format(id)):
        image_url = image_url_base + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 1
        while cnt != 0:
            try:
                request.urlretrieve(image_url.format(cnt), f'{path}/{page_num:05d}.jpg')
                page_num += 1
                print(image_url.format(cnt))
                exit()
            except urllib.error.HTTPError as e:
                assert e.code == 404
                print(f'Clawed: {id=}, {cnt=}')
                cnt = -1
            cnt += 1
        id += 1
    print(f'Total page number: {page_num}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
