#!/bin/python
# coding=utf-8
from os import path, system, getcwd, remove, makedirs, walk
from datetime import timedelta
from datetime import datetime
from shutil import rmtree
from json import load
from ftplib import FTP
from glob import glob


def mkpathandreadjson(path):
    nowtime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    makedirs(nowtime)
    if len(path) < 4:
        data = load(open(path + "easycopy.json"))
        x_c = path + "xcopy"
        path += nowtime
        return x_c, data, path
    else:
        path += "\\"
        data = load(open(path + "easycopy.json"))
        x_c = path + "xcopy"
        path += nowtime
        return x_c, data, path


def geteveryday(begin_date, end_date):
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if (begin_date > end_date):
        begin_date, end_date = end_date, begin_date
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


def slicedate(date_list):
    l0, l1, l2 = [[] for i in range(3)]
    for date in date_list:
        l0.append(date)
        l1.append(date.replace("-", "_"))
    for date in l1:
        if (date[5] == "0"):
            l2.append(date[-4:])
        else:
            l2.append(date[-5:])
    return l0, l1, l2


def getstationame():
    stationame = glob("E:\\jd1awxj\\" + "*w*.rar")[0][11:14]
    return stationame


def copy(l0, l1, l2):
    for s0, s1, s2 in zip(l0, l1, l2):
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\replays\replay" + s2 + ".*",
                nowdir + r"\JD1AWXJ\replays\replay" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\alarms\alm" + s2 + ".*",
                nowdir + r"\JD1AWXJ\alarms\alm" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\button\btn" + s2 + ".*",
                nowdir + r"\JD1AWXJ\button\btn" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\errors\err" + s2 + ".*",
                nowdir + r"\JD1AWXJ\errors\err" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\doginfo\info" + s1 + ".*",
                nowdir + r"\JD1AWXJ\doginfo\info" + s1 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\JD1AWXJ\sysinfo\sys" + s1 + ".*",
                nowdir + r"\JD1AWXJ\sysinfo\sys" + s1 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\MYLOGSERVER\Data\*" + s0 + ".*",
                nowdir + r"\MYLOGSERVER\Data\*" + s0 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, r"E:\MYLOGSERVER\Log\*" + s0 + ".*",
                nowdir + r"\MYLOGSERVER\Log\*" + s0 + ".*"))
    system("%s /d /y %s %s" %
           (x_c, r"E:\JD1AWXJ\*.RAR", nowdir + r"\JD1AWXJ\*.RAR"))
    system(
        "%s /d /y %s %s" %
        (x_c, r"E:\MYLOGSERVER\*LOG*.RAR", nowdir + r"\MYLOGSERVER\*LOG*.RAR"))

    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + r"\JD1AWXJ\*W*.RAR", nowdir + r"\JD1AWXJ"))
    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + r"\MYLOGSERVER\*LOG0*.RAR", nowdir + r"\MYLOGSERVER"))
    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + r"\MYLOGSERVER\MYLOG*_*.RAR", nowdir + r"\MYLOGSERVER"))


def popdict(dict, popkey):
    for k in popkey:
        dict.pop(k)


def copybyftp(l0, l1, l2, args):
    for ip in args:
        everyip(args[ip], l0, l1, l2)


def searchsoft(list):
    templist = []
    for ele in list:
        if ele.endswith(".RAR") or ele.endswith(".rar"):
            templist.append(ele)
    return templist


def downlist(ftp, l0, l1):
    for ele0, ele1 in zip(l0, l1):
        print(ele0)
        if (download(ftp, ele0, ele1)):
            remove(ele0)


def everyip(ip, l0, l1, l2):
    print(ip)
    ftp = FTP()
    ftp.connect(ip, 21)
    # ftp.login("Remote","jd1awxj")
    ftp.login("Anonymous", "jd1awxj")
    ftp.cwd("jd1awxj")
    for ele in searchsoft(ftp.nlst()):
        if "MW" in ele or "WX" in ele:
            wxjsoftname = ele
    ftpstationame = wxjsoftname[0:3]
    newfile(ftpstationame)
    ftp.cwd("..")
    ftp.cwd("mylogserver")
    for ele in searchsoft(ftp.nlst()):
        if "LOG" in ele:
            logsoftname = ele
    ftp.cwd("..")
    q0 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ" + "\\" + wxjsoftname
    q1 = 'RETR ' + r"JD1AWXJ" + "\\" + wxjsoftname
    q2 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER" + "\\" + logsoftname
    q3 = 'RETR ' + r"MYLOGSERVER" + "\\" + logsoftname
    downlist(ftp, [q0, q2], [q1, q3])
    for s0, s1, s2 in zip(l0, l1, l2):

        r0 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\replays\replay" + s2 + ".rar"
        r1 = 'RETR ' + r"JD1AWXJ\replays\replay" + s2 + ".rar"

        r2 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\replays\replay" + s2 + ".rep"
        r3 = 'RETR ' + r"JD1AWXJ\replays\replay" + s2 + ".rep"

        r4 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\doginfo\info" + s1 + ".txt"
        r5 = 'RETR ' + r"JD1AWXJ\doginfo\info" + s1 + ".txt"

        r6 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\sysinfo\sys" + s1 + ".txt"
        r7 = 'RETR ' + r"JD1AWXJ\sysinfo\sys" + s1 + ".txt"

        r8 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\alarms\alm" + s2
        r9 = 'RETR ' + r"JD1AWXJ\alarms\alm" + s2

        r10 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\button\btn" + s2
        r11 = 'RETR ' + r"JD1AWXJ\button\btn" + s2

        r12 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ\errors\err" + s2
        r13 = 'RETR ' + r"JD1AWXJ\errors\err" + s2

        r14 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Data" + "\\" + ftpstationame + "_I_A" + " " + s0 + ".rar"
        r15 = 'RETR ' + r"MYLOGSERVER\Data" + "\\" + ftpstationame + "_I_A" + " " + s0 + ".rar"

        r16 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Data" + "\\" + ftpstationame + "_II_A" + " " + s0 + ".rar"
        r17 = 'RETR ' + r"MYLOGSERVER\Data" + "\\" + ftpstationame + "_II_A" + " " + s0 + ".rar"

        r18 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Data" + "\\" + ftpstationame + "_I_B" + " " + s0 + ".rar"
        r19 = 'RETR ' + r"MYLOGSERVER\Data" + "\\" + ftpstationame + "_I_B" + " " + s0 + ".rar"

        r20 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Data" + "\\" + ftpstationame + "_II_B" + " " + s0 + ".rar"
        r21 = 'RETR ' + r"MYLOGSERVER\Data" + "\\" + ftpstationame + "_II_B" + " " + s0 + ".rar"

        r22 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "_I_A" + " " + s0 + ".rar"
        r23 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "_I_A" + " " + s0 + ".rar"

        r24 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "_II_A" + " " + s0 + ".rar"
        r25 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "_II_A" + " " + s0 + ".rar"

        r26 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "_I_B" + " " + s0 + ".rar"
        r27 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "_I_B" + " " + s0 + ".rar"

        r28 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "_II_B" + " " + s0 + ".rar"
        r29 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "_II_B" + " " + s0 + ".rar"

        r30 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_I_A" + " " + s0 + ".rar"
        r31 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_I_A" + " " + s0 + ".rar"

        r32 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_II_A" + " " + s0 + ".rar"
        r33 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_II_A" + " " + s0 + ".rar"

        r34 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_I_B" + " " + s0 + ".rar"
        r35 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_I_B" + " " + s0 + ".rar"

        r36 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_II_B" + " " + s0 + ".rar"
        r37 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + ftpstationame + "MW" + "_II_B" + " " + s0 + ".rar"

        r38 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\Log" + "\\" + "MyLogServer1" + " " + s0 + ".rar"
        r39 = 'RETR ' + r"MYLOGSERVER\Log" + "\\" + "MyLogServer1" + " " + s0 + ".rar"

        list0 = [
            r0, r2, r4, r6, r8, r10, r12, r14, r16, r18, r20, r22, r24, r26,
            r28, r30, r32, r34, r36, r38
        ]
        list1 = [
            r1, r3, r5, r7, r9, r11, r13, r15, r17, r19, r21, r23, r25, r27,
            r29, r31, r33, r35, r37, r39
        ]
        downlist(ftp, list0, list1)
    ftp.quit()
    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + r"\JD1AWXJ\*W*.RAR",
            nowdir + "\\" + ftpstationame + r"\JD1AWXJ"))
    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\*LOG0*.RAR",
            nowdir + "\\" + ftpstationame + r"\MYLOGSERVER"))
    system("start winrar x -y -r -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + r"\MYLOGSERVER\MYLOG*_*.RAR",
            nowdir + "\\" + ftpstationame + r"\MYLOGSERVER"))


def download(ftp, local_file, remote_file):
    try:
        buf_size = 1024
        fp = open(local_file, 'wb')
        ftp.retrbinary(remote_file, fp.write, buf_size)
        fp.close()
        print("success")
        return 0
    except Exception as err:
        print("no such data")
        return 1


def newfile(path):
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\replays")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\doginfo")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\sysinfo")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\alarms")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\button")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\errors")
    makedirs(nowdir + "\\" + path + r"\mylogserver" + r"\Data")
    makedirs(nowdir + "\\" + path + r"\mylogserver" + r"\Log")


nowdir = getcwd()
x_c, jsondata, nowdir = mkpathandreadjson(nowdir)
date_list = geteveryday(jsondata["starttime"], jsondata["endtime"])
l0, l1, l2 = slicedate(date_list)

if jsondata["remote"] is "0":
    stationame = getstationame()
    nowdir = nowdir + "\\" + stationame
    copy(l0, l1, l2)
    print("All right, all the data has been copied to %s " % (nowdir[0:-4]))
    print("All right, all the data has been copied to %s " % (nowdir[0:-4]))
    print("All right, all the data has been copied to %s " % (nowdir[0:-4]))
elif jsondata["remote"] is "1":
    popdict(jsondata, ["starttime", "endtime", "remote"])
    copybyftp(l0, l1, l2, jsondata)
    print("All right, all the data has been copied to %s " % (nowdir))
    print("All right, all the data has been copied to %s " % (nowdir))
    print("All right, all the data has been copied to %s " % (nowdir))
else:
    print("Something Wrong")
    exit()
system("pause")
