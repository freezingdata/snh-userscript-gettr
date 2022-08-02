#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   one_posting_collector.py
@Time    :   2022/08/03 12:12:12
@Author  :   Anton Sinaiskii
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2022, Freezingdata GmbH
@Desc    :   None
'''
import json
import time

import snhwalker_utils
from Gettr.debug import *
from Gettr.posting_collector import PostingCollector
from data_objects import GettrDataObject


class OnePostingCollector:
    def __init__(self, url: str, config: dict):
        self.url: str = url
        self.config: dict = config

    def run(self) -> None:
        debugPrint('[START] Python Script: Save posting')
        self.get_data_from_one_posting()
        debugPrint('[COMPLETED] Python Script: Save posting')

    def get_data_from_one_posting(self):
        post_data: list = self.capture_data()
        self.prepare_post_data_to_snh(post_data)

    def capture_data(self) -> list:
        debugPrint(f"[INFO]: Start resource capture. Url: {self.url}")
        CAPTURE_FILTER: str = "api.gettr.com/u/post"
        snhwalker_utils.snh_browser.StartResourceCapture(CAPTURE_FILTER, "")
        snhwalker_utils.snh_browser.LoadPage(self.url)
        snhwalker_utils.snh_browser.WaitMS(3000)

        post_data = snhwalker_utils.snh_browser.FlushResourceCapture()
        break_count = 0

        while not post_data:
            snhwalker_utils.snh_browser.WaitMS(3000)
            break_count += 1
            post_data = snhwalker_utils.snh_browser.FlushResourceCapture()
            if break_count == 5:
                debugPrint("[ERROR]: Bad resource capture. Check capture filter.")
                break

        snhwalker_utils.snh_browser.StopResourceCapture()
        debugPrint(f"[INFO]: Stop resource capture. Data: {post_data[0:200]}...")
        return post_data

    def prepare_post_data_to_snh(self, post_data):
        # We use here the existing implementation of data collection. (GettrDataObject)
        data_fresh = post_data[0].get("response_body")
        data = json.loads(data_fresh)

        unif_data: dict = data["result"]["aux"]["uinf"]
        key = list(unif_data.keys())[0]
        path: dict = data["result"]["aux"]["uinf"][key]

        gettr = GettrDataObject(data_fresh)
        snh_user_data = gettr.uinf_to_snuserdata(path)
        snh_posting_data = gettr.get_chat_messages(data, messages_structure=False)[0]
        snh_posting_data["SenderUser"] = snh_user_data
        snhwalker_utils.snhwalker.PromoteSNChatmessage(snh_posting_data)

        if self.config["SaveComments"] is True:
            posting_collector = PostingCollector(snh_user_data, None)
            comments: list = posting_collector.load_comments()
            posting_collector.convert_and_promote_comments(comments)
