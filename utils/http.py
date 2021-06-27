import requests
from html.parser import HTMLParser


def GET(url: str, cookie={}, retry=1) -> requests.Response:
    ret = None
    for _ in range(retry):
        ret = requests.get(url, cookies=cookie)
        if ret.status_code == 200:
            return ret.content
    ret.raise_for_status()


class HTMLParserTHU(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.file_list = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == 'a':
            self.file_list.append(attrs[0][1])


def get_file_list(url: str, cookie, retry):
    text = str(GET(url, cookie, retry))
    parser = HTMLParserTHU()
    parser.feed(text)
    return parser.file_list[1:]
