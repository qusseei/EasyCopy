#!/bin/python
# coding=utf-8
from os import system, getcwd, makedirs
from datetime import datetime, timedelta
from json import load
from ftplib import FTP
from glob import glob
from itertools import zip_longest


#读取配置文件并新建保存目录
def mkpathandreadjson(path):
    nowtime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    makedirs(nowtime)
    if len(path) < 4:
        try:
            data = load(open(path + "easycopy.json"))
        except Exception as err:
            print(err)
            system("pause")
            exit()
        x_c = path + "xcopy"
        path += nowtime
        return x_c, data, path
    else:
        path += "\\"
        try:
            data = load(open(path + "easycopy.json"))
        except Exception as err:
            print(err)
            system("pause")
            exit()
        x_c = path + "xcopy"
        path += nowtime
        return x_c, data, path


#构造日期列表l0,l1,l2
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


#得到本地站名
def getstationame():
    stationame = glob("E:\\jd1awxj\\" + "*w*.rar")[0][11:14]
    return stationame


#拷贝本地日志
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
    #解压软件到指定目录
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + r"\JD1AWXJ\*W*.RAR", nowdir + r"\JD1AWXJ"))
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + r"\MYLOGSERVER\*LOG*.RAR", nowdir + r"\MYLOGSERVER"))


#删除多余配置项，留下IP地址字典
def popdict(dict, popkey):
    for k in popkey:
        dict.pop(k)


#遍历IP拷贝数据
def copybyftp(l0, l1, l2, args):
    for ip in args:
        everyip(args[ip], l0, l1, l2)


#建立FTP连接，对比日期列表拷贝日志
def everyip(ip, l0, l1, l2):
    print(ip)
    ftp = FTP()
    ftp.connect(ip, 21)
    # ftp.login("Remote","jd1awxj")
    ftp.login("Anonymous", "jd1awxj")
    wxjnlst = ftp.nlst("jd1awxj")
    mylognlst = ftp.nlst("mylogserver")
    alarmsnlst = ftp.nlst("jd1awxj/alarms")
    buttonnlst = ftp.nlst("jd1awxj/button")
    doginfonlst = ftp.nlst("jd1awxj/doginfo")
    errorsnlst = ftp.nlst("jd1awxj/errors")
    replayslst = ftp.nlst("jd1awxj/replays")
    sysinfolst = ftp.nlst("jd1awxj/sysinfo")
    Datanlst = ftp.nlst("mylogserver/Data")
    Loglst = ftp.nlst("mylogserver/Log")

    for ele in searchname(wxjnlst):
        if "MW" in ele or "WX" in ele:
            wxjsoftname = ele

    ftpstationame = wxjsoftname[0:3] + "_" + ip
    newfile(ftpstationame)

    for ele in searchname(mylognlst):
        if "LOG" in ele:
            logsoftname = ele

    q0 = nowdir + "\\" + ftpstationame + r"\JD1AWXJ" + "\\" + wxjsoftname
    q1 = 'RETR ' + r"JD1AWXJ" + "\\" + wxjsoftname
    q2 = nowdir + "\\" + ftpstationame + r"\MYLOGSERVER" + "\\" + logsoftname
    q3 = 'RETR ' + r"MYLOGSERVER" + "\\" + logsoftname
    download(ftp, q0, q1)
    download(ftp, q2, q3)

    for Data, Log, doginfo, sysinfo, alarms, button, errors, replays in zip_longest(
            Datanlst, Loglst, doginfonlst, sysinfolst, alarmsnlst, buttonnlst,
            errorsnlst, replayslst):
        for s0, s1, s2 in zip(l0, l1, l2):
            if Data:
                if s0 in Data:
                    wxjdownload(ftp, Data, "Data", ftpstationame)
            if Log:
                if s0 in Log:
                    wxjdownload(ftp, Log, "Log", ftpstationame)
            if doginfo:
                if s1 in doginfo:
                    wxjdownload(ftp, doginfo, "doginfo", ftpstationame)
            if sysinfo:
                if s1 in sysinfo:
                    wxjdownload(ftp, sysinfo, "sysinfo", ftpstationame)
            if alarms:
                if s2 in alarms:
                    wxjdownload(ftp, alarms, "alarms", ftpstationame)
            if button:
                if s2 in button:
                    wxjdownload(ftp, button, "button", ftpstationame)
            if errors:
                if s2 in errors:
                    wxjdownload(ftp, errors, "errors", ftpstationame)
            if replays:
                if s2 in replays:
                    wxjdownload(ftp, replays, "replays", ftpstationame)

    ftp.quit()
    #解压指定文件
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + "\JD1AWXJ\*W*.RAR",
            nowdir + "\\" + ftpstationame + "\JD1AWXJ"))
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + "\MYLOGSERVER\*LOG*.RAR",
            nowdir + "\\" + ftpstationame + "\MYLOGSERVER"))


#远程获取站名
def searchname(list):
    templist = []
    for ele in list:
        if ele.endswith(".RAR") or ele.endswith(".rar"):
            templist.append(ele)
    return templist


#指定维修机和日志下载到不同地址
def wxjdownload(ftp, file, type, stationame):
    if type in ("Data", "Log"):
        ra = "%s%s%s%s%s%s%s" % (nowdir, "\\", stationame, "\MYLOGSERVER\\",
                                 type, "\\", file)
        rb = "%s%s%s%s%s" % ('RETR', "MYLOGSERVER\\", type, "\\", file)
        download(ftp, ra, rb)
    elif type in ("doginfo", "sysinfo", "alarms", "button", "replays",
                  "errors"):
        ra = "%s%s%s%s%s%s%s" % (nowdir, "\\", stationame, "\JD1AWXJ\\", type,
                                 "\\", file)
        rb = "%s%s%s%s%s" % ('RETR', "JD1AWXJ\\", type, "\\", file)
        download(ftp, ra, rb)


#下载数据及异常处理
def download(ftp, local_file, remote_file):
    try:
        buf_size = 1024
        fp = open(local_file, 'wb')
        ftp.retrbinary(remote_file, fp.write, buf_size)
        fp.close()
        print("success copy %s " % (remote_file[4:]))
        return 1
    except Exception as err:
        print(err)
        print("failed copy %s " % (remote_file))
        return 0


#新建指定空文件夹
def newfile(path):
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\replays")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\doginfo")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\sysinfo")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\alarms")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\button")
    makedirs(nowdir + "\\" + path + r"\jd1awxj" + r"\errors")
    makedirs(nowdir + "\\" + path + r"\mylogserver" + r"\Data")
    makedirs(nowdir + "\\" + path + r"\mylogserver" + r"\Log")


#获取当前路径
nowdir = getcwd()
#读取配置文件并新建保存目录
x_c, jsondata, nowdir = mkpathandreadjson(nowdir)
#构造日期列表l0,l1,l2
l0, l1, l2 = geteveryday(jsondata["starttime"], jsondata["endtime"])
#本地拷贝日志
if jsondata["remote"] is "0":
    stationame = getstationame()
    nowdir = nowdir + "\\" + stationame
    copy(l0, l1, l2)
    print("All data has been copied to %s " % (nowdir))
    print("All data has been copied to %s " % (nowdir))
    print("All data has been copied to %s " % (nowdir))
#远程拷贝日志
elif jsondata["remote"] is "1":
    popdict(jsondata, ["starttime", "endtime", "remote"])
    copybyftp(l0, l1, l2, jsondata)
    print("All data has been copied to %s " % (nowdir))
    print("All data has been copied to %s " % (nowdir))
    print("All data has been copied to %s " % (nowdir))
#异常
else:
    print("Something Wrong")
#暂停
system("pause")