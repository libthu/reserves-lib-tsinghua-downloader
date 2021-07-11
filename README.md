# 清华大学教参服务平台 Downloader

![GitHub release (latest by date)](https://img.shields.io/github/v/release/i207M/reserves-lib-tsinghua-downloader) ![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/i207M/reserves-lib-tsinghua-downloader/Release%20Test/main) ![GitHub issues](https://img.shields.io/github/issues/i207M/reserves-lib-tsinghua-downloader)

Download pages from http://reserves.lib.tsinghua.edu.cn/

自动下载书籍每一页的原图，免登录。

## Download

点击右侧[Releases](https://github.com/i207M/reserves-lib-tsinghua-downloader/releases/latest)，下载`Assets`中的`downloader.exe`。

## Usage

![image-20210308204615230](https://i.loli.net/2021/03/08/zVAYweuK7cHk5os.png)

运行`downloader`，输入`阅读全文`之下的链接地址（如图中标黄的位置）。程序会自动爬取当前章节以下的所有章节。

程序会将图片保存在`./clawed`下，并自动生成PDF。

**此程序无需登录即可使用**。

## Q&A

Q: 运行报错`ModuleNotFoundError`，怎么办？

A: 在命令行中运行`pip install -r requirements.txt`以安装依赖。

Q: 运行报错`Cookie Required`，怎么办？

A: 经测试，**绝大部分教参无需`cookie`即可访问**。少数教参需要`cookie`进行身份验证，请将网站`cookie`中，`.ASPXAUTH`和`ASP.NET_SessionId`的值依次写入`cookie.txt`中，每行一个。（我将会完善获取网站`cookie`的相关教程。若急需，请与我发邮件）

Q: 下载的章节不全？

A: 这是因为此图书的目录编号不连续。请再次运行程序并输入下一位置的章节链接。

Q: 分享一点高级玩法？

A: 使用学校提供的正版福昕编辑器可以进行OCR文字识别。

## Advanced Settings

Run `downloader --help` in terminal.

```
usage: downloader.exe [-h] [--url URL] [--no-pdf] [--no-img] [--quality QUALITY] [--con CON] [--resume]

See README.md for help; Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader

optional arguments:
  -h, --help         show this help message and exit
  --url URL          input target URL
  --no-pdf           disable generating PDF
  --no-img           disable saving images
  --quality QUALITY  reduce file size, [1, 96] (85 by recommendation, 96 by default)
  --con CON          the number of concurrent downloads (6 by default)
  --resume           skip downloading images (for testing)
```

希望尝鲜？从GitHub Actions中下载预览版的可执行文件！可执行文件由Pyinstaller打包。

## TODO

- PDF Bookmark
- You tell me

## Contribution

请查看[`contribution.md`](/contribution.md)。

---

欢迎Star/Issue/PR.

*仅供学习编程，请勿用于非法用途！*

更多清华常用信息/服务汇总请看[这里](https://github.com/ZenithalHourlyRate/thuservices)。

