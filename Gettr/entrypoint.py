#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   entrypoint.py
@Time    :   2022/01/14 22:43:38
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2021, Freezingdata GmbH
@Desc    :   None
'''


# Updated to new structure on 2021-09-21 10:11:56
import snhwalker_utils
from snhwalker_utils import snhwalker


from Gettr.module_tools import *
from Gettr.urls import *
from Gettr.debug import *
from Gettr.profile_collector import ProfileCollector
from Gettr.contacts_collector import ContactsCollector
from Gettr.handler_account import AccountHandling
from Gettr.media_collector import MediaCollector
from Gettr.posting_collector import PostingCollector



def snh_GetUrl(profile, urlType):
    print('snh_GetUrl: ' + urlType)
    if urlType == "OwnProfile":
        result = GetURL_OwnProfile(profile["UserID"], profile["UserIDNumber"])
    elif urlType == "Timeline":
        result = GetURL_Timeline(profile["UserID"], profile["UserIDNumber"])
    elif urlType == "Profile":
        result = GetURL_Profile(profile["UserID"], profile["UserIDNumber"])
    elif urlType == "Friends":
        result = GetURL_Friends(profile["UserID"], profile["UserIDNumber"])
    elif urlType == "Group":
        result = GetURL_Group(profile["UserID"], profile["UserIDNumber"])
    return result

def snh_Save(taskItem):
    print('[START] snh_Save ' + taskItem["TargetType"])
    initDebug(taskItem) 
    debugConfig["enableDebugFileOutput"] = True   
    if taskItem["TargetType"] == "Profile":
        ProfileCollector().save_profile(taskItem["TargetURL"])
    elif taskItem["TargetType"] == "Timeline":
        PostingCollector(taskItem["Targetprofile"], taskItem["Config"]).run()
    elif taskItem["TargetType"] == "ProfileDetails":
        ProfileCollector().save_profile_details(taskItem["Targetprofile"])
    elif taskItem["TargetType"] == "Media":
        MediaCollector(taskItem["Targetprofile"], taskItem["Config"]).run()        
    elif taskItem["TargetType"] == "Friends":
        ContactsCollector(taskItem["Targetprofile"], taskItem["Config"]).run()


def GetScreenshotSizes():
    return  {'areaPositionX': 0,
              'areaPositionY': 0,
              'areaSizeX': 1050}
 
def getPluginInfo():
    pluginInfo = {}
    pluginInfo['name'] = 'SNH user script - Gettr '
    pluginInfo['url'] = 'https://gettr.com/'
    pluginInfo['copyright'] = 'Freezingdata GmbH'
    pluginInfo['functions'] = {}
    pluginInfo['functions']['profile'] = True
    pluginInfo['functions']['groups'] = False
    pluginInfo['functions']['details'] = True
    pluginInfo['functions']['stories'] = False
    pluginInfo['functions']['videos'] = True
    pluginInfo['functions']['friends'] = True
    pluginInfo['functions']['follower'] = True
    pluginInfo['functions']['timeline'] = True
    pluginInfo['functions']['timelinereactions'] = False
    pluginInfo['functions']['timelinecomments'] = True
    pluginInfo['functions']['media'] = False
    pluginInfo['functions']['mediareactions'] = False
    pluginInfo['functions']['mediacomments'] = False
    return pluginInfo

def DisableUseraccountData():
    AccountHandling().disable_account()
       
def EnableUseraccountData():
    AccountHandling().enable_account()

def GetProfileStatus():
    # Not used in Userscripts
    return True

def GetLoginStatus():
    # Not used in Userscripts
    return True

def doLogin(userid, password):
    # Not used in Userscripts
    return True

def CurrentWebPageIsUser():
    return ProfileCollector().current_is_user()

def CurrentWebPageIsPage():
    return ProfileCollector().current_is_page()

def CurrentWebPageIsGroup():
    return ProfileCollector().current_is_group()

def HandleProfile():
    ProfileCollector().handle_current_profile()

def HandleGroupsPage():
    ProfileCollector().handle_current_group()
    pass



