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
from Gettr.data_objects import GettrDataObject
from Gettr.urls import GettrUrlResolver, GETTR_POST_PAGE, GETTR_COMMENT_PAGE


class OnePostingCollector:
    def __init__(self, url: str, config: dict):
        self.url: str = url
        self.config: dict = config
        self.url_resolver = GettrUrlResolver(self.url)

    def run(self) -> None:
        debugPrint('[START] Python Script: Save posting')
        self.get_data_from_one_posting()
        debugPrint('[COMPLETED] Python Script: Save posting')

    def get_data_from_one_posting(self) -> None:
        post_data: list = self.capture_data()
        self.prepare_post_data_to_snh(post_data)

    def capture_data(self) -> list:
        debugPrint(f"[INFO]: Start resource capture. Url: {self.url}")
        if self.url_resolver.get_page_type() == GETTR_POST_PAGE:
            CAPTURE_FILTER: str = "api.gettr.com/u/post"
        elif self.url_resolver.get_page_type() == GETTR_COMMENT_PAGE:
            CAPTURE_FILTER: str = "api.gettr.com/u/comment"
        else:
            debugPrint("[ERROR]: Bad capture filter. Check capture filter.")
            return [{}]

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

    def prepare_post_data_to_snh(self, post_data: list) -> None:
        # We use here the existing implementation of data collection. (GettrDataObject)
        data_fresh = post_data[0].get("response_body")
        data = json.loads(data_fresh)

        # We prepare here dict-path for use existing methods
        unif_data: dict = data["result"]["aux"]["uinf"]
        key = list(unif_data.keys())[0]
        path: dict = data["result"]["aux"]["uinf"][key]

        gettr = GettrDataObject(data_fresh)
        snh_user_data: dict = gettr.uinf_to_snuserdata(path)
        snh_posting_data: dict = gettr.get_chat_messages(data, messages_structure=False)[0]
        snh_posting_data["SenderUser"] = snh_user_data
        snh_posting_data["ChatURL"] = f'https://gettr.com/post/{snh_posting_data["UniqueIDNetwork"]}'
        snhwalker_utils.snhwalker.PromoteSNChatmessage(snh_posting_data)

        if self.config["SaveComments"] is True:
            comments_list = []
            posting_collector = PostingCollector(snh_user_data, None)
            comments_pack: list = posting_collector.load_comments_from_current_posting(snh_posting_data.get("UniqueIDNetwork"))
            for comments in comments_pack:
                gettr = GettrDataObject(comments)
                comments_list += gettr.as_SNChatmessage_list(messages_structure=False)

            post_count = 0
            max_count = len(comments_list)
            for chat_item in comments_list:
                post_count += 1
                debugPrint(f'[Posts] Handling posting  {post_count}/{max_count} -> {chat_item}')
                snhwalker_utils.snhwalker.PromoteSNChatmessage(chat_item)

    @classmethod
    def handle_post(cls):
        GETTR_URL = "https://gettr.com/"
        QS = "querySelector"
        QSA = "querySelectorAll"
        CHAT_URL_JS = "window.location.href"
        USER_DATA_JS = f"""document.{QS}("div[class='body-content']").{QSA}("div[class*='MuiBox-root']")[0]"""
        PICTURE_JS = f"""{USER_DATA_JS}.{QS}("div[id='hoverPopup']").{QS}("img").getAttribute("src")"""
        USER_NAME_JS = f"""{USER_DATA_JS}.{QS}("div[id='hoverPopup']").{QS}("img").getAttribute("alt")"""
        USER_URL_JS = f"""{USER_DATA_JS}.{QS}("div[id='hoverPopup']").{QS}("a").getAttribute("href")"""
        USER_ID_JS = f"""a.{QS}("div[class*='MuiBox']").{QS}("div[class*='MuiBox']")[1].{QS}("div").textContent"""
        CONTENT_JS = f"""document.{QS}("div[class='body-content']").{QS}("div[class*='text-content']").textContent"""

        # Prepare snh profile
        snh_profile = snhwalker_utils.snh_model_manager.CreateDictSNUserData()
        profile_data = {
            'UserName': snhwalker_utils.snh_browser.GetJavascriptString(USER_NAME_JS),
            'UserURL': f"{GETTR_URL}{snhwalker_utils.snh_browser.GetJavascriptString(USER_URL_JS)}",
            'UserProfilePictureURL': snhwalker_utils.snh_browser.GetJavascriptString(PICTURE_JS),
            'UserID': snhwalker_utils.snh_browser.GetJavascriptString(USER_ID_JS),
        }
        snh_profile.update(profile_data)

        # Prepare snh chat message
        snh_chat_message = snhwalker_utils.snh_model_manager.CreateDictSNChatmessage()
        posting_data = {
            'Text': snhwalker_utils.snh_browser.GetJavascriptString(CONTENT_JS),
            'ChatURL': snhwalker_utils.snh_browser.GetJavascriptString(CHAT_URL_JS),
            'SenderUser': snh_profile,
        }
        snh_chat_message.update(posting_data)
        snhwalker_utils.snhwalker.PromoteSNChatmessage(snh_chat_message)

