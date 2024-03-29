#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   posting_collector.py
@Time    :   2022/01/14 22:43:10
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2021, Freezingdata GmbH
@Desc    :   None
'''

from Gettr.module_tools import *
from Gettr.urls import *
from Gettr.debug import *
from Gettr.api import GattrAPI
from Gettr.data_objects import GettrDataObject

from snhwalker_utils import snhwalker, snh_major_version
import snhwalker_utils  


class PostingCollector:
    def __init__(self, profile, config):
        self.profile = profile
        self.config = config
        self.gettr_posts_list = []
        self.api = GattrAPI()
        pass

    def run(self):
        debugPrint('[START] Python Script: Save posting')
        self.__get_gettr_post_list()
        debugPrint('[COMPLETED] Python Script: Save posting')    

    def __get_gettr_post_list(self):
        url = GetURL_Timeline(self.profile["UserID"])             
        self.api.load_page(url)   

        # Load messages from "Posts" tab
        offset = 0            
        cursor = ''
        object_stringlist = []
        while True:
            debugPrint(f'[Posts] Request posting data (offset={offset})')
            snhwalker.DropStatusMessage(f'Request posting data {offset}')
            gettr_data = self.api.get_posts(self.profile["UserID"], offset, 20, cursor)
            object_stringlist.append(gettr_data)
            debugWrite(f'Gettr_Posts_response_{str(time.time())}.data',gettr_data )
            cursor = GettrDataObject(gettr_data).get_pstfd_cursor() 
            offset += 20
            if cursor == '':
                break
            snhwalker_utils.snh_browser.WaitMS(1000)

        # Load answers from "Replies" tab
        if self.config["SaveComments"] is True:
            comments: list = self.load_comments()
            object_stringlist: list = object_stringlist + comments

        self.convert_and_promote_comments(object_stringlist)

    def load_comments(self) -> list:
        object_stringlist = []
        offset = 0
        cursor = ''
        while True:
            debugPrint(f'[Posts] Request comment data (offset={offset})')
            snhwalker.DropStatusMessage(f'Request answer data {offset}')
            gettr_data = self.api.get_answers(self.profile["UserID"], offset, 20, cursor)
            object_stringlist.append(gettr_data)
            debugWrite(f'Gettr_Comments_response_{str(time.time())}.data', gettr_data)
            cursor = GettrDataObject(gettr_data).get_pstfd_cursor()
            offset += 20
            if cursor == '':
                break
            snhwalker_utils.snh_browser.WaitMS(1000)
        return object_stringlist

    @staticmethod
    def convert_and_promote_comments(object_stringlist) -> None:
        # convert gettr messages to snh data objects
        chatmessage_list = []
        snhwalker.DropStatusMessage(f'Converting messages')
        for data_string in object_stringlist:
            chatmessage_list += GettrDataObject(data_string).as_SNChatmessage_list()

        # submit cSNChatmessages to SNH
        post_count = 0
        max_count = len(chatmessage_list)
        for chat_item in chatmessage_list:
            post_count += 1
            debugPrint(f'[Posts] Handling posting  {post_count}/{max_count} -> {chat_item}')
            snhwalker.PromoteSNChatmessage(chat_item)

    def load_comments_from_current_posting(self, post_id) -> list:
        object_stringlist = []
        offset = 0
        cursor = ''
        while True:
            debugPrint(f'[Posts] Request comment data (offset={offset})')
            snhwalker.DropStatusMessage(f'Request answer data {offset}')
            gettr_data = self.api.get_comments(post_id, offset, 20, cursor)
            object_stringlist.append(gettr_data)
            debugWrite(f'Gettr_Comments_response_{str(time.time())}.data', gettr_data)
            cursor = GettrDataObject(gettr_data).get_next_comment_cursor()
            offset += 20
            if cursor == '':
                break
            snhwalker_utils.snh_browser.WaitMS(1000)
        return object_stringlist