import requests
import urllib
from urllib.request import urlretrieve

__author__ = 'i207M'

# URL_example = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html'
# URL_image_example = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'


def url_available(url: str) -> bool:
    # print(url)
    return True


def claw(url: str) -> None:
    if not url.endswith('index.html'):
        raise Exception('URL Wrong!')
    url = url.rstrip('000/index.html')
    index_url = url + '{:03d}/index.html'
    id = 0
    while id <= 999 and url_available(index_url.format(id)):
        image_url = url.replace('book4/', 'book4') + f'{id:03d}/files/mobile/{{}}.jpg'
        # print(image_url)
        cnt = 1
        while cnt != 0:
            try:
                urlretrieve(image_url.format(cnt), f'./clawed/{id}_{cnt}.png')
            except urllib.error.HTTPError as e:
                assert e.code == 404
                print(id, cnt, image_url.format(cnt))
                cnt = -1
            cnt = cnt + 1
        id = id + 1
        break


if __name__ == '__main__':
    claw('http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/index.html')
