# -*- coding: utf-8 -*-
from requests import get
from bs4 import BeautifulSoup

def t006():
    url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdSearchAllService/retrieveNewAdressAreaCdSearchAllService/getNewAddressListAreaCdSearchAll';
    post_key = 'TT%2B0PoN6%2B%2F3LaMkX1frj5%2BpM%2Bl6YKE00ftdDWZwMyavHKY31LYhiR%2FfwMKSyT9zFW32KTXAn7wpux9jEpb3%2FCg%3D%3D';

    req_url ='%s?ServiceKey=%s&countPerPage=10&currentPage=1&srchwrd=새창로 52' % (url, post_key)
    r = get(req_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    if (len(soup.zipno.string) == 0):
        return -1
    print("[TEST006][OK]")
    print('\t우편번호: ', soup.zipno.string)
    print('\t주    소: ', soup.lnmadres.string)
    return 0
