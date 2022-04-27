#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   urls.py
@Time    :   2022/01/14 22:42:11
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2021, Freezingdata GmbH
@Desc    :   None
'''


def GetURL_Timeline(UserID, UserIDNumber = ''):
    return f'https://gettr.com/user/{UserID}'

def GetURL_Profile(UserID, UserIDNumber = ''):
    return f'https://gettr.com/user/{UserID}'

def GetURL_Friends(UserID, UserIDNumber = ''):
    return f'https://gettr.com/user/{UserID}/following'

def GetURL_Following(UserID, UserIDNumber = ''):
    return f'https://gettr.com/user/{UserID}/following'

def GetURL_Followers(UserID, UserIDNumber = ''):
    return f'https://gettr.com/user/{UserID}/followers'        

def GetURL_Fotos(UserID, UserIDNumber = ''):
    return f'http://url.com/fotos/{UserID}' #Dummy

def GetURL_Group(UserID, UserIDNumber = ''):
    return f'http://url.com/group/{UserID}' #Dummy

def GetURL_OwnProfile(UserID, UserIDNumber = ''):
    return f'http://url.com/self' #Dummy