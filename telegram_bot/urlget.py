""" Gathering information by openapi"""

import os
import re
import urllib.request
from bs4 import BeautifulSoup

from typing import List

MAX_LENGTH = 1024

'''
        [1] : 년
        [2] : 동
        [4] : 아파트
        [3] : 보증금액
        [5] : 월
        [6] : 월세 금액
        [7] : 일
        [8] : 전용면적
        [9] : 지번
        [10] : 지역코드
        [11]: 층
        ['', '2016', '상암동', '    15,000', '상암월드컵파크11단지', '11', '       100', '11~20', '84.89', '1741', '11440', '7']
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

        if (info[6].strip() == '0'):
            ret_msg1 = '%s/%s %s층 %s(%s)\n' % (info[5], info[7], info[11].strip(),
                                                info[3].strip(), info[6].strip())
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s/%s %s층 %s(%s)\n' % (info[5], info[7], info[11].strip(),
                                                info[3].strip(), info[6].strip())
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1=''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2=''

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

        if (info[6].strip() == '0'):
            ret_msg1 = '%s/%s %s %s층 %sm² %s(%s)\n' % (info[5], info[7], info[4],
                                                     info[11].strip(), info[8],
                                                     info[3].strip(), info[6].strip())
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s/%s %s %s층 %sm² %s(%s)\n' % (info[5], info[7], info[4],
                                                     info[11].strip(), info[8],
                                                     info[3].strip(), info[6].strip())
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1=''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2=''

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

