#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys 
import configparser
import logging
from typing import List

import telepot

from urlget import (request_data, request_naver_rank, request_seoul_dust,
                    request_postal_code)
from localcode import (localcode_db_check, select_local_code)

MAX_ARGUMENTS = 10

class Assi:

    def __init__(self):
        # Check sqlite3 db table, tuple
        localcode_db_check()

        # Read config
        self.config = configparser.ConfigParser()
        self.config.readfp(open('../bot.ini'))
        self.telegram_token = self.config.get('TOKEN', 'telegram')

        self.bot = telepot.Bot(self.telegram_token)

        log_level = self.config.getint('LOG', 'level')
        logging.basicConfig(filename='bot.log', level=log_level)
        logging.info(self.bot.getMe())
 
        self.apt_rent_url = self.config.get('TOKEN', 'apt_rent_url')
        self.apt_rent_svckey = self.config.get('TOKEN', 'apt_rent_key', raw=True)

        self.postal_code_url = self.config.get('TOKEN', 'postal_code_url')
        self.postal_code_key = self.config.get('TOKEN', 'postal_code_key', raw=True)

    def send(self, chat_id: int, msg: str): 
        print(chat_id)
        try:
            self.bot.sendMessage(chat_id, msg)
        except Exception as e:
            logging.error(e, exc_info=True)
    
    
    def bot_help(self, chat_id: int):
        self.bot.sendMessage(chat_id, 
'''
아파트 전세가
/1 - 지역 아파트 전세 실거래가 (def: /1 11440 201611)
/2 - 지역번호 조회 (def: /2 강남구)
/3 - 내가 거주할 아파트만 조회 (bot.ini 설정 필요)
     예)서울시 강남구 대치동 76.79m²
/4 - 서울 미세먼지 농도
/5 - 네이버 실시간 검색 순위
/6 - 우편번호 검색 (def: /6 독립문로14길 33)
'''
        )

 
    def get_apt_rent(self, command: List[str]):
        result = []
    
        if (len(command) != 3):
            # use defult
            loc_code = 11440
            ymd = 201611
        else:
            loc_code = command[1]
            ymd = command[2]
    
        request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (self.apt_rent_url, 
                loc_code, ymd, self.apt_rent_svckey)
    
        result = request_data(request_url)
        return result


    def get_loc(self, command: List[str]):
        result = []
    
        district = ''
        if (len(command) != 2):
            # use defult
            district = '강남구'
        else:
            district = command[1]
    
        result = select_local_code(district)
        return result


    def get_ty(self):
        import datetime
        now = datetime.datetime.now()
        month = now.month
        year = now.year
    
        result_msg = [] 
    
        loc_code = self.config.get('MY', 'loc_code')
        dong = self.config.get('MY', 'dong')
        apt = self.config.get('MY', 'apt')
        size = self.config.get('MY', 'size')
    
        init_message = '%s %sm²\n' % (apt, size)
        result_msg.append(init_message)
    
        for i in range(2, -1, -1):
            if (month - i < 10):
                ymd ='%s0%s' % (year, month-i)
            else: 
                ymd ='%s%s' % (year, month-i)
            request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (self.apt_rent_url, 
                    loc_code, ymd, self.apt_rent_svckey)
            res = request_data(request_url, 1, dong, apt, size)
    
            for j in res:
                encoded_res = j.encode('utf-8')
                result_msg.append(encoded_res)
    
        return result_msg
    

    def get_seoul_dust(self):
        result = []
        result = request_seoul_dust()
        return result

   
    def get_naver_search_rank(self):
        result = []
        result = request_naver_rank()
        return result


    def get_postal_code(self, command: List[str]):
        result = []
        if (len(command) != 3):
            req_url = '%s?ServiceKey=%s&countPerPage=10&currentPage=1&srchwrd=독립문로14길 33' % (
                    self.postal_code_url, self.postal_code_key)
        else:
            req_url = '%s?ServiceKey=%s&countPerPage=10&currentPage=1&srchwrd=%s %s' % (
                    self.postal_code_url, self.postal_code_key, 
                    command[1], command[2])

        result = request_postal_code(req_url)
        return result
    

def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    logging.info('content type: %s, chat type: %s, chat id: %s',
            content_type, chat_type, chat_id)

    if content_type != 'text':
        send(chat_id, "Only text!")

    rcv_msg = msg['text']
    command = rcv_msg.split(' ')

    if (len(command) > 10):
        send(chat_id, "Too many argument")
        return

    if command[0] == '/1':
        res_list = assi.get_apt_rent(command)
    elif command[0] == '/2':
        res_list = assi.get_loc(command)
    elif command[0] == '/3':
        res_list = assi.get_ty()
    elif command[0] == '/4':
        res_list = assi.get_seoul_dust()
    elif command[0] == '/5':
        res_list = assi.get_naver_search_rank()
    elif command[0] == '/6':
        res_list = assi.get_postal_code(command)
    else:
        assi.bot_help(chat_id)
        return

    if (len(res_list) == 0):
        assi.send(chat_id, "No result")
    else:
        for res in res_list:
            assi.send(chat_id, res)
    return


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('callback query :', query_id, from_id, query_data)


if __name__ == '__main__':

    assi = Assi()
    assi.bot.message_loop({'chat': on_chat_message,
                           'callback_query': on_callback_query},
                           run_forever='Listening ...')

    sys.exit(0)
