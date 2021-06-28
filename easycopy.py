#!/bin/python
# -*- coding: utf-8 -*-
from os import system, getcwd, makedirs, walk, path
from datetime import datetime, timedelta
from json import load
from ftplib import FTP
from glob import glob
from itertools import zip_longest
from shutil import copy


#读取配置文件并新建保存目录
def mkpathandreadjson(newpath):
    nowtime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    try:
        jsondata = load(open(path.join(newpath, "easycopy.json")))
        newpath = path.join(newpath, nowtime)
    except Exception as err:
        print(err)
        print("CAN NOT FIND EASYCOPY.JSON")
        system("pause")
        exit()
    return jsondata, newpath


#构造日期列表l0,l1,l2
def geteveryday(begindate, enddate):
    datelist = []
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
        stationame = glob(path.join("E:\\jd1awxj", "*w*.RAR"))[0][11:14]
    except Exception as err:
        print(err)
        print("CAN NOT FIND JA1AWXJ")
        system("pause")
        exit()
    return stationame


#复制维修机数据
def copywxj(ll, l1, l2):
    for root, dirs, files in ll:
        for dir in dirs:
            try:
                makedirs(path.join(nowdir + root[2:], dir))
            except Exception as err:
                print(err)
                system("pause")
                exit()
        for file in files:
            for s1, s2 in zip(l1, l2):
                if s1 in file or s2 in file:
                    ccopy(root, file)
        for file in files:
            if ("RAR" in file or "rar" in file) and ("WX" in file
                                                     or "MW" in file):
                ccopy(root, file)
                break


#复制mylog数据
def copylog(ll, l0):
    for root, dirs, files in ll:
        for dir in dirs:
            try:
                makedirs(path.join(nowdir + root[2:], dir))
            except Exception as err:
                print(err)
                system("pause")
                exit()
        for file in files:
            for s0 in l0:
                if s0 in file:
                    ccopy(root, file)
        for file in files:
            if ("RAR" in file or "rar" in file) and ("MyLogServer_" in file
                                                     or "LOG" in file):
                ccopy(root, file)
                break


#复制数据以及异常处理
def ccopy(root, file):
    try:
        temp = path.join(root, file)
        copy(temp, path.join(nowdir + root[2:], file))
        print("SUCCESS COPY %s " % temp)
    except Exception as err:
        print(err)
        print("FAILED COPY %s " % temp)
        system("pause")
        exit()


def unzip():
    #解压软件到指定目录
    system("start winrar x -y -ikbc -inul %s %s" % (path.join(
        nowdir, "JD1AWXJ", "*W*.RAR"), path.join(nowdir, "JD1AWXJ")))
    system("start winrar x -y -ikbc -inul %s %s" % (path.join(
        nowdir, "MYLOGSERVER", "*LOG*.RAR"), path.join(nowdir, "MYLOGSERVER")))


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
    sysinfonlst = ftp.nlst("jd1awxj/sysinfo")
    Datanlst = ftp.nlst("mylogserver/Data")
    Lognlst = ftp.nlst("mylogserver/Log")

    wxjsoftname = "ABCMW001.RAR"
    for ele in searchname(wxjnlst):
        if "MW" in ele or "WX" in ele:
            wxjsoftname = ele
            break

    ftpstationame = wxjsoftname[0:3] + "_" + ip
    print(ftpstationame)
    newfile(ftpstationame)

    logsoftname = "ABCLOG001.RAR"
    for ele in searchname(mylognlst):
        if "LOG" in ele:
            logsoftname = ele
            break

    q0 = path.join(nowdir, ftpstationame, "JD1AWXJ", wxjsoftname)
    q1 = 'RETR ' + path.join("JD1AWXJ", wxjsoftname)
    q2 = path.join(nowdir, ftpstationame, "MYLOGSERVER", logsoftname)
    q3 = 'RETR ' + path.join("MYLOGSERVER", logsoftname)
    download(ftp, q0, q1)
    download(ftp, q2, q3)

    for Data, Log, doginfo, sysinfo, alarms, button, errors, replays in zip_longest(
            Datanlst, Lognlst, doginfonlst, sysinfonlst, alarmsnlst,
            buttonnlst, errorsnlst, replayslst):
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
           (path.join(nowdir, ftpstationame, "JD1AWXJ",
                      "*W*.RAR"), path.join(nowdir, ftpstationame, "JD1AWXJ")))
    system("start winrar x -y -ikbc -inul %s %s" %
           (path.join(nowdir, ftpstationame, "MYLOGSERVER", "*LOG*.RAR"),
            path.join(nowdir, ftpstationame, "MYLOGSERVER")))


#远程获取站名
def searchname(list):
    templist = []
    for ele in list:
        ele = ele.upper()
        if ele.endswith(".RAR"):
            templist.append(ele)
    return templist


#指定维修机和日志下载到不同地址
def wxjdownload(ftp, file, type, stationame):
    if type in ("Data", "Log"):
        ra = path.join(nowdir, stationame, "MYLOGSERVER", type, file)
        rb = 'RETR ' + path.join("MYLOGSERVER\\", type, file)
        download(ftp, ra, rb)
    elif type in ("doginfo", "sysinfo", "alarms", "button", "replays",
                  "errors"):
        ra = path.join(nowdir, stationame, "JD1AWXJ", type, file)
        rb = 'RETR ' + path.join("JD1AWXJ\\", type, file)
        download(ftp, ra, rb)


#下载数据及异常处理
def download(ftp, localfile, remotefile):
    try:
        buf_size = 1024
        fp = open(localfile, 'wb')
        ftp.retrbinary(remotefile, fp.write, buf_size)
        fp.close()
        print("SUCCESS DOWNLOAD %s " % (remotefile[4:]))
        return 1
    except Exception as err:
        print(err)
        print("FAILED DOWNLOAD %s " % (remotefile))
        return 0


#新建指定空文件夹
def newfile(newpath):
    try:
        makedirs(path.join(nowdir, newpath, "jd1awxj", "replays"))
        makedirs(path.join(nowdir, newpath, "jd1awxj", "doginfo"))
        makedirs(path.join(nowdir, newpath, "jd1awxj", "sysinfo"))
        makedirs(path.join(nowdir, newpath, "jd1awxj", "alarms"))
        makedirs(path.join(nowdir, newpath, "jd1awxj", "button"))
        makedirs(path.join(nowdir, newpath, "jd1awxj", "errors"))
        makedirs(path.join(nowdir, newpath, "mylogserver", "Data"))
        makedirs(path.join(nowdir, newpath, "mylogserver", "Log"))
    except Exception as err:
        print(err)
        system("pause")
        exit()


#判断ipv4地址是否合法
def is_ipv4(ip: str) -> bool:
    return True if [1] * 4 == [
        x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")
    ] else False


#检查easycopy.json各项值的正确性，返回日期，以及是否远程
def checkjson(jsondata):
    #删除空值
    for key in list(jsondata.keys()):
        if not jsondata.get(key):
            del jsondata[key]

    #检查各项值是否合理
    try:
        begindate = datetime.strptime(jsondata["starttime"], "%Y-%m-%d")
        enddate = datetime.strptime(jsondata["endtime"], "%Y-%m-%d")
        if jsondata["remote"] in ("0", "1"):
            pass
        else:
            print("ERROR EASYCOPT.JSON STARTTIME,ENDTIME,REMOTE")
            system("pause")
            exit()
    except Exception as err:
        print(err)
        print("ERROR EASYCOPT.JSON STARTTIME,ENDTIME,REMOTE")
        system("pause")
        exit()

    #得到IP字典并检查是否为空，不为空检查IP地址的正确性
    if jsondata["remote"] is "1":
        remoteornot = True
        popdict(jsondata, ["starttime", "endtime", "remote"])
        if not jsondata:
            for ele in jsondata:
                if not is_ipv4(ele):
                    print("ERROR EASYCOPT.JSON IP")
                    system("pause")
                    exit()
            print("ERROR EASYCOPT.JSON IP")
            system("pause")
            exit()
    else:
        remoteornot = False
    return begindate, enddate, remoteornot


#获取当前程序路径
nowdir = getcwd()

#读取easycopy.json并新建日志保存目录
jsondata, nowdir = mkpathandreadjson(nowdir)

#检查easycopy.json各项值的正确性,返回日期，以及是否远程
begindate, enddate, remoteornot = checkjson(jsondata)

#新建保存目录
try:
    makedirs(nowdir)
except Exception as err:
    print(err)
    print("CAN NOT NEW DIRECTORY")
    system("pause")
    exit()

#构造日期列表l0,l1,l2
l0, l1, l2 = geteveryday(begindate, enddate)

#远程拷贝日志
if remoteornot:
    #检查是否为空
    if jsondata:
        copybyftp(l0, l1, l2, jsondata)
        print("All DATA HAS BEEN DOWNLOADED TO %s " % (nowdir))
        print("All DATA HAS BEEN DOWNLOADED TO %s " % (nowdir))
        print("All DATA HAS BEEN DOWNLOADED TO %s " % (nowdir))

#本地拷贝日志
else:
    stationame = getstationame()
    nowdir = path.join(nowdir, stationame)
    copywxj(walk("e:\\jd1awxj"), l1, l2)
    copylog(walk("e:\\mylogserver"), l0)
    unzip()
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))
    print("All DATA HAS BEEN COPIED TO %s " % (nowdir))

#暂停
system("pause")
exit()