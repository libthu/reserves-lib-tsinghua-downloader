from html.parser import HTMLParser

import requests


class CustomHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.file_list = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == 'a':
            self.file_list.append(attrs[0][1])


def get_file_list(url: str, session: requests.Session):
    ret = session.get(url)
    ret.raise_for_status()
    parser = CustomHTMLParser()
    parser.feed(ret.text)
    return parser.file_list[1:]
