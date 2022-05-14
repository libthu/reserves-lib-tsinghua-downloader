import os
from argparse import ArgumentParser
from distutils.util import strtobool

import requests

from utils.claw import claw
from utils.cookie import get_cookie
from utils.image import resize
from utils.pdf import generate_pdf

# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/mobile/index.html'
# example_URL = 'http://reserves.lib.tsinghua.edu.cn/book6/00009127/00009127000/mobile/index.html'
# example_URL_need_cookie = 'http://reserves.lib.tsinghua.edu.cn/books/00000398/00000398000/index.html'
# example_image_URL = 'http://reserves.lib.tsinghua.edu.cn/book4/00013082/00013082000/files/mobile/1.jpg'


# This may be re-written using regular expression.
# example output: http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000
def get_base_url(url: str) -> str:
    if url.startswith('https://'):
        url = 'http' + url[5:]
    # using HTTP because the website's certificate somtimes expires
    assert url.startswith('http://reserves.lib.tsinghua.edu.cn/'), 'Invalid URL'
    assert url.endswith('/index.html'), 'Invalid URL'
    url = url[:-11]  # '/index.html'
    if url.endswith('mobile'):
        url = url[:-7]
    return url


def resume_file(img_dir: str) -> dict[str, list[bytes]]:
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


def download(
    url: str,
    gen_pdf: bool = True,
    save_img: bool = True,
    quality: int = 96,
    concurrent: int = 4,
    resume: bool = False,
    interval: float = 1,
) -> None:
    print('Preparing...')
    url = get_base_url(url)
    sep = url[:-11].rfind('/')
    book_id = url[sep + 1:sep + 9]
    img_dir = 'clawed_' + book_id

    need_cookie = ('/books/' in url)  # Magic.
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
    else:
        try:
            imgs = claw(url, session, concurrent, interval)
        except Exception as e:
            print(e)
            print('*' * 20)
            print('An exception occurred.')
            print('This may be due to network issues. Please try again later.')
            print('Note: The API has a rate limit. You may use `--interval` to set time interval.')

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
    parser = ArgumentParser(description='See README.md for help. ' 'Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader')
    parser.add_argument('-u', '--url', type=str, help='input URL')
    parser.add_argument(
        '-q', '--quality', type=int, default=96, metavar='Q', help='the image quality, from 0 (worst) to 95 (best). 96 keeps images unchanged.'
    )
    parser.add_argument('-c', '--concurrent', type=int, default=4, metavar='C', help='the number of concurrent downloads (4 by default)')
    parser.add_argument('-i', '--interval', type=float, default=1, metavar='I', help='time interval between batchs, in seconds')
    parser.add_argument('--no-pdf', action='store_true', help='disable generating PDF')
    parser.add_argument('--no-img', action='store_true', help='disable saving images')
    parser.add_argument('--exit', action='store_true', help='exit automatically after finishing')
    parser.add_argument('--resume', action='store_true', help='skip downloading images')
    args = parser.parse_args()
    url = args.url
    quality = args.quality

    if url is None:
        print('GitHub Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader')
        print('Thanks for using. Please see README.md for help.')
        print('Try running "downloader -h" in terminal for advanced settings.')
        print('Note: The API has a rate limit. You may use `--interval` to set time interval.')
        print('*' * 20)
        print('Made with Love :) Email: libthu@yandex.com')
        print('*' * 20)
        url = input('INPUT URL: ')
        quality = input('Reduce file size? y/[n] ')
        if quality != '' and strtobool(quality):
            quality = input('Please input the image quality, from 0 (worst) to 95 (best), 75 by recommendation: ')
            quality = int(quality) if quality != '' else 75
        else:
            quality = 96
    assert (1 <= quality <= 96)

    download(url, not args.no_pdf, not args.no_img, quality, args.concurrent, args.resume, args.interval)

    if not args.exit:
        # Prevent window from closing.
        input("Press Enter to Exit. You may use `--exit` to exit the process automatically.")
