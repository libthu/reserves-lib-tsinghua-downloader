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


def claw(url: str) -> None:
    if not url.endswith('index.html'):
        raise Exception('URL Wrong!')
    os.makedirs('./clawed')
    url = url.rstrip('000/index.html')
    index_url = url + '{:03d}/index.html'
    id = 0
    while id <= 999 and url_available(index_url.format(id)):
        image_url = url.replace('book4/', 'book4') + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 1
        while cnt != 0:
            try:
                request.urlretrieve(image_url.format(cnt), f'./clawed/{id:03d}_{cnt:05d}.png')
            except urllib.error.HTTPError as e:
                assert e.code == 404
                print(f'Clawed: {id=}, {cnt=}')
                cnt = -1
            cnt = cnt + 1
        id = id + 1


if __name__ == '__main__':
    url = input('INPUT URL:')
    claw(url)
    # claw('http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html')
