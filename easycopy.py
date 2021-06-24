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
    try:
        makedirs(nowtime)
    except Exception as err:
        print(err)
        system("pause")
        exit()
    if len(path) < 4:
        try:
            data = load(open(path + "easycopy.json"))
        except Exception as err:
            print(err)
            print("CAN NOT FIND EASYCOPY.JSON")
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
            print("CAN NOT FIND EASYCOPY.JSON")
            system("pause")
            exit()
        x_c = path + "xcopy"
        path += nowtime
        return x_c, data, path


#构造日期列表l0,l1,l2
def geteveryday(begindate, enddate):
    datelist = []
    begindate = datetime.strptime(begindate, "%Y-%m-%d")
    enddate = datetime.strptime(enddate, "%Y-%m-%d")
    if (begindate > enddate):
        begindate, enddate = enddate, begindate
    while begindate <= enddate:
        date_str = begindate.strftime("%Y-%m-%d")
        datelist.append(date_str)
        begindate += timedelta(days=1)
        l1, l2 = [[] for i in range(2)]
    for date in datelist:
        l1.append(date.replace("-", "_"))
    for date in l1:
        if (date[5] == "0"):
            if (date[8] == "0"):
                l2.append(date[-4:-2] + date[-1:])
            else:
                l2.append(date[-4:])
        else:
            if (date[8] == "0"):
                l2.append(date[-5:-2] + date[-1:])
            else:
                l2.append(date[-5:])
    return datelist, l1, l2


#得到本地站名
def getstationame():
    try:
        stationame = glob("E:\\jd1awxj\\" + "*w*.rar")[0][11:14]
    except Exception as err:
        print(err)
        print("CAN NOT FIND JA1AWXJ")
        system("pause")
        exit()
    return stationame


#拷贝本地日志
def copy(l0, l1, l2):
    for s0, s1, s2 in zip(l0, l1, l2):
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\replays\\replay" + s2 + ".*",
                nowdir + "\\JD1AWXJ\\replays\\replay" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\alarms\\alm" + s2 + ".*",
                nowdir + "\\JD1AWXJ\\alarms\\alm" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\button\\btn" + s2 + ".*",
                nowdir + "\\JD1AWXJ\\button\\btn" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\errors\\err" + s2 + ".*",
                nowdir + "\\JD1AWXJ\\errors\\err" + s2 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\doginfo\\info" + s1 + ".*",
                nowdir + "\\JD1AWXJ\\doginfo\\info" + s1 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\JD1AWXJ\\sysinfo\\sys" + s1 + ".*",
                nowdir + "\\JD1AWXJ\\sysinfo\\sys" + s1 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\MYLOGSERVER\\Data\\*" + s0 + ".*",
                nowdir + "\\MYLOGSERVER\\Data\\*" + s0 + ".*"))
        system("%s /s /e /d /y %s %s" %
               (x_c, "E:\\MYLOGSERVER\Log\\*" + s0 + ".*",
                nowdir + "\\MYLOGSERVER\Log\\*" + s0 + ".*"))
    system("%s /d /y %s %s" %
           (x_c, "E:\\JD1AWXJ\\*W*.RAR", nowdir + "\\JD1AWXJ\\*W*.RAR"))
    system("%s /d /y %s %s" % (x_c, "E:\\MYLOGSERVER\\*LOG*.RAR",
                               nowdir + "\\MYLOGSERVER\\*LOG*.RAR"))
    #解压软件到指定目录
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + "\\JD1AWXJ\\*W*.RAR", nowdir + "\\JD1AWXJ"))
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + "\\MYLOGSERVER\\*LOG*.RAR", nowdir + "\\MYLOGSERVER"))


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
    try:
        ftp = FTP()
        ftp.connect(ip, 21)
        # ftp.login("Remote","jd1awxj")
        ftp.login("Anonymous", "jd1awxj")
    except Exception as err:
        print(err)
        print("FTP CONNECT ERROR")
        system("pause")
        exit()
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

    wxjsoftname = "ABCMW001.RAR"
    for ele in searchname(wxjnlst):
        if "MW" in ele or "WX" in ele:
            wxjsoftname = ele

    ftpstationame = wxjsoftname[0:3] + "_" + ip
    print(ftpstationame)
    newfile(ftpstationame)

    logsoftname = "ABCLOG001.RAR"
    for ele in searchname(mylognlst):
        if "LOG" in ele:
            logsoftname = ele

    q0 = nowdir + "\\" + ftpstationame + "\\JD1AWXJ" + "\\" + wxjsoftname
    q1 = 'RETR ' + "JD1AWXJ" + "\\" + wxjsoftname
    q2 = nowdir + "\\" + ftpstationame + "\\MYLOGSERVER" + "\\" + logsoftname
    q3 = 'RETR ' + "MYLOGSERVER" + "\\" + logsoftname
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
           (nowdir + "\\" + ftpstationame + "\\JD1AWXJ\\*W*.RAR",
            nowdir + "\\" + ftpstationame + "\\JD1AWXJ"))
    system("start winrar x -y -ikbc -inul %s %s" %
           (nowdir + "\\" + ftpstationame + "\\MYLOGSERVER\\*LOG*.RAR",
            nowdir + "\\" + ftpstationame + "\\MYLOGSERVER"))


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
        ra = "%s%s%s%s%s%s%s" % (nowdir, "\\", stationame, "\\MYLOGSERVER\\",
                                 type, "\\", file)
        rb = "%s%s%s%s%s" % ('RETR', "MYLOGSERVER\\", type, "\\", file)
        download(ftp, ra, rb)
    elif type in ("doginfo", "sysinfo", "alarms", "button", "replays",
                  "errors"):
        ra = "%s%s%s%s%s%s%s" % (nowdir, "\\", stationame, "\\JD1AWXJ\\", type,
                                 "\\", file)
        rb = "%s%s%s%s%s" % ('RETR', "JD1AWXJ\\", type, "\\", file)
        download(ftp, ra, rb)


#下载数据及异常处理
def download(ftp, localfile, remotefile):
    try:
        buf_size = 1024
        fp = open(localfile, 'wb')
        ftp.retrbinary(remotefile, fp.write, buf_size)
        fp.close()
        print("SUCCESS COPY %s " % (remotefile[4:]))
        return 1
    except Exception as err:
        print(err)
        print("FAILED COPY %s " % (remotefile))
        return 0


#新建指定空文件夹
def newfile(path):
    try:
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\replays")
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\doginfo")
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\sysinfo")
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\alarms")
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\button")
        makedirs(nowdir + "\\" + path + "\\jd1awxj" + "\\errors")
        makedirs(nowdir + "\\" + path + "\\mylogserver" + "\\Data")
        makedirs(nowdir + "\\" + path + "\\mylogserver" + "\\Log")
    except Exception as err:
        print(err)
        system("pause")
        exit()


#获取当前路径
nowdir = getcwd()
#读取配置文件并新建保存目录
x_c, jsondata, nowdir = mkpathandreadjson(nowdir)
#删除配置文件的空值
for key in list(jsondata.keys()):
    if not jsondata.get(key):
        del jsondata[key]
#检查配置文件是否有需要的值
lista = ("starttime", "endtime", "remote")
for ele in lista:
    if ele in jsondata:
        pass
    else:
        print("ERROR EASYCOPT.JSON")
        system("pause")
        exit()
#构造日期列表l0,l1,l2
l0, l1, l2 = geteveryday(jsondata["starttime"], jsondata["endtime"])
#本地拷贝日志
if jsondata["remote"] is "0":
    stationame = getstationame()
    nowdir = nowdir + "\\" + stationame
    copy(l0, l1, l2)
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
#远程拷贝日志
elif jsondata["remote"] is "1":
    popdict(jsondata, ["starttime", "endtime", "remote"])
    #检查是否为空
    if jsondata:
        copybyftp(l0, l1, l2, jsondata)
        print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
        print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
        print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
    else:
        print("NO IP HERE,CHECK EASYCOPY.JSON")
#异常
else:
    print("SOMETHING WRONG")
#暂停
system("pause")