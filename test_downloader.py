from downloader import download


def test_claw_book():
    download(
        "https://ereserves.lib.tsinghua.edu.cn/bookDetail/092404F541455700E065000000000001"
    )


if __name__ == "__main__":
    test_claw_book()
