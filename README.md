# 清华大学教参服务平台 Downloader
Download pages from http://reserves.lib.tsinghua.edu.cn/

自动下载书籍每一页的原图。

## Usage

![image-20210308204615230](https://i.loli.net/2021/03/08/zVAYweuK7cHk5os.png)

直接运行（或调用`reserves-downloader.py`中的函数`claw`），传入的参数为`阅读全文`下第一个链接（图中标黄的链接）。

程序会自动从第一章开始爬取每一章的每一页，保存在`./clawed`下。

## TODO
- 自动将图片整合为PDF（临时方案：使用学校提供的`Foxit Editor`创建PDF）
- 自动设置图片的压缩率

欢迎Star/Issue/PR.

*请勿用于非法用途！*