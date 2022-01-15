#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   handler_account.py
@Time    :   2022/01/14 22:42:40
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


class AccountHandling:
    def __init__(self):
        debugConfig["enableDebugLog"] = True
        pass 

    def disable_account(self):
        # Commands to hide the account identity
        pass
        
    def enable_account(self):
        # Commands to show the account identity
        pass
