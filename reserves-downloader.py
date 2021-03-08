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


def mkdir(path):
    # print(path)
    if not os.path.exists(path):
        os.makedirs(path)


def claw(url: str) -> None:
    if not url.endswith('index.html'):
        raise Exception('URL Wrong!')
    url = url[7:-11]  # 'http://', '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    url = url[:-3]
    path = './clawed_' + url.split('/')[-1]
    mkdir(path)
    index_url = url + '{:03d}/index.html'
    id = 0
    page_num = 0
    while id <= 999 and url_available('http://' + index_url.format(id)):
        image_url = 'http://' + url.replace('//', '/') + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 1
        while cnt != 0:
            try:
                request.urlretrieve(image_url.format(cnt), f'{path}/{page_num:05d}.jpg')
            except urllib.error.HTTPError as e:
                assert e.code == 404
                print(f'Clawed: {id=}, {cnt=}')
                cnt = -1
            cnt = cnt + 1
            page_num = page_num + 1
        id = id + 1
    print(f'Total page number: {page_num}')


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
