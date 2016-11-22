""" Gathering information by openapi"""
# -*- coding: utf-8 -*-

import re
import urllib.request
from bs4 import BeautifulSoup
from typing import List

MAX_LENGTH = 1024

'''
1<건축년도>2007</건축년도>
2<년>2015</년>
3<법정동>필운동</법정동>
4<보증금액>65,000</보증금액>
5<아파트>신동아블루아광화문의 꿈</아파트>
6<월>12</월>
7<월세금액>0</월세금액>
8<일>1~10</일>
9<전용면적>111.97</전용면적>
10<지번>254</지번>
11<지역코드>11110</지역코드>
12<층>7</층>
'''
def request_3month(url: str, dong: str, apt: str, size: str) -> List[str]:


    result = []

    ret_msg1 = ''  # 전세
    result_msg1 = ''
    ret_msg2 = ''  # 월세
    result_msg2 = ''

    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        result = ['Check your input']
        return result

    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = item.text
        item = re.sub('<.*?>', '|', item)
        info = item.split('|')

        if (info[2] != dong):
            continue
        if (info[4] != apt):
            continue
        if (info[8] != size):
            continue

        for i in range(0, len(info)):
            info[i] = info[i].strip()

        if (info[6] == '0'):
            ret_msg1 = '%s/%s %s층 %s(%s)\n' % (info[6], info[8], info[12],
                                                info[4], info[7])
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s/%s %s층 %s(%s)\n' % (info[6], info[8], info[12],
                                                info[4], info[7])
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1=''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2=''

    if (len(result_msg1) == 0 and len(result_msg2) == 0 and len(result) == 0):
        result = ['Not found']
    else:
        result.append(result_msg1)
        result.append(result_msg2)
    return result


def request_all(url: str) -> List[str]:

    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        result = ['Check your input']
        return result

    result = []
    ret_msg1 = ''  # 전세
    ret_msg2 = ''  # 월세
    result_msg1 = ''
    result_msg2 = ''

    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = item.text
        item = re.sub('<.*?>', '|', item)
        info = item.split('|')
        for i in range(0, len(info)):
            info[i] = info[i].strip()

        if (info[6] == '0'):
            ret_msg1 = '%s %s(%s) %s층 %sm² %s(%s) 준공:%s\n' % (info[3], info[5], info[8], 
                                                                 info[12], info[9], info[4], 
                                                                 info[7], info[1])
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s %s(%s) %s층 %sm² %s(%s) 준공:%s\n' % (info[3], info[5], info[8], 
                                                                 info[12], info[9], info[4], 
                                                                 info[7], info[1])
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1=''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2=''

    if (len(result_msg1) == 0 and len(result_msg2) == 0 and len(result) == 0):
        result = ['Not found']
    else:
        result.append(result_msg1)
        result.append(result_msg2)

    return result


def request_data(url: List[str], 
        specific: int = 0, dong: str = None, 
        apt: str = None, size: str = None) -> List[str]:

    result = []
    if (specific):
        result = request_3month(url, dong, apt, size)
    else:
        result = request_all(url)

    return result
