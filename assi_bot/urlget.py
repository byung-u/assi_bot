""" Gathering information by openapi"""
# -*- coding: utf-8 -*-

import re
import urllib.request
from bs4 import BeautifulSoup
from typing import List
from requests import get
import json

MAX_LENGTH = 1024


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

        if (info[3] != dong):
            continue
        if (info[5] != apt):
            continue
        if (info[9] != size):
            continue

        for i in range(0, len(info)):
            info[i] = info[i].strip()

        if (info[6] == '0'):
            ret_msg1 = '%s/%s %s층 %s(%s)\n' % (
                    info[6], info[8], info[12], info[4], info[7])
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s/%s %s층 %s(%s)\n' % (
                    info[6], info[8], info[12], info[4], info[7])
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1 = ''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2 = ''

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
            ret_msg1 = '%s %s(%s) %s층 %sm² %s(%s) 준공:%s\n' % (
                    info[3], info[5], info[8], info[12],
                    info[9], info[4], info[7], info[1])
            result_msg1 = '%s%s' % (result_msg1, ret_msg1)
        else:
            ret_msg2 = '%s %s(%s) %s층 %sm² %s(%s) 준공:%s\n' % (
                    info[3], info[5], info[8], info[12],
                    info[9], info[4], info[7], info[1])
            result_msg2 = '%s%s' % (result_msg2, ret_msg2)

        if (len(result_msg1) > MAX_LENGTH):
            result.append(result_msg1)
            result_msg1 = ''
        if (len(result_msg2) > MAX_LENGTH):
            result.append(result_msg2)
            result_msg2 = ''

    if (len(result_msg1) == 0 and len(result_msg2) == 0 and len(result) == 0):
        result = ['Not found']
    else:
        result.append(result_msg1)
        result.append(result_msg2)

    return result


def request_data(
        url: List[str], specific: int = 0, dong: str = None,
        apt: str = None, size: str = None) -> List[str]:

    result = []
    if (specific):
        result = request_3month(url, dong, apt, size)
    else:
        result = request_all(url)

    return result


def request_seoul_dust() -> List[str]:

    url = 'http://openAPI.seoul.go.kr:8088/756e6d666b6a656f38346e764e734e/xml/ForecastWarningMinuteParticleOfDustService/1/1/'

    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        print('UnicodeEncodeError')
        return -1

    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')

    seoul_dust = []
    result = ""

    if (len(soup.caistep.string) == 0) or (len(soup.alarm_cndt.string) == 0):
        result = '[ERR]: [%s]\n%s' % (
                soup.caistep.string, soup.alarm_cndt.string)
        result = ['Not found']
        seoul_dust.append(result)
    else:
        # OK
        result = '\t[%s]\n\t%s' % (soup.caistep.string, soup.alarm_cndt.string)
        seoul_dust.append(result)

    return seoul_dust


def request_naver_rank() -> List[str]:

    url = "http://www.naver.com/"
    r = get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    options = soup.find_all('option')
    realtime_rank = []
    result = ""

    for opt in options:
        opt = str(opt)
        m = re.search('>\d+위:', opt)
        if (m is None):
            continue
        opt = re.sub('<.*?>', '', opt)
        result = "%s\n%s" % (result, opt)

    if (len(result) == 0):
        realtime_rank = ['Not found']

    realtime_rank.append(result)
    return realtime_rank


def request_postal_code(req_url) -> List[str]:
    postal_code = []
    r = get(req_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if (len(soup.zipno.string) == 0):
        result = ['Not found']
    else:
        result = "우편번호: %s\n주소: %s" % (
                soup.zipno.string, soup.lnmadres.string)

    postal_code.append(result)
    return postal_code


def request_naver_translate(n_id, n_secret, command) -> List[str]:
    output = []

    input_str = ' '.join(command[1:])
    encText = urllib.parse.quote(input_str)

    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/language/translate"

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", n_id)
    req.add_header("X-Naver-Client-Secret", n_secret)
    response = urllib.request.urlopen(req, data=data.encode("utf-8"))

    rescode = response.getcode()
    if (rescode == 200):
        data = response.read()
        data = data.decode('utf-8')
        js = json.loads(data)
        result = '입력: %s\n결과: %s\n' % (
                input_str, js['message']['result']['translatedText'])
        output.append(result)
    else:
        output.append(['Error'])

    return output
