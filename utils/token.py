import os

import requests


def get_token():
    TOKEN_PATH = "token.txt"
    if not os.path.exists(TOKEN_PATH):
        print("Cookie Required.")
        print("See README.md for help.")
        print("*" * 30)
        raise FileNotFoundError(f'No such file: "{TOKEN_PATH}"')
    with open(TOKEN_PATH) as f:
        data = [v.strip() for v in f.read().splitlines()]
    if len(data) != 1:
        raise Exception(f'Too many or too many lines in "{TOKEN_PATH}"')

    token = data[0]
    return token


def test_token(url: str, session: requests.Session):
    ret = session.get(url)
    print(ret.text)
