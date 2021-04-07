from downloader import claw


def test_claw_default():
    claw('http://reserves.lib.tsinghua.edu.cn/book5//00001471/00001471000/index.html')
