# 清华教参服务平台 辅助工具

![GitHub release (latest by date)](https://img.shields.io/github/v/release/i207M/reserves-lib-tsinghua-downloader) ![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/i207M/reserves-lib-tsinghua-downloader/Release%20Test/main) ![GitHub issues](https://img.shields.io/github/issues/i207M/reserves-lib-tsinghua-downloader) [![Netlify Status](https://api.netlify.com/api/v1/badges/d6a79087-90b9-4659-9700-acd47b95cd9b/deploy-status)](https://reserves-lib.netlify.app/)

Download pages from http://reserves.lib.tsinghua.edu.cn/

自动下载书籍每一页的原图，生成PDF，免登录。

## Download

从[Releases](https://github.com/i207M/reserves-lib-tsinghua-downloader/releases/latest)或[项目网站](https://reserves-lib.netlify.app/)，下载`Assets`中对应系统的可执行文件。

## Usage

![image-20210308204615230](https://i.loli.net/2021/03/08/zVAYweuK7cHk5os.png)

运行`downloader`，输入网站“`阅读全文`”之下的链接地址（如图中标黄的位置）。程序会自动爬取当前章节以下的所有章节。

程序会将图片保存在`./clawed`下，并自动生成PDF。

**此程序无需登录即可使用**。

### MacOS

MacOS用户可能无法直接运行下载的`downloader`，是因为它没有被标记为“可执行的”。

解决方法：在终端中进入`downloader`文件所在的文件夹，执行`chmod +x downloader`命令。有关此命令的更多帮助请参阅[Apple](https://support.apple.com/zh-cn/guide/terminal/apdd100908f-06b3-4e63-8a87-32e71241bab4/mac)。

MacOS上的第一次启动可能会有点慢。

## Q&A

**Q:** 图片压缩的`quality ratio`怎样设置？

A: 范围[1, 96]：其中96为不压缩，[1, 95]从最差到最佳。

**Q:** 运行报错`Cookie Required`，怎么办？

A: 经测试，绝大部分教参无需`cookie`即可访问。少数教参需要`cookie`进行身份验证，请将网站`cookie`中，`.ASPXAUTH`和`ASP.NET_SessionId`的值依次写入`cookie.txt`中，每行一个。（我将会完善获取网站`cookie`的相关教程。若急需，请与我发邮件）

**Q:** 下载的章节不全？

A: 这是因为此图书的目录编号不连续。请再次运行程序并输入下一位置的章节链接。通常不会出现此情况。

**Q:** 分享一点高级玩法？

A: 使用学校提供的正版福昕编辑器可以进行OCR文字识别。

## Advanced Settings

Run `downloader --help` in terminal.

```
usage: downloader.exe [-h] [--url URL] [--no-pdf] [--no-img] [--quality QUALITY] [--con CON] [--resume]

See README.md for help. Repo: https://github.com/i207M/reserves-lib-tsinghua-downloader

optional arguments:
  -h, --help         show this help message and exit
  --url URL          input target URL
  --no-pdf           disable generating PDF
  --no-img           disable saving images
  --quality QUALITY  reduce file size, [1, 96] (75 by recommendation, 96 by default)
  --con CON          the number of concurrent downloads (6 by default)
  --resume           skip downloading images (for testing)
```

希望尝鲜？从GitHub Actions中下载预览版的可执行文件！

## TODO

- PDF Bookmark
- You tell me

## Contribution

请查看[`contribution.md`](/contribution.md)。

欢迎Star/Issue/PR~

---

*仅供Python语言的学习参考，请勿用于非法用途！*

更多清华常用信息/服务汇总请看[这里](https://github.com/ZenithalHourlyRate/thuservices)。
