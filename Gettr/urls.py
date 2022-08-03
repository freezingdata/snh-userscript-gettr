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
from Gettr.debug import debugPrint


def GetURL_Timeline(UserID, UserIDNumber=''):
    return f'https://gettr.com/user/{UserID}'


def GetURL_Profile(UserID, UserIDNumber=''):
    return f'https://gettr.com/user/{UserID}'


def GetURL_Friends(UserID, UserIDNumber=''):
    return f'https://gettr.com/user/{UserID}/following'


def GetURL_Following(UserID, UserIDNumber=''):
    return f'https://gettr.com/user/{UserID}/following'


def GetURL_Followers(UserID, UserIDNumber=''):
    return f'https://gettr.com/user/{UserID}/followers'


def GetURL_Fotos(UserID, UserIDNumber=''):
    return f'http://url.com/fotos/{UserID}'  # Dummy


def GetURL_Group(UserID, UserIDNumber=''):
    return f'http://url.com/group/{UserID}'  # Dummy


def GetURL_OwnProfile(UserID, UserIDNumber=''):
    return f'http://url.com/self'  # Dummy


GETTR_POST_PAGE: str = "GETTR_POST_PAGE"
GETTR_PROFILE_PAGE: str = "GETTR_PROFILE_PAGE"
GETTR_COMMENT_PAGE: str = "GETTR_COMMENT_PAGE"

GETTR_PAGE_TYPES: list = [
    GETTR_POST_PAGE,
    GETTR_PROFILE_PAGE,
    ]


class GettrUrlResolver:
    def __init__(self, url: str):
        self.url: str = url
        self.page_type: str = ""
        self.resolve_url()

    def resolve_url(self) -> None:
        debugPrint(f"[INFO]: Start solve url. Url: {self.url}")
        split_url: list = self.url.split("/")
        if split_url[3] == "user":
            self.set_page_type(GETTR_PROFILE_PAGE)
        if split_url[3] == "post":
            self.set_page_type(GETTR_POST_PAGE)
        if split_url[3] == "comment":
            self.set_page_type(GETTR_COMMENT_PAGE)
        debugPrint(f"[INFO]: End solve url. Current url type: {self.get_page_type()}")

    def get_page_type(self):
        return self.page_type

    def set_page_type(self, page_type):
        self.page_type = page_type
