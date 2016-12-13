# -*- coding: utf-8 -*-

import re
from requests import get
from bs4 import BeautifulSoup


def t005():
    url = "http://www.naver.com/"
    r = get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    options = soup.find_all('option')
    realtime_rank = []

    for opt in options:
        opt = str(opt)
        m = re.search('>\d+위:', opt)
        if (m is None):
            continue
        opt = re.sub('<.*?>', '', opt)
        realtime_rank.append(opt)

    if (len(realtime_rank) == 0):
        print("[TEST005][Not OK]")
        return -1
    print("[TEST005][OK]")
    print('\t', realtime_rank)
    return 0
