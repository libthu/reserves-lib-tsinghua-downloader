## 写在前面

目前学校对教参平台的访问添加了速率限制，短时间内多次爬取会暂时ban IP，请过一段时间重试。

设置相邻请求的间隔时间可以使用 `-i seconds` 来设置，关于命令行参数的更多帮助请运行 `downloader --help`

# 清华教参服务平台 辅助工具

![GitHub release (latest by date)](https://img.shields.io/github/v/release/libthu/reserves-lib-tsinghua-downloader) ![Python version](https://img.shields.io/badge/python-3.9%2B-blue) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/libthu/reserves-lib-tsinghua-downloader/Release%20Test?label=test) ![GitHub issues](https://img.shields.io/github/issues/libthu/reserves-lib-tsinghua-downloader)

Download pages from http://reserves.lib.tsinghua.edu.cn/

自动下载书籍每一页的原图，生成PDF，免登录。

![command.png](https://s2.loli.net/2022/01/23/utwNI73z15T4OLS.png)

## Download

从[Releases](https://github.com/libthu/reserves-lib-tsinghua-downloader/releases/latest)，下载`Assets`中对应系统的可执行文件。或运行Python脚本`downloader.py`。

## Usage

![website.png](https://i.loli.net/2021/03/08/zVAYweuK7cHk5os.png)

运行`downloader`，输入网站“`阅读全文`”之下的链接地址（如图中标黄的位置）。程序会自动爬取当前章节以下的所有章节。

程序会将图片保存在`./clawed`下，并自动生成PDF。

**此程序无需登录即可使用**。

### MacOS

**NOTE**：可执行文件可能无法在macOS Monterey运行，正在修复。

MacOS用户可能无法直接运行下载的`downloader`，是因为它没有“执行权限”。

解决方法：在终端中进入`downloader`文件所在的文件夹，执行`chmod +x downloader`命令。有关此命令的更多帮助请参阅[Apple](https://support.apple.com/zh-cn/guide/terminal/apdd100908f-06b3-4e63-8a87-32e71241bab4/mac)。

MacOS上的第一次启动可能会有点慢。

## Q&A

**Q:** 图片压缩的`quality`应该怎样设置？

A: 范围[1, 96]：其中96为原图，[1, 95]从最差到最佳。

**Q:** 运行报错`Cookie Required`，怎么办？

A: 经测试，绝大部分教参无需`cookie`即可访问。少数教参需要`cookie`进行身份验证，请将网站`cookie`中，`.ASPXAUTH`和`ASP.NET_SessionId`的值依次写入同目录下`cookie.txt`中，每行一个。（我将会完善获取网站`cookie`的相关教程。若急需，请与我发邮件）

**Q:** 运行报错`'type' object is not subscriptable`，怎么办？

A: 请升级Python版本至**3.9+**，或直接运行分发的可执行文件。

**Q:** 下载的章节不全？

A: 这是因为此图书的章节编号不连续。请再次运行程序并输入下一位置的章节链接。通常不会出现此情况。

**Q:** 分享一点高级玩法？

A: 使用学校提供的正版福昕编辑器可以进行OCR。

## Advanced Settings

Run `downloader --help` in terminal.

```
usage: downloader.py [-h] [-u URL] [-q Q] [-c C] [-i I] [--no-pdf] [--no-img] [--end] [--resume]

See README.md for help. Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     input URL
  -q Q, --quality Q     the image quality, from 0 (worst) to 95 (best). 96 keeps images unchanged.
  -c C, --concurrent C  the number of concurrent downloads (6 by default)
  -i I, --interval I    time interval between batchs, in seconds
  --no-pdf              disable generating PDF
  --no-img              disable saving images
  --end                 exit automatically after finishing
  --resume              skip downloading images
```

希望尝鲜？从GitHub Actions中下载预览版的可执行文件！

## TODO

- Fix executable on macOS
- tqdm
- Fetch pure text from website
- PDF Bookmark

## Contribution

请查看[`contribution.md`](/contribution.md)。

欢迎Star/Issue/PR~

---

*仅供Python语言的学习参考，请勿用于非法用途！*

友情链接：

更多清华常用信息/服务汇总请看[这里](https://github.com/ZenithalHourlyRate/thuservices)。
