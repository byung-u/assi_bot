#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys 

import configparser
import logging
from typing import List

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from urlget import request_data
from localcode import (local_code_check, select_local_code)

def sendMessage(chat_id: int, meg: str): 
    try:
        bot.sendMessage(chat_id, meg)
    except Exception as e:
        logging.error(e, exc_info=True)


def bot_help(chat_id: int):
    sendMessage(chat_id, 
'''
아파트 전세가
/1 - 지역 아파트 전세 실거래가 (def: /1 11440 201611)
/2 - 지역번호 조회 (def: /2 강남구)
/3 - 내가 거주할 아파트만 조회 (bot.ini 설정 필요)
     예)서울시 강남구 대치동 76.79m²
''')


def get_ty():
    import datetime
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    result_msg = [] 

    url = config.get('TOKEN', 'apt_rent_url')
    svc_key = config.get('TOKEN', 'apt_rent_key', raw=True)

    loc_code = config.get('MY', 'loc_code')
    dong = config.get('MY', 'dong')
    apt = config.get('MY', 'apt')
    size = config.get('MY', 'size')

    init_message = '%s %sm²\n' % (apt, size)
    result_msg.append(init_message)

    for i in range(2, -1, -1):
        if (month - i < 10):
            ymd ='%s0%s' % (year, month-i)
        else: 
            ymd ='%s%s' % (year, month-i)
        request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (url, loc_code, ymd, svc_key)

        res = request_data(request_url, 1, dong, apt, size)
        for j in res:
            encoded_res = j.encode('utf-8')
            result_msg.append(encoded_res)

    return result_msg


def get_apt_rent(command: List[str]):
    result = []

    if (len(command) != 3):
        loc_code = 11440
        ymd = 201610
        # use defult
    else:
        loc_code = command[1]
        ymd = command[2]

    url = config.get('TOKEN', 'apt_rent_url')
    svc_key = config.get('TOKEN', 'apt_rent_key', raw=True)
    request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (url, loc_code, ymd, svc_key)

    result = request_data(request_url)

    return result


def get_loc(command: List[str]):
    result = []

    if (len(command) != 2):
        result = ['Invalid input']
        return result

    result = select_local_code(command[1])
    return result
 

def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    logging.info('content type: %s, chat type: %s, chat id: %s',
            content_type, chat_type, chat_id)

    if content_type != 'text':
        sendMessage(chat_id, "Only text!")

    rcv_msg = msg['text']
    command = rcv_msg.split(' ')

    if command[0] == '/1':
        res_list = get_apt_rent(command)
    elif command[0] == '/2':
        res_list = get_ty()
    elif command[0] == '/3':
        res_list = get_loc(command)
    else:
        bot_help(chat_id)
        return

    if (len(res_list) == 0):
        sendMessage(chat_id, "No result")
    else:
        for res in res_list:
            sendMessage(chat_id, res)
    return


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('callback query :', query_id, from_id, query_data)


if __name__ == '__main__':

    # Check sqlite3 db table, tuple
    local_code_check()

    # Read config
    config = configparser.ConfigParser()
    config.readfp(open('../bot.ini'))

    token = config.get('TOKEN', 'telegram')
    log_level = config.getint('LOG', 'level')

    # Set logging
    logging.basicConfig(filename='bot.log', level=log_level)

    bot = telepot.Bot(token)
    logging.info(bot.getMe())

    bot.message_loop({'chat': on_chat_message,
                      'callback_query': on_callback_query},
                      run_forever='Listening ...')

    sys.exit(0)
