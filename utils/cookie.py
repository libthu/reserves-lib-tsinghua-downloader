import os


def get_cookie():
    COOKIE_PATH = 'cookie.txt'
    cookie = {}

    if not os.path.exists(COOKIE_PATH):
        raise FileNotFoundError(f'No such file: "{COOKIE_PATH}"\nSee README.md for help.')
    with open(COOKIE_PATH) as f:
        data = [v.strip() for v in f.read().splitlines()]
        if len(data) != 2:
            raise Exception(f'Too many or too few lines in "{COOKIE_PATH}"')
        cookie['.ASPXAUTH'] = data[0]
        cookie['ASP.NET_SessionId'] = data[1]
    return cookie
