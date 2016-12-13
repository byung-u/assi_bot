# -*- coding: utf-8 -*-
import urllib.request
import json


def t007(client_id, client_secret):
    encText = urllib.parse.quote("나는 누군가?")
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/language/translate"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(req, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        data = response.read()
        data = data.decode('utf-8')
        js = json.loads(data)
        print("[TEST007][OK]")
        print('\t', js['message']['result']['translatedText'])
        return 0
    else:
        print("[TEST007][Not OK]")
        return -1
