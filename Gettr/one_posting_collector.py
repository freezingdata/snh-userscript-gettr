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


class PostingCollector:
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


        #return captured_page_data

    def capture_data(self) -> list:
        debugPrint(f"[INFO]: Start resource capture. Url: {self.url}")
        CAPTURE_FILTER: str = "https://api.gettr.com/u/post"
        snhwalker_utils.snh_browser.StartResourceCapture(CAPTURE_FILTER, "")
        snhwalker_utils.snh_browser.LoadPage(self.url)
        snhwalker_utils.snh_browser.WaitMS(3000)

        post_data = snhwalker_utils.snh_browser.FlushResourceCapture()
        break_count = 0
        while post_data == "":
            snhwalker_utils.snh_browser.WaitMS(1000)
            break_count += 1
            post_data = snhwalker_utils.snh_browser.FlushResourceCapture()
            if break_count == 6:
                debugPrint("[ERROR]: Bad resource capture. Check capture filter.")
                break

        snhwalker_utils.snh_browser.StopResourceCapture()
        debugPrint(f"[INFO]: Stop resource capture. Data: {post_data[0:200]}...")
        return post_data

    def prepare_post_data_to_snh(self, post_data):
        print(post_data)

