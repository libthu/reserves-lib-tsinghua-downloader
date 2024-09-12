import os
from argparse import ArgumentParser
from distutils.util import strtobool

import requests

from utils.claw import claw
from utils.token import get_token
from utils.image import resize
from utils.pdf import generate_pdf

__version__ = "3.2.1"

# example_URL = 'https://ereserves.lib.tsinghua.edu.cn/bookDetail/092404F541465700E065000000000001'


def resume_file(img_dir: str) -> dict[str, list[bytes]]:
    imgs = {}
    for file in os.listdir(img_dir):
        chapter_id = file.split("_")[0]
        img = open(f"{img_dir}/{file}", "rb").read()
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
    interval: float = 0.5,
    resume: bool = False,
) -> None:
    print("Preparing...")
    sep = url.rfind("/")
    book_id = url[sep + 1 :]
    img_dir = "clawed_" + book_id
    token = get_token()

    session = requests.session()
    session.headers.update({"jcclient": token})
    session.headers.update(
        {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
        }
    )

    if resume:
        print("Resuming...")
        imgs = resume_file(img_dir)
    else:
        try:
            imgs = claw(book_id, session, concurrent, interval)
        except Exception as e:
            print(e)
            print("*" * 30)
            print("An exception occurred.")
            print("This may be due to network issues. Please try again later.")
            print(
                "Note: The API has a rate limit. You may use `--interval` to set the time interval between batchs."
            )

    if quality < 96:
        print("Optimizing images...")
        for img_list in imgs.values():
            resize(img_list, quality)

    if save_img:
        print("Saving images...")
        os.makedirs(img_dir, exist_ok=True)
        for chapter_id, img_list in imgs.items():
            for i, img in enumerate(img_list):
                with open(img_dir + f"/{chapter_id}_{i:04d}.jpg", "wb") as file:
                    file.write(img)
        print(f"Image directory: {img_dir}")

    if gen_pdf:
        print("Generating PDF...")
        pdf_path = book_id + ".pdf"
        generate_pdf(pdf_path, imgs)
        print(f"PDF path: {pdf_path}")

    print("Done.")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="See README.md for help. "
        "Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader"
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument("-u", "--url", type=str, help="input URL")
    parser.add_argument(
        "-c",
        "--concurrent",
        type=int,
        default=4,
        metavar="C",
        help="the number of concurrent downloads (4 by default)",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=0.5,
        metavar="I",
        help="the time interval between batchs, in seconds (0.5 by default)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=96,
        metavar="Q",
        help="the image quality, from 0 (worst) to 95 (best). 96 keeps images unchanged.",
    )
    parser.add_argument(
        "-r", "--resume", action="store_true", help="skip downloading images"
    )
    parser.add_argument(
        "-e", "--exit", action="store_true", help="exit automatically when done"
    )
    parser.add_argument("--no-pdf", action="store_true", help="do not generate PDF")
    parser.add_argument("--no-img", action="store_true", help="do not save images")
    args = parser.parse_args()
    url = args.url
    quality = args.quality

    if url is None:
        print("Thanks for using. Please see README.md for help.")
        print('Try running "downloader --help" in terminal for advanced settings.')
        print(
            "Note: The API has a rate limit. You may use `--interval` to set the time interval between batchs."
        )
        print("*" * 30)
        print("Made with Love. Stars are welcomed :)")
        print("GitHub Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader")
        print("Email: libthu@yandex.com")
        print("*" * 30)
        url = input("INPUT URL: ")
        if url == "":
            print("No URL input. Exiting...")
            exit(0)
        quality = input("Compress images? y/[n] ")
        if quality != "" and strtobool(quality):
            quality = input(
                "Please input the image quality, from 0 (worst) to 95 (best): (75 by recommendation) "
            )
            quality = int(quality) if quality != "" else 75
        else:
            quality = 96
    assert 1 <= quality <= 96

    download(
        url,
        not args.no_pdf,
        not args.no_img,
        quality,
        args.concurrent,
        args.interval,
        args.resume,
    )

    if not args.exit:
        # prevent the window from closing
        input(
            "Press Enter to exit. You may use `--exit` to exit the process automatically."
        )
