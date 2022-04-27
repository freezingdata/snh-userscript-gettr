#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   contacts_collector.py
@Time    :   2022/01/14 22:42:18
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
from Gettr.config import modul_config

from snhwalker_utils import snhwalker, snh_major_version
import snhwalker_utils    

class ContactsCollector:
    def __init__(self, input_profile, input_config):
        self.profile = input_profile
        self.config = input_config
        self.contact_type = ''

        self.naming = {
            'FTFriend': 'Followings',
            'FTFollower': 'Follower',   
        }

        self.api = GattrAPI()
        pass
        
    def run(self):
        debugPrint('[START] Python Script: Save contacts')

        if self.config['FTFriend'] == True:
            self.contact_type = 'FTFriend'
            self.__get_contacts()
        if self.config['FTFollower'] == True:    
            self.contact_type = 'FTFollower'
            self.__get_contacts()            
        debugPrint('[Finished] Python Script: Save contacts')

    def __get_contacts(self):
        debugPrint(f'[Contacts] Save {self.contact_type}')
        if self.contact_type == 'FTFollower':
            snhwalker.DropStatusMessage(f'Collect Follower')
            url = GetURL_Followers(self.profile["UserID"])    
            api_function = self.api.get_follower
        if self.contact_type == 'FTFriend':
            snhwalker.DropStatusMessage(f'Collect Following')
            url = GetURL_Following(self.profile["UserID"])     
            api_function = self.api.get_followings           
        self.api.load_page(url)   

        offset = 0
        contact_count = 0
        while True:
            debugPrint(f'[Contacts] Request contact data (offset={offset})')
            gettr_data = api_function(self.profile["UserID"], offset, 20)
            debugWrite(f'Gettr_{self.contact_type}_response_{str(time.time())}.data',gettr_data )
            object_handler = GettrDataObject(gettr_data)
            has_next_page = not (object_handler.get_rslst_cursor() == 0)
            userlist = object_handler.as_userlist()   
            for item in userlist:
                contact_count += 1
                snhwalker.DropStatusMessage(f'Collecting {contact_count} {self.naming[self.contact_type]}')
                debugPrint(f'[Contacts] Handling contact  {contact_count} {self.naming[self.contact_type]} -> {item}')
                self.__send_to_snh(item)
            
            offset += 20
            if has_next_page is False:
                break

            if (self.contact_type == 'FTFollower') and (modul_config["limit_follower"] is True) and (contact_count > modul_config["limit_follower_count"]):
                break
            if (self.contact_type == 'FTFriend') and (modul_config["limit_following"] is True) and (contact_count > modul_config["limit_following_count"]):
                break            
            
            snhwalker_utils.snh_browser.WaitMS(1000)
        

    def __send_to_snh(self, SNUserData):        
        SNHFriendItem = snhwalker_utils.snh_model_manager.CreateDictSNFriendshipdata()
        SNHFriendItem['User'] = SNUserData
        SNHFriendItem['FriendshipType'] = self.contact_type  
        snhwalker.PromoteSNFriendshipdata(SNHFriendItem)              

    