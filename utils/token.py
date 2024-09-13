import os

import requests
import base64
import json
import time
from selenium import webdriver


def get_token():
    TOKEN_PATH = "token.txt"
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as f:
            data = [v.strip() for v in f.read().splitlines()]
        if len(data) != 1:
            raise Exception(f'Too few or too many lines in "{TOKEN_PATH}"')
        token = data[0]
        try:
            _, payload, _ = token.split(".")
            value = json.loads(base64.b64decode(payload))
            if time.time() > value["exp"] - 60:
                print("Token need to renew.")
                os.remove(TOKEN_PATH)
                return get_token()
        except Exception as e:
            raise Exception(f"Error parsing token in {TOKEN_PATH}: {e}")
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        driver = webdriver.Chrome(options=options)
        driver.get("https://ereserves.lib.tsinghua.edu.cn/login")
        print("Please login in the browser.")
        input("Press Enter after login without closing the browser.")

        token = driver.execute_script("return localStorage.License")
    with open(TOKEN_PATH, "w") as f:
        f.write(token)
    return token


def test_token(url: str, session: requests.Session):
    ret = session.get(url)
    print(ret.text)
