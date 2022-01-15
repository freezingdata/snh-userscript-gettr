#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   debug.py
@Time    :   2022/01/14 22:44:02
@Author  :   Benno Krause 
@Contact :   bk@freezingdata.de
@License :   (C)Copyright 2020-2021, Freezingdata GmbH
@Desc    :   None
'''

import os

# TODO: Switch to debugging class

debugConfig = {
    "enableDebugFileOutput"       : False,
    "enableDebugLog"              : False,
    "debugFolderLocation"         : "c:\\SNH-Temp\\Gettr\\",
    "debugLevelThreshold"         : 0  
}

def initDebug(task_item):
    global debugConfig
    if "Debug" in task_item:
        debugConfig = task_item["Debug"]

def debugPrint(*text):
    if debugConfig["enableDebugLog"] is True:
        data = tuple(str(x) for x in text)
        print(" | ".join(data))
        if debugConfig["enableDebugFileOutput"] is True:
            if not os.path.exists(debugConfig["debugFolderLocation"]):
                os.makedirs(debugConfig["debugFolderLocation"])
            debugFile = open(debugConfig["debugFolderLocation"] + "gettr.log", 'a', encoding="utf-8")
            debugFile.write(" | ".join(data) + "\n")
            debugFile.close()

def debugWrite(filepath, content):
    if debugConfig["enableDebugFileOutput"] is True:
        if not os.path.exists(debugConfig["debugFolderLocation"]):
            os.makedirs(debugConfig["debugFolderLocation"])
        contentfile = open(debugConfig["debugFolderLocation"] + filepath, 'w', encoding="utf-8")
        contentfile.write(content)
        contentfile.write("\n")
        contentfile.close()
        debugPrint("Write Debug File in " + debugConfig["debugFolderLocation"] + filepath)

