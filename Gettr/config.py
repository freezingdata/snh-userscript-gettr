#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   config.py
@Time    :   2022/04/09
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2022, Freezingdata GmbH
@Desc    :   None
'''

modul_config = {
    # limit_follower
    # Type: boolean
    # If its set to True, the count of follower will be limited
    # to the limit_follower_count value
    "limit_follower": True,


    # limit_follower_count
    # Type: integer
    # Max count of follower, which can be collected,
    "limit_follower_count": 1000,


    # limit_following
    # Type: boolean
    # If its set to True, the count of following will be limited
    # to the limit_following_count value
    "limit_following": True,


    # limit_following_count
    # Type: integer
    # Max count of followings, which can be collected,
    "limit_following_count": 1000,    

}