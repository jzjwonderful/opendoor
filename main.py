#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-02-07 14:29
# @Author  : Jared Kin
# @File    : main.py
# @Software: PyCharm
import requests
import json
import sys
import platform
import time
session_path = 'session'


Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
}
proxies = {'https': 'http://localhost:8888','http':'http://localhost:8888'}


def getSessionId(text):
    try:
        js = json.loads(text)
        if js["code"] == 0:
            return js["data"]["sessionId"]
        else:
            writelog("get session fail:" + js["message"])
    except Exception as e:
        writelog(e)
        return None


def refresh(sessionId):
    try:
        URL = "https://mobileapi.qinlinkeji.com/api/wxmini/v3/appuser/refresh"
        url = URL + "?sessionId=" + sessionId
        writelog("request refresh url:" + url)
        req = requests.post(url=url, headers=Headers, data=None)
        return getSessionId(req.text)
    except Exception as e:
        writelog("refresh session fail:")
        writelog(e)
        return None


def open_session(sessionId):
    try:
        URL = "https://mobileapi.qinlinkeji.com/api/open/doorcontrol/v2/open"
        url = URL + "?sessionId=" + sessionId
        writelog("request open url:" + url)
        req = requests.post(url=url, headers=Headers, data=None)
        return getSessionId(req.text)
    except Exception as e:
        writelog("faild to open door:")
        writelog(e)
        return None

def readSessionId():
    ss = ""
    with open(session_path,"r+",) as f :
        ss =  str(f.read())
    writelog("read session:" + ss)
    return ss

def writeSessionId(session):
    writelog("write session:" + session)
    with open(session_path,"w+") as f :
        return f.write(session)

def writelog(log):
    line = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + ":" +log
    with open("/tmp/log","a+") as w:
        w.write(line + "\n")
    print line

if __name__ == '__main__':
    session = readSessionId()
    session = refresh(session)

    if session is None:
        writelog("session is none")
    else:
        writeSessionId(session)

    writelog("finished refresh")
