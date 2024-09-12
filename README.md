写在前面：Looking for maintainers. Please contact libthu (a) yandex.com if you are interested!

# 清华教参服务平台 辅助工具

![GitHub release (latest by date)](https://img.shields.io/github/v/release/libthu/reserves-lib-tsinghua-downloader) ![Python version](https://img.shields.io/badge/python-3.9%2B-blue) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/libthu/reserves-lib-tsinghua-downloader/release-test.yml?label=test) ![GitHub issues](https://img.shields.io/github/issues/libthu/reserves-lib-tsinghua-downloader)

Download pages from https://ereserves.lib.tsinghua.edu.cn/

下载书籍每一页的原图，生成 PDF，需要登录获取 Token 才能正常使用。

## Download

从 [Releases](https://github.com/libthu/reserves-lib-tsinghua-downloader/releases/latest) 的 `Assets` 中，下载对应系统的可执行文件。或运行 Python 脚本 `downloader.py`。

## Token

由于新版教参平台使用 SSO 单点登录，需要自行在网页上登录并获得 Token 才能访问资源。

![login.png](https://s2.loli.net/2024/09/13/xFezwadpABgl2tZ.png)

通过统一身份认证登录后，在主页用 F12 或 Ctrl-Shift-I 打开开发者工具。进入“控制台”或“Console”选项卡，运行 `localStorage.License` 获取 Token。 将 Token 保存在同一目录下的 `Token.txt` 文件中。**Token 的有效期为 1 个小时，如果过期需要重新登录。**

## Usage

![bookinfo.png](https://s2.loli.net/2024/09/12/2dXCsKD4SMnu9ix.png)

运行 `downloader`，输入网站教参详情的地址（如图中标黄的位置）。程序会自动爬取对应书籍。

程序会将图片保存在 `clawed` 文件夹下，并自动生成 PDF。

![image.png](https://s2.loli.net/2023/02/28/JNfP4Sk7HuLhapz.png)

### macOS

macOS 用户可能无法直接运行下载的 `downloader`，可能有两种原因：

- 因为它没有“执行权限”。

  解决方法：在终端中进入 `downloader` 文件所在的文件夹，执行 `chmod +x downloader` 命令。有关此命令的更多帮助请参阅 [Apple](https://support.apple.com/zh-cn/guide/terminal/apdd100908f-06b3-4e63-8a87-32e71241bab4/mac)。

- 因为它不是从 App Store 下载的。

  解决方法：点击“**安全性与隐私**” -> “**通用**” -> “**仍要打开**”按钮来允许被阻止的 App。此按钮在您尝试打开该 App 后一小时内可用。更多帮助请参阅 [Apple](https://support.apple.com/zh-cn/guide/mac-help/mh40616/mac)。

## Q&A

**Q:** 图片压缩的 `quality` 选项应该怎样设置？

A: 范围 [1, 96]：其中 96 为不压缩（默认），[1, 95]从最差到最佳。更多信息请参见[PIL 文档](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?#jpeg)。

**Q:** 运行时报错 `'type' object is not subscriptable`，怎么办？

A: 请升级 Python 版本至 **3.9+**，或直接运行分发的可执行文件。

<!-- **Q:** 运行时报错 `Cookie Required`，怎么办？

A: 经测试，绝大部分教参无需 cookie 即可访问。少数教参需要 cookie 进行身份验证，请将网站 cookie 中 `.ASPXAUTH` 和 `ASP.NET_SessionId` 的值依次写入同目录下 `cookie.txt`，每行一个。获取 cookie 的方法请见 [#5](https://github.com/libthu/reserves-lib-tsinghua-downloader/issues/5) -->

<!-- **Q:** 下载的章节不全？

A: 这是因为此图书的章节编号不连续。请再次运行程序并输入下一位置的章节链接。通常不会出现此情况。 -->

**Q:** 下载突然失败了？

A: 目前学校对教参平台的访问添加了**速率限制**，短时间内多次爬取会暂时 ban IP，请过一段时间重试。设置相邻请求的间隔时间可以使用 `-i seconds` 来设置。

**Q:** 分享一些高级玩法？

- 使用学校提供的正版福昕编辑器可以对 PDF 进行 OCR。
- Z-Library 无法正常访问，使用谷歌搜索 `zlib searcher` 有惊喜。
- 从 GitHub Actions 中可以下载预览版的可执行文件。

## Advanced Settings

Run `downloader --help` in terminal.

```
usage: downloader.py [-h] [-v] [-u URL] [-c C] [-i I] [-q Q] [-r] [-e] [--no-pdf] [--no-img]

See README.md for help. Repo: https://github.com/libthu/reserves-lib-tsinghua-downloader

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -u URL, --url URL     input URL
  -c C, --concurrent C  the number of concurrent downloads (4 by default)
  -i I, --interval I    the time interval between batchs, in seconds (0.5 by default)
  -q Q, --quality Q     the image quality, from 0 (worst) to 95 (best). 96 keeps images unchanged.
  -r, --resume          skip downloading images
  -e, --exit            exit automatically when done
  --no-pdf              do not generate PDF
  --no-img              do not save images
```

## TODO

- Translation
- Fetch pure text from the website
- PDF bookmark

## Contribution

请查看[`contribution.md`](/contribution.md)。

欢迎 Star/Issue/PR~

---

Use at your own risk.

友情链接：更多清华常用信息/服务汇总请看[这里](https://github.com/ZenithalHourlyRate/thuservices)。
