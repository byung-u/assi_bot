# -*- coding: utf-8 -*-
from requests import get
from bs4 import BeautifulSoup


def t006(url, post_key):

    req_url = '%s?ServiceKey=%s&countPerPage=10&currentPage=1&srchwrd=새창로 52' % (url, post_key)
    r = get(req_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    if (len(soup.zipno.string) == 0):
        print("[TEST006][Not OK]")
        return -1
    print("[TEST006][OK]")
    print('\t우편번호: ', soup.zipno.string)
    print('\t주    소: ', soup.lnmadres.string)
    return 0
