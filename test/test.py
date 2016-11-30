#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import configparser

from t001_realstate import t001
# t002, t003 pass
from t004_seoul_dust_level import t004
from t005_naver_search_rank import t005
from t006_postal_code import t006

if __name__ == '__main__':
    ok = 0
    nok = 0

    # Read config
    config = configparser.ConfigParser()
    config.readfp(open('../bot.ini'))

    url = config.get('TOKEN', 'apt_rent_url')
    svc_key = config.get('TOKEN', 'apt_rent_key', raw=True)
    request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (url, 11440, 201611, svc_key)

    if (t001(request_url) == 0): ok += 1
    else: nok += 1

    if (t004() == 0): ok += 1
    else: nok += 1

    if (t005() == 0): ok += 1
    else: nok += 1

    if (t006() == 0): ok += 1
    else: nok += 1

    result = "\n\nOK:%d, NOK:%d" % (ok, nok)
    print(result)

    sys.exit(0)
