#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   profile_collector.py
@Time    :   2022/01/14 22:42:29
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

class ProfileCollector:
    def __init__(self):
        self.api = GattrAPI()
        pass

    def handle_current_profile(self):
        pass

    def handle_current_group(self):
        pass    

    def current_is_user(self):
        return True

    def current_is_page(self):
        return False

    def current_is_group(self):
        return False        

    def save_profile(self, profileUrl):
        debugPrint('[START] Python Script: Save profile')
        user_id = getRegex(profileUrl, 'https://www.gettr.com/user/(.*)', 1)
        self.api.load_page(profileUrl)
        gettr_data_unif = self.api.get_unif(user_id)

        object_handler = GettrDataObject(gettr_data_unif)
        snhwalker.PromoteSNUserdata(object_handler.as_SNUserData())
        #debugPrint(f'Profile: gettr_data_unif {gettr_data_unif}')


        debugPrint('[Finished] Python Script: Save profile')
        
    def save_profile_details(self, profile):
        debugPrint('[START] Python Script: SaveProfileDetails')
        debugPrint('[Finished] Python Script: SaveProfileDetails')