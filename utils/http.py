import requests
from html.parser import HTMLParser


class SessionTHU:
    def __init__(self, cookie, retry) -> None:
        self.s = requests.session()
        self.s.cookies = requests.utils.cookiejar_from_dict(cookie)
        self.retry = retry

    def GET(self, url: str) -> requests.Response:
        ret = None
        for _ in range(self.retry):
            ret = self.s.get(url)
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


def get_file_list(url: str, session: SessionTHU):
    text = str(session.GET(url))
    parser = HTMLParserTHU()
    parser.feed(text)
    return parser.file_list[1:]
