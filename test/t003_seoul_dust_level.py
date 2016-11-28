# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup

def t003():
    url = 'http://openAPI.seoul.go.kr:8088/756e6d666b6a656f38346e764e734e/xml/ForecastWarningMinuteParticleOfDustService/1/1/';
    
    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        print('UnicodeEncodeError')
        return -1
    
    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')

    if (len(soup.caistep.string) == 0) or (len(soup.alarm_cndt.string) == 0):
        result = '[ERR]: [%s]\n%s' % (soup.caistep.string, soup.alarm_cndt.string)
        print(result)
        return -1
    
    print("\n[TEST003][OK]")
    result = '\t[%s]\n\t%s' % (soup.caistep.string, soup.alarm_cndt.string)
    print(result)
    return 0
    
