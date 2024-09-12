import time
import requests
from utils.concurrent import concurrent_download
from bs4 import BeautifulSoup


def get_chapter_list(scanid: str, session: requests.Session) -> list:
    url = "https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapters"
    ret = session.post(url, data={"SCANID": scanid}).json()
    if ret["code"] != 1:
        raise Exception("Please renew your token.")
    chapters = ret["data"]
    return chapters


def claw(
    bookid: str, session: requests.Session, concurrent: int, interval: float
) -> dict[int, list[bytes]]:
    ret = session.get(
        "https://ereserves.lib.tsinghua.edu.cn/userapi/MyBook/getBookDetail?bookId="
        + bookid
    ).json()
    if ret["code"] != 1:
        raise Exception("Please renew your token.")
    bookname = ret["data"]["jc_ebook_vo"]["EBOOKNAME"]
    readid = ret["data"]["jc_ebook_vo"]["urls"][0]["READURL"]
    print("Bookname:", bookname)

    ret = session.post(
        "https://ereserves.lib.tsinghua.edu.cn/userapi/ReadBook/GetResourcesUrl",
        json={"id": readid},
    ).json()
    if ret["code"] != 1:
        raise Exception("Please renew your token.")
    ret = session.get(ret["data"])
    scanid = BeautifulSoup(ret.text, "html.parser").find("input", {"id": "scanid"})[
        "value"
    ]

    BotuReadKernel = session.cookies.get("BotuReadKernel")
    session.headers.update({"BotuReadKernel": BotuReadKernel})

    print("Clawing chapters...")
    chapter_list = get_chapter_list(scanid, session)

    total_page = 0
    total_time = 0
    imgs = {}
    for i, chapter in enumerate(chapter_list):
        time_usage = time.time()

        url = "https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapter"
        ret = session.post(url, data={"EMID": chapter["EMID"], "BOOKID": bookid}).json()
        if ret["code"] != 1:
            raise Exception("Please renew your token.")

        page_list = ret["data"]["JGPS"]
        page_cnt = len(page_list)
        print(f"Clawing chapter {i}, {page_cnt} pages in total.")

        img_list = concurrent_download(page_list, session, concurrent, interval)
        imgs[i] = img_list

        time_usage = time.time() - time_usage
        total_time += time_usage
        total_page += page_cnt

    print(f"Clawed {total_page} pages in total, time usage:{total_time: .3f}s")
    return imgs
