#!/bin/python
# coding=utf-8
from os import path, system, getcwd
from glob import glob
from datetime import timedelta
from datetime import datetime
from shutil import rmtree

nowdir = getcwd()

if len(nowdir) < 4:
    ss = glob(nowdir + "2*.exe")
    if path.exists(nowdir + "jd1awxj"):
        rmtree(nowdir + "jd1awxj")
    if path.exists(nowdir + "mylogserver"):
        rmtree(nowdir + "mylogserver")
else:
    nowdir += r"\\"
    ss = glob(nowdir + "*.exe")
    if path.exists(nowdir + "jd1awxj"):
        rmtree(nowdir + "jd1awxj")
    if path.exists(nowdir + "mylogserver"):
        rmtree(nowdir + "mylogserver")

x_c = nowdir + "xcopy"

system("%s /d /y %s %s" %
       (x_c, r"E:\JD1AWXJ\*.RAR", nowdir + r"JD1AWXJ\*.RAR"))
system("%s /d /y %s %s" %
       (x_c, r"E:\MYLOGSERVER\*LOG*.RAR", nowdir + r"MYLOGSERVER\*LOG*.RAR"))


def copy(s0, s1, s2):
    global nowdir
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\replays\replay" + s2 + ".*",
            nowdir + r"JD1AWXJ\replays\replay" + s2 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\alarms\alm" + s2 + ".*",
            nowdir + r"JD1AWXJ\alarms\alm" + s2 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\button\btn" + s2 + ".*",
            nowdir + r"JD1AWXJ\button\btn" + s2 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\errors\err" + s2 + ".*",
            nowdir + r"JD1AWXJ\errors\err" + s2 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\doginfo\info" + s1 + ".*",
            nowdir + r"JD1AWXJ\doginfo\info" + s1 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\sysinfo\sys" + s1 + ".*",
            nowdir + r"JD1AWXJ\sysinfo\sys" + s1 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\MYLOGSERVER\Data\*" + s0 + ".*",
            nowdir + r"MYLOGSERVER\Data\*" + s0 + ".*"))
    system("%s /s /e /d /y %s %s" %
           (x_c, r"E:\MYLOGSERVER\Log\*" + s0 + ".*",
            nowdir + r"MYLOGSERVER\Log\*" + s0 + ".*"))


def slicedate(date):
    s0 = date
    s1 = date.replace("-", "_")
    if (s1[5] == "0"):
        s2 = s1[-4:]
    else:
        s2 = s1[-5:]
    copy(s0, s1, s2)


def geteveryday(begin_date, end_date):
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if (begin_date > end_date):
        begin_date, end_date = end_date, begin_date
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        slicedate(date_str)
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    print("Copy Success!")


geteveryday(ss[0][-14:-4], ss[0][-25:-15])
system("start winrar x -y -ikbc -inul %s %s" %
       (nowdir + r"JD1AWXJ\*MW*.RAR", nowdir + r"JD1AWXJ"))
system("start winrar x -y -ikbc -inul %s %s" %
       (nowdir + r"MYLOGSERVER\*LOG*.RAR", nowdir + r"MYLOGSERVER"))
system("pause")
