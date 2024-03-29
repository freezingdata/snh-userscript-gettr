#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   api_data_converter.py
@Time    :   2022/01/14 23:11:25
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
import json
import sys
from urllib.parse import urlparse

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

class GettrDataObject:
    def __init__(self, json_string) -> None:
        self.data_string = json_string
        self.json_valid= True
        try:
            self.data = json.loads(json_string)        
        except:
            self.json_valid = False
        pass

    def is_valid(self):
        if self.json_valid is True:
            if not ("rc" in self.data):
                return False
            if not ("result" in self.data):
                return False            
            if not (self.data["rc"] == "OK"):
                return False
            return True
        else:
            return False

    def is_uinf(self):
        if not (self.is_valid() is True):
            return False
        if not (self.data["result"]["serial"] == "uinf"):
            return False
        return True

    def is_rslst(self):
        if not (self.is_valid() is True):
            return False
        if not (self.data["result"]["serial"] == "rslst"):
            return False
        return True     

    def is_pstfd(self):
        if not (self.is_valid() is True):
            return False
        if not (self.data["result"]["serial"] == "pstfd"):
            return False
        return True            

    def get_rslst_cursor(self):
        if self.is_rslst() is True:    
            return self.data["result"]["aux"]["cursor"]
        return 0

    def get_pstfd_cursor(self):
        if self.is_pstfd() is True:    
            if not (self.data["result"]["aux"]["cursor"] == 0):
                return self.data["result"]["aux"]["cursor"]         
        return ''        

    def get_next_comment_cursor(self):
        if not (self.data["result"]["aux"]["cursor"] == 0):
            return self.data["result"]["aux"]["cursor"]
        return ''

    def as_userlist(self):
        return_list = []
        if self.is_rslst() is True:
            for attribute, item in self.data["result"]["aux"]["uinf"].items():
                ProfileData = self.uinf_to_snuserdata(item)
                return_list.append(ProfileData)
        return return_list

    def as_gettr_post_list(self):
        return_list = []
        if self.is_pstfd() is True:
            for attribute, item in self.data["result"]["aux"]["post"].items():
                return_list.append(item)
        return return_list        

    @classmethod
    def uinf_to_snuserdata(cls, unif_data):
        ProfileData = snhwalker_utils.snh_model_manager.CreateDictSNUserData()
 
        ProfileData['ProfileType'] = 0
        ProfileData['UserIDNumber'] = unif_data['_id']
        ProfileData['UserID'] = unif_data['_id']
        ProfileData['UserURL'] = GetURL_Profile(ProfileData['UserID'], ProfileData['UserIDNumber'])
        if "nickname" in unif_data:
            ProfileData['UserName'] = unif_data['nickname']
        else:
            ProfileData['UserName'] = unif_data['username']
        if "ico" in unif_data:   
            ProfileData['UserProfilePictureURL'] = "https://media.gettr.com/" + unif_data['ico']               
        return ProfileData

    def as_SNUserData(self):
        ProfileData = snhwalker_utils.snh_model_manager.CreateDictSNUserData()
        if self.is_uinf() is True:
            unif_data = self.data["result"]["data"]
            ProfileData =self.uinf_to_snuserdata(unif_data)
        else:
            debugPrint(f'API DataObject -> as_SNUserData: No uinf data object')  
        return ProfileData

    def as_SNUserdetailsItem_list(self):
        return_list = []
        if not self.is_uinf() is True:
            return []
        unif_data = self.data["result"]["data"]
        if "location" in unif_data:
            DetailLocation = snhwalker_utils.snh_model_manager.CreateDictSNUserdetailsItem()
            DetailLocation['DetailType'] = 'CurrentCity'        
            DetailLocation['DetailMainContent'] = unif_data["location"]
            return_list.append(DetailLocation)
        if "dsc" in unif_data:
            DetailDsc = snhwalker_utils.snh_model_manager.CreateDictSNUserdetailsItem()
            DetailDsc['DetailType'] = 'Description'        
            DetailDsc['DetailMainContent'] = unif_data["dsc"]
            return_list.append(DetailDsc)     
        if "website" in unif_data:
            DetailWeb = snhwalker_utils.snh_model_manager.CreateDictSNUserdetailsItem()
            DetailWeb['DetailType'] = 'Website'        
            DetailWeb['DetailMainContent'] = unif_data["website"]
            return_list.append(DetailWeb)       
        return return_list              

    def as_SNChatmessage_list(self, messages_structure=True):
        return_list = []
        try:
            if self.is_pstfd() is False and messages_structure:
                return []
            for list_item in self.data["result"]["data"]["list"]:
                result = self.get_chat_messages(list_item, messages_structure)
                return_list.append(result)
            flat_return_list = [item for sublist in return_list for item in sublist]
            return flat_return_list

        except Exception as e:
            debugPrint("[API DataObject] ERROR in Chat conversion")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            debugPrint(e, exc_type, exc_tb.tb_lineno)  
            return []

    def get_chat_messages(self, list_item, messages_structure=True):
        return_list = []
        chat_message = snhwalker_utils.snh_model_manager.CreateDictSNChatmessage()
        if messages_structure:
            post_id = list_item["activity"]["pstid"]
            post_data = self.data["result"]["aux"]["post"][post_id]
        else:
            try:
                post_id = list_item["result"]["data"]["_id"]
                post_data = list_item["result"]["data"]
                list_item["action"] = "pub_pst"
            except KeyError:
                post_id = list_item["_id"]
                post_data = list_item
                list_item["action"] = "pub_cm"

        if "txt" in post_data:
            chat_message["Text"] = post_data["txt"]
        if "prevsrc" in post_data:
            chat_message["LinkURL"] = post_data["prevsrc"]
        if ('img' in post_data) and (len(post_data["img"]) > 0):  # deprecated?
            if uri_validator(post_data["img"][0]) is False:
                chat_message["ImageURL"] = "https://media.gettr.com/" + post_data["img"][0]
            else:
                chat_message["ImageURL"] = post_data["img"][0]
        if ('imgs' in post_data) and (len(post_data["imgs"]) > 0):
            if uri_validator(post_data["imgs"][0]) is False:
                chat_message["ImageURL"] = "https://media.gettr.com/" + post_data["imgs"][0]
            else:
                chat_message["ImageURL"] = post_data["imgs"][0]
        if ('previmg' in post_data):
            if uri_validator(post_data["previmg"]) is False:
                chat_message["ImageURL"] = "https://media.gettr.com/" + post_data["previmg"]
            else:
                chat_message["ImageURL"] = post_data["previmg"]
        if ('ovid' in post_data):
            if uri_validator(post_data["ovid"]) is False:
                chat_message["ImageURL"] = "https://media.gettr.com/" + post_data["ovid"]
            else:
                chat_message["ImageURL"] = post_data["ovid"]

        if list_item.get("action") == "pub_pst":
            chat_message["Timestamp"] = post_data["cdate"] / 1000
            chat_message["UniqueIDNetwork"] = post_data["_id"]
            chat_message["ChatParentID"] = "-1"
            if messages_structure:
                chat_message["SenderUser"] = self.uinf_to_snuserdata(
                    self.data["result"]["aux"]["uinf"][list_item["activity"]["uid"]])
            else:
                pass
            return_list.append(chat_message)

        elif list_item.get("action") == "shares_pst":
            # 1. add repost to list
            chat_message["Timestamp"] = list_item["activity"]["cdate"] / 1000
            chat_message["UniqueIDNetwork"] = list_item["activity"]["_id"]
            chat_message["ChatParentID"] = post_id
            chat_message["SenderUser"] = self.uinf_to_snuserdata(self.data["result"]["aux"]["uinf"][post_data["uid"]])
            chat_message["ChatURL"] = f'https://gettr.com/post/{chat_message["UniqueIDNetwork"]}'
            return_list.append(chat_message)

            # 2. add original post to list
            chat_message_original = chat_message.copy()
            chat_message_original["Timestamp"] = post_data["cdate"] / 1000
            chat_message_original["UniqueIDNetwork"] = post_id
            chat_message_original["ChatParentID"] = "-1"
            chat_message_original["SenderUser"] = self.uinf_to_snuserdata(
                self.data["result"]["aux"]["uinf"][post_data["uid"]])
            chat_message_original["ChatURL"] = f'https://gettr.com/post/{chat_message_original["UniqueIDNetwork"]}'

            return_list.append(chat_message_original)

        elif list_item.get("action") == "pub_cm":
            # 1. add comment post to list
            chat_message["Timestamp"] = list_item.get("cdate", 0) / 1000
            if not chat_message["Timestamp"]:
                chat_message["Timestamp"] = list_item.get("activity", {}).get("cdate", 0) / 1000

            chat_message["UniqueIDNetwork"] = post_id
            chat_message["ChatParentID"] = post_data.get("pid")
            if not chat_message["ChatParentID"]:
                chat_message["ChatParentID"] = post_data.get("_id")

            chat_message["SenderUser"] = self.uinf_to_snuserdata(self.data["result"]["aux"]["uinf"][post_data["uid"]])
            chat_message["ChatURL"] = f'https://gettr.com/comment/{chat_message["UniqueIDNetwork"]}'
            return_list.append(chat_message)

            # 2. add original post to list
            try:
                original_post = self.data["result"]["aux"]["post"][post_data["pid"]]
            except KeyError:
                original_post = None

            if original_post:
                chat_message_original = snhwalker_utils.snh_model_manager.CreateDictSNChatmessage()
                if "txt" in original_post:
                    chat_message_original["Text"] = original_post["txt"]
                if "prevsrc" in original_post:
                    chat_message_original["LinkURL"] = original_post["prevsrc"]
                if ('img' in original_post) and (len(original_post["img"]) > 0):
                    chat_message_original["ImageURL"] = "https://media.gettr.com/" + original_post["img"][0]
                if ('previmg' in original_post):
                    chat_message_original["ImageURL"] = "https://media.gettr.com/" + original_post["previmg"]
                if ('ovid' in original_post):
                    chat_message_original["VideoURL"] = "https://media.gettr.com/" + original_post["ovid"]
                chat_message_original["Timestamp"] = original_post["cdate"] / 1000
                chat_message_original["UniqueIDNetwork"] = post_data["pid"]
                chat_message_original["ChatParentID"] = "-1"
                chat_message_original["SenderUser"] = self.uinf_to_snuserdata(
                    self.data["result"]["aux"]["uinf"][original_post["uid"]])
                chat_message_original["ChatURL"] = f'https://gettr.com/post/{chat_message_original["UniqueIDNetwork"]}'

                return_list.append(chat_message_original)

        return return_list