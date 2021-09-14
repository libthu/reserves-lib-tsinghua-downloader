import os
from argparse import ArgumentParser
from distutils.util import strtobool

import requests

from utils.claw import claw, claw_book4
from utils.cookie import get_cookie
from utils.image import resize
from utils.pdf import generate_pdf

__author__ = 'i207M'

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book6/00009127/00009127000/mobile/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'


def get_base_url(url: str) -> str:
    if not (url.startswith('http://reserves.lib.tsinghua.edu.cn/') and url.endswith('/index.html')):
        raise Exception('Invalid URL')
    url = url[:-11]  # '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    return url


def resume_file(img_dir: str):
    imgs = {}
    for file in os.listdir(img_dir):
        chapter_id = file.split('_')[0]
        with open(f'{img_dir}/{file}', 'rb') as f:
            img = f.read()
        try:
            imgs[chapter_id].append(img)
        except KeyError:
            imgs[chapter_id] = [img]
    return imgs


def download(url: str, gen_pdf=True, save_img=True, quality=96, concurrent=6, resume=False) -> None:

    print('Preparing...')

    url = get_base_url(url)
    sep = url[:-11].rfind('/')
    book_id = url[sep + 1:sep + 9]
    img_dir = 'clawed_' + book_id

    need_cookie = ('/books/' in url)  # magic
    cookie = get_cookie() if need_cookie else {}

    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie)
    session.headers.update({
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    })

    if resume:
        print('Resuming...')
        imgs = resume_file(img_dir)
    elif '/book4/' in url:
        url = url[:-11]
        imgs = claw_book4(url, concurrent, session)
    else:
        print('Unable to download concurrently due to limitations.')
        imgs = claw(url, session)

    if quality < 96:
        print('Optimizing images...')
        for img_list in imgs.values():
            resize(img_list, quality)

    if save_img:
        print('Saving images...')
        os.makedirs(img_dir, exist_ok=True)
        for chapter_id, img_list in imgs.items():
            for i, img in enumerate(img_list):
                with open(img_dir + f'/{chapter_id}_{i:04d}.jpg', 'wb') as file:
                    file.write(img)
        print(f'Image folder path: {img_dir}')

    if gen_pdf:
        print('Generating PDF...')
        pdf_path = book_id + '.pdf'
        generate_pdf(pdf_path, imgs)
        print(f'PDF path: {pdf_path}')

    print('Done.')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='See README.md for help. '
        'Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader'
    )
    parser.add_argument('--url', type=str, help='input target URL')
    parser.add_argument('--no-pdf', action='store_true', help='disable generating PDF')
    parser.add_argument('--no-img', action='store_true', help='disable saving images')
    parser.add_argument(
        '--quality',
        type=int,
        default=96,
        help='reduce file size, [1, 96] (85 by recommendation, 96 by default)'
    )
    parser.add_argument(
        '--con', type=int, default=6, help='the number of concurrent downloads (6 by default)'
    )
    parser.add_argument('--resume', action='store_true', help='skip downloading images (for testing)')
    args = parser.parse_args()
    url = args.url
    quality = args.quality

    if url is None:
        print('GitHub Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader')
        print('Thanks for using. Please see README.md for help.')
        print('Try running "downloader -h" in terminal for advanced settings.')
        print('*' * 20)
        print('Made by i207M with Love :) Email: connect@mail.i207m.top')
        print('*' * 20)
        url = input('INPUT URL: ')
        quality = input('Reduce file size? y/[n] ')
        if quality != '' and strtobool(quality):
            quality = input('Please input quality ratio in [1, 96] (85 by recommendation): ')
            quality = int(quality) if quality != '' else 85
        else:
            quality = 96

    if not (1 <= quality <= 96):
        raise ValueError('--quality [1, 96] out of bounds')

    download(url, not args.no_pdf, not args.no_img, quality, args.con, args.resume)
    input("Press Enter to Exit.")  # Prevent window from closing
