#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   api.py
@Time    :   2022/01/14 22:55:51
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2021, Freezingdata GmbH
@Desc    :   None
'''

from Gettr.module_tools import *
from Gettr.urls import *
from Gettr.debug import *

from snhwalker_utils import snhwalker, snh_major_version
import snhwalker_utils   
import uuid
import sys
import requests
from requests.structures import CaseInsensitiveDict

class GattrAPI:
    def __init__(self):
        self.x_app_auth = ''
        self.version = ''

        self.useragent = ''

        pass

    def load_page(self, url):
        snhwalker_utils.snh_browser.StartResourceCapture('https://api.gettr.com/', '')
        snhwalker_utils.snh_browser.LoadPage(url)
        snhwalker_utils.snh_browser.StopResourceCapture() 
        last_request_header = snhwalker_utils.snh_browser.GetResourceHeader()
        debugPrint(f'[API]  Resource header -> {last_request_header}')
        self.x_app_auth = getRegex(last_request_header, 'x-app-auth=(\{.*?\})', 1)
        self.version = getRegex(last_request_header, ';ver=(.*?);', 1)
        self.useragent = getRegex(last_request_header, ';User-Agent=(.*?);[^;]+?\=', 1)
        debugPrint(f'[API]  x_app_auth -> {self.x_app_auth}')


    def get_unif(self, user_id):
        response_data = self.__get_request(f'https://api.gettr.com/s/uinf/{user_id}')
        debugPrint(f'[API] Response unif -> {response_data[0:100]}')
        return response_data

    def get_follower(self, user_id, offset, max = 20):
        response_data = self.__get_request(f'https://api.gettr.com/u/user/{user_id}/followers/?offset={offset}&max={max}&incl=userstats|userinfo|followings|followers')
        debugPrint(f'[API] Response followers -> {response_data[0:100]}')
        return response_data

    def get_followings(self, user_id, offset, max = 20):
        response_data = self.__get_request(f'https://api.gettr.com/u/user/{user_id}/followings/?offset={offset}&max={max}&incl=userstats|userinfo|followings|followers')
        debugPrint(f'[API] Response followings -> {response_data[0:100]}')
        return response_data        

    def get_posts(self, user_id, offset, max, cursor = ''):
        response_data = self.__get_request(f'https://api.gettr.com/u/user/{user_id}/posts/?offset={offset}&dir=fwd&max={max}&incl=posts|stats|userinfo|shared|liked&fp=f_uo&cursor={cursor}')
        debugPrint(f'[API] Response posts -> {response_data[0:100]}')
        return response_data       

    def get_answers(self, user_id, offset, max, cursor = ''):
        response_data = self.__get_request(f'https://api.gettr.com/u/user/{user_id}/posts/?offset={offset}&dir=fwd&max={max}&incl=posts|stats|userinfo|shared|liked&fp=f_uc&cursor={cursor}')
        debugPrint(f'[API] Response answers -> {response_data[0:100]}')
        return response_data                

    def __get_request(self, requesturl):
        debugPrint(f'[API] Request: {requesturl}')
        headers = CaseInsensitiveDict()
        headers["User-Agent"] = self.useragent
        headers["Accept"] = "application/json, text/plain, */*"
        headers["Accept-Language"] = "de,en-US;q=0.7,en;q=0.3"
        headers["Referer"] = "https://gettr.com/"
        headers["Connection"] = "keep-alive"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "no-cors"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Pragma"] = "no-cache"
        headers["Cache-Control"] = "no-cache"
        headers["TE"] = "trailers"
        headers["x_app_auth"] = self.version
        headers["ver"] = self.x_app_auth
        try:
            resp = requests.get(requesturl, headers=headers)   
            debugWrite('Gettr_API_response_'+str(time.time())+'.data', resp.text )        
            return resp.text     
        except Exception as e:
            debugPrint("'[API] ERROR in get_request")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            debugPrint(e, exc_type, exc_tb.tb_lineno)   
            return ''

        