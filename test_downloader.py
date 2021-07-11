from downloader import download


def test_claw_book4():
    download('http://reserves.lib.tsinghua.edu.cn/book4//00013082/00013082000/mobile/index.html')


def test_claw_book5():
    download('http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/index.html')


def test_claw_book6():
    download('http://reserves.lib.tsinghua.edu.cn/book6//00009438/00009438000/mobile/index.html')


if __name__ == '__main__':
    test_claw_book4()
    test_claw_book5()
    test_claw_book6()
