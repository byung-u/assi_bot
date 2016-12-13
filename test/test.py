#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
import configparser

from t001_realstate import t001
# t002, t003 pass
from t004_seoul_dust_level import t004
from t005_naver_search_rank import t005
from t006_postal_code import t006
from t007_naver_translate import t007
from t008_realstate_trade import t008

if __name__ == '__main__':
    ok = 0
    nok = 0
    not_check = 0

    # Read config
    config = configparser.ConfigParser()
    config.readfp(open('../bot.ini'))

    url = config.get('TOKEN', 'apt_rent_url')
    svc_key = config.get('TOKEN', 'apt_key', raw=True)
    request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (url, 11440, 201611, svc_key)

    if (t001(request_url) == 0):
        ok += 1
    else:
        nok += 1

    not_check += 2  # t002, t003

    if (t004() == 0):
        ok += 1
    else:
        nok += 1

    if (t005() == 0):
        ok += 1
    else:
        nok += 1

    url = config.get('TOKEN', 'postal_code_url', raw=True)
    post_key = config.get('TOKEN', 'postal_code_key', raw=True)
    if (t006(url, post_key) == 0):
        ok += 1
    else:
        nok += 1

    n_id = config.get('TOKEN', 'naver_client_id')
    n_secret = config.get('TOKEN', 'naver_client_secret')
    if (t007(n_id, n_secret) == 0):
        ok += 1
    else:
        nok += 1

    url = config.get('TOKEN', 'apt_trade_url')
    request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (url, 11440, 201611, svc_key)
    if (t008(request_url) == 0):
        ok += 1
    else:
        nok += 1

 
    result = "\n\nOK:%d, PASS:%d, NOK:%d" % (ok, not_check, nok)
    print(result)

    sys.exit(0)
