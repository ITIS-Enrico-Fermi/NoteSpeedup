#!/usr/bin/env python3

import requests
import re

def get_title(url):
    response = requests.get(url)
    title = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE).group(1)
    return title

def to_markdown(url):
    title = get_title(url)

    return f"[{title}]({url})"

if __name__ == "__main__":
    url = input()
    print(to_markdown(url))