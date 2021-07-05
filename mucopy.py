#!/bin/python
# -*- coding: utf-8 -*-
from os import system, getcwd, makedirs, walk, path
from datetime import datetime, timedelta
from json import load
from ftplib import FTP
from glob import glob
from itertools import zip_longest
from shutil import copy


#Json类，读取mucopy.json,检查该json,生成构造日期list
class MUJson:
    #初始化
    def __init__(self):
        self.mudir = getcwd()
        self.mudata = {}
        self.muremote = "0"
        self.mula, self.mulb, self.mulc = [[] for i in range(3)]

    def mujson(self):
        print("START READ MUCOPY.JSON")
        self.__checkjson()
        print("MUCOPY.JSON READ SUCCESSFULLY\n")

    #检查各项值的合理性
    def __checkjson(self):
        self.__getjson()
        #去掉空值
        for key in list(self.mudata.keys()):
            if not self.mudata.get(key):
                del self.mudata[key]
        #验证日期的合理性
        try:
            begindate = datetime.strptime(self.mudata["starttime"], "%Y-%m-%d")
            enddate = datetime.strptime(self.mudata["endtime"], "%Y-%m-%d")
            if self.mudata["remote"] in ("0", "1", "2"):
                pass
            else:
                print("ERROR MUCOPT.JSON STARTTIME,ENDTIME,REMOTE")
                system("pause")
                exit()
        except Exception as err:
            print(err)
            print("ERROR MUCOPT.JSON STARTTIME,ENDTIME,REMOTE")
            system("pause")
            exit()
        #仅远程下载
        if self.mudata["remote"] is "1":
            self.muremote = "1"
            #删除对应的键值对
            for k in ["starttime", "endtime", "remote"]:
                self.mudata.pop(k)
            if not self.mudata:
                for ele in self.mudata:
                    if not self.__is_ipv4(ele):
                        print("ERROR MUCOPT.JSON IP")
                        system("pause")
                        exit()
                print("ERROR MUCOPT.JSON IP")
                system("pause")
                exit()
        #远程下载和本地复制
        elif self.mudata["remote"] is "2":
            self.muremote = "2"
            #删除对应的键值对
            for k in ["starttime", "endtime", "remote"]:
                self.mudata.pop(k)
            if not self.mudata:
                for ele in self.mudata:
                    if not self.__is_ipv4(ele):
                        print("ERROR MUCOPT.JSON IP")
                        system("pause")
                        exit()
                print("ERROR MUCOPT.JSON IP")
                system("pause")
                exit()
        #仅本地复制
        else:
            self.muremote = "0"
        self.__geteveryday(begindate, enddate)

    #读取mucopy.py，更新mudir的值
    def __getjson(self):
        nowtime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        try:
            self.mudata = load(open(path.join(self.mudir, "mucopy.json")))
            self.mudir = path.join(self.mudir, nowtime)
        except Exception as err:
            print(err)
            print("CAN NOT FIND MUCOPY.JSON")
            system("pause")
            exit()

    #检查ip的合理性
    def __is_ipv4(ip: str) -> bool:
        return True if [1] * 4 == [
            x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")
        ] else False

    #构造生成3个日期列表
    def __geteveryday(self, begindate, enddate):
        if (begindate > enddate):
            begindate, enddate = enddate, begindate
        while begindate <= enddate:
            date_str = begindate.strftime("%Y-%m-%d")
            self.mula.append(date_str)
            begindate += timedelta(days=1)
        for date in self.mula:
            self.mulb.append(date.replace("-", "_"))
        for date in self.mulb:
            if (date[5] == "0"):
                if (date[8] == "0"):
                    self.mulc.append(date[-4:-2] + date[-1:])
                else:
                    self.mulc.append(date[-4:])
            else:
                if (date[8] == "0"):
                    self.mulc.append(date[-5:-2] + date[-1:])
                else:
                    self.mulc.append(date[-5:])


#Copy类，根据日期复制维修机回放和日志
class MUCopy:
    #初始化，传入各项值
    def __init__(self, mudir, mula, mulb, mulc):
        self.mudir = mudir
        self.mula, self.mulb, self.mulc = mula, mulb, mulc

    #主函数，调用其他函数
    def mucopy(self):
        print("START COPY LOCAL DATA")
        self.__getstationame()
        self.__copywxj()
        self.__copylog()
        self.__unrar()
        print("LOCAL DATA COPY SUCCESSFULLY\n")

    #得到站名缩写
    def __getstationame(self):
        try:
            stationame = glob(path.join("E:\\jd1awxj", "*w*.RAR"))[0][11:14]
            self.mudir = path.join(self.mudir, stationame)
        except Exception as err:
            print(err)
            print("CAN NOT FIND JA1AWXJ")
            system("pause")
            exit()

    #遍历并复制维修机数据
    def __copywxj(self):
        for root, dirs, files in walk("e:\\jd1awxj"):
            for dir in dirs:
                try:
                    makedirs(path.join(self.mudir + root[2:], dir))
                except Exception as err:
                    print(err)
                    system("pause")
                    exit()
            for file in files:
                for s1, s2 in zip(self.mulb, self.mulc):
                    if s1 in file or s2 in file:
                        self.__ccopy(root, file)
            for file in files:
                if ("RAR" in file or "rar" in file) and ("WX" in file
                                                         or "MW" in file):
                    self.__ccopy(root, file)
                    break

    #遍历并复制LOG数据
    def __copylog(self):
        for root, dirs, files in walk("e:\\mylogserver"):
            for dir in dirs:
                try:
                    makedirs(path.join(self.mudir + root[2:], dir))
                except Exception as err:
                    print(err)
                    system("pause")
                    exit()
            for file in files:
                for s0 in self.mula:
                    if s0 in file:
                        self.__ccopy(root, file)
            for file in files:
                if ("RAR" in file or "rar" in file) and ("MyLogServer_" in file
                                                         or "LOG" in file):
                    self.__ccopy(root, file)
                    break

    #复制文件函数
    def __ccopy(self, root, file):
        try:
            temp = path.join(root, file)
            copy(temp, path.join(self.mudir + root[2:], file))
            print("SUCCESS COPY %s " % temp)
        except Exception as err:
            print(err)
            print("FAILED COPY %s " % temp)
            system("pause")
            exit()

    #解压缩软件到相应目录
    def __unrar(self):
        system("start winrar x -y -ikbc -inul %s %s" %
               (path.join(self.mudir, "JD1AWXJ",
                          "*W*.RAR"), path.join(self.mudir, "JD1AWXJ")))
        system("start winrar x -y -ikbc -inul %s %s" %
               (path.join(self.mudir, "MYLOGSERVER",
                          "*LOG*.RAR"), path.join(self.mudir, "MYLOGSERVER")))


#FTP类，根据IP、日期远程下载维修机回放和日志
class MUFtp:
    #初始化，传入各项值
    def __init__(self, mudir, mudata, mula, mulb, mulc):
        self.mudir = mudir
        self.mudata = mudata
        self.mula, self.mulb, self.mulc = mula, mulb, mulc

    #主函数
    def muftp(self):
        for ip in self.mudata:
            print("START DOWNLOAD REMOTE DATA")
            self.__dlfromip(self.mudata[ip])
            print("REMOTE DATA DOWNLOAD SUCCESSFULLY\n")

    #建立对应IP的FTP连接，调用函数
    def __dlfromip(self, ip):
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
        #调用其他函数，保证mudir值不被修改
        temp = self.mudir
        self.__dlsoft(ftp, ip)
        self.__traverse(ftp)
        self.__unrar()
        self.mudir = temp
        ftp.quit()

    #下载维修机和日志软件包
    def __dlsoft(self, ftp, ip):
        wxjnlst = ftp.nlst("jd1awxj")
        mylognlst = ftp.nlst("mylogserver")
        wxjsoftname = "ABCMW001.RAR"
        for ele in self.__searchname(wxjnlst):
            if "MW" in ele or "WX" in ele:
                wxjsoftname = ele
                break
        #生成包含站名、IP的新mudir
        self.mudir = path.join(self.mudir, wxjsoftname[0:3] + "_" + ip)
        self.__newfile(self.mudir)
        logsoftname = "ABCLOG001.RAR"
        for ele in self.__searchname(mylognlst):
            if "LOG" in ele:
                logsoftname = ele
                break
        #下载维修机和日志软件
        q0 = path.join(self.mudir, self.mudir, "JD1AWXJ", wxjsoftname)
        q1 = 'RETR ' + path.join("JD1AWXJ", wxjsoftname)
        q2 = path.join(self.mudir, self.mudir, "MYLOGSERVER", logsoftname)
        q3 = 'RETR ' + path.join("MYLOGSERVER", logsoftname)
        self.__download(ftp, q0, q1)
        self.__download(ftp, q2, q3)

    #返回以RAR为后缀的文件名
    def __searchname(self, list):
        templist = []
        for ele in list:
            ele = ele.upper()
            if ele.endswith(".RAR"):
                templist.append(ele)
        return templist

    #创建各项空文件夹
    def __newfile(self, newpath):
        try:
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "replays"))
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "doginfo"))
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "sysinfo"))
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "alarms"))
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "button"))
            makedirs(path.join(self.mudir, newpath, "jd1awxj", "errors"))
            makedirs(path.join(self.mudir, newpath, "mylogserver", "Data"))
            makedirs(path.join(self.mudir, newpath, "mylogserver", "Log"))
        except Exception as err:
            print(err)
            system("pause")
            exit()

    #FTP下载函数
    def __download(self, ftp, localfile, remotefile):
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

    #遍历各文件夹并下载
    def __traverse(self, ftp):
        ftpnlst = [
            ftp.nlst("mylogserver/Data"),
            ftp.nlst("mylogserver/Log"),
            ftp.nlst("jd1awxj/doginfo"),
            ftp.nlst("jd1awxj/sysinfo"),
            ftp.nlst("jd1awxj/alarms"),
            ftp.nlst("jd1awxj/button"),
            ftp.nlst("jd1awxj/errors"),
            ftp.nlst("jd1awxj/replays")
        ]
        for Data, Log, doginfo, sysinfo, alarms, button, errors, replays in zip_longest(
                *ftpnlst):
            for s0, s1, s2 in zip(self.mula, self.mulb, self.mulc):
                if Data:
                    if s0 in Data:
                        self.__dlwxjlog(ftp, Data, "Data")
                if Log:
                    if s0 in Log:
                        self.__dlwxjlog(ftp, Log, "Log")
                if doginfo:
                    if s1 in doginfo:
                        self.__dlwxjlog(ftp, doginfo, "doginfo")
                if sysinfo:
                    if s1 in sysinfo:
                        self.__dlwxjlog(ftp, sysinfo, "sysinfo")
                if alarms:
                    if s2 in alarms:
                        self.__dlwxjlog(ftp, alarms, "alarms")
                if button:
                    if s2 in button:
                        self.__dlwxjlog(ftp, button, "button")
                if errors:
                    if s2 in errors:
                        self.__dlwxjlog(ftp, errors, "errors")
                if replays:
                    if s2 in replays:
                        self.__dlwxjlog(ftp, replays, "replays")

    #分别指定不同文件的下载位置
    def __dlwxjlog(self, ftp, file, type):
        if type in ("Data", "Log"):
            ra = path.join(self.mudir, "MYLOGSERVER", type, file)
            rb = 'RETR ' + path.join("MYLOGSERVER\\", type, file)
            self.__download(ftp, ra, rb)
        elif type in ("doginfo", "sysinfo", "alarms", "button", "replays",
                      "errors"):
            ra = path.join(self.mudir, "JD1AWXJ", type, file)
            rb = 'RETR ' + path.join("JD1AWXJ\\", type, file)
            self.__download(ftp, ra, rb)

    #解压软件到指定位置
    def __unrar(self):
        system("start winrar x -y -ikbc -inul %s %s" %
               (path.join(self.mudir, "JD1AWXJ",
                          "*W*.RAR"), path.join(self.mudir, "JD1AWXJ")))
        system("start winrar x -y -ikbc -inul %s %s" %
               (path.join(self.mudir, "MYLOGSERVER",
                          "*LOG*.RAR"), path.join(self.mudir, "MYLOGSERVER")))


#MUJson类实例化并调用函数
Mujson = MUJson()
Mujson.mujson()

#MUFtp类实例化并调用函数
Muftp = MUFtp(Mujson.mudir, Mujson.mudata, Mujson.mula, Mujson.mulb,
              Mujson.mulc)
#MUCopy类实例化并调用函数
Mucopy = MUCopy(Mujson.mudir, Mujson.mula, Mujson.mulb, Mujson.mulc)

#判断是否需要远程,"0":本地,"1":远程,"2":远程+本地,
if Mujson.muremote is "0":
    Mucopy.mucopy()
elif Mujson.muremote is "1":
    Muftp.muftp()
elif Mujson.muremote is "2":
    Muftp.muftp()
    Mucopy.mucopy()

#输出完成信息
print("All DATA COPIED SUCCESSFULLY %s " % (Mujson.mudir))
print("All DATA COPIED SUCCESSFULLY %s " % (Mujson.mudir))
print("All DATA COPIED SUCCESSFULLY %s " % (Mujson.mudir))
system("pause")
exit()
