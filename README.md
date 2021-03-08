# 清华大学教参服务平台 Downloader
Download pages from http://reserves.lib.tsinghua.edu.cn/

自动下载书籍每一页的原图。

## Usage

![image-20210308204615230](https://i.loli.net/2021/03/08/zVAYweuK7cHk5os.png)

直接运行（或调用`reserves-downloader.py`中的函数`claw`），传入的参数为`阅读全文`下第一个链接（图中标黄的链接）。

目前仅支持`book4`类型（判断方法：URL中`book`后的数字）

## TODO
- 自动将图片整合为PDF（临时方案：使用学校提供的`Foxit Editor`创建PDF）
- 支持`book6` [eg.](http://reserves.lib.tsinghua.edu.cn/book6/00009127/00009127000/files/mobile/1.jpg)

欢迎Star/Issue/PR.

*请勿用于非法用途！*