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
        #mudir F:\  mula 2021-07-08 mulb 2021_07_08 mulc 5_9、5_10
        self.mudir = getcwd()
        self.mudata = {}
        self.muremote = '0'
        self.mula, self.mulb, self.mulc = [[] for i in range(3)]

    def mujson(self):
        print('START READ MUCOPY.JSON')
        self.__checkjson()
        print('MUCOPY.JSON READ SUCCESSFULLY\n')

    #检查各项值的合理性
    def __checkjson(self):
        self.__getjson()
        #去掉空值
        for key in list(self.mudata.keys()):
            if not self.mudata.get(key):
                del self.mudata[key]
        #验证日期的合理性
        try:
            begindate = datetime.strptime(self.mudata['starttime'], '%Y-%m-%d')
            enddate = datetime.strptime(self.mudata['endtime'], '%Y-%m-%d')
        except Exception as err:
            print(err)
            print('ERROR MUCOPT.JSON STARTTIME,ENDTIME')
            system('pause')
            exit()
        #日期生成需要的列表
        self.__geteveryday(begindate, enddate)
        #验证remote的合理性
        try:
            if self.mudata['remote'] in ('0', '1', '2'):
                pass
            else:
                print('ERROR MUCOPT.JSON REMOTE')
                system('pause')
                exit()
        except Exception as err:
            print(err)
            print('ERROR MUCOPT.JSON REMOTE')
            system('pause')
            exit()
        #仅远程下载
        if self.mudata['remote'] is '1':
            self.muremote = '1'
            #删除对应的键值对
            for k in ['starttime', 'endtime', 'remote']:
                self.mudata.pop(k)
            if not self.mudata:
                for ele in self.mudata:
                    if not self.__is_ipv4(ele):
                        print('ERROR MUCOPT.JSON IP')
                        system('pause')
                        exit()
                print('ERROR MUCOPT.JSON IP')
                system('pause')
                exit()
        #远程下载和本地复制
        elif self.mudata['remote'] is '2':
            self.muremote = '2'
            #删除对应的键值对
            for k in ['starttime', 'endtime', 'remote']:
                self.mudata.pop(k)
            if not self.mudata:
                for ele in self.mudata:
                    if not self.__is_ipv4(ele):
                        print('ERROR MUCOPT.JSON IP')
                        system('pause')
                        exit()
                print('ERROR MUCOPT.JSON IP')
                system('pause')
                exit()
        #仅本地复制
        elif self.mudata['remote'] is '0':
            self.muremote = '0'

    #读取mucopy.json，更新mudir的值
    def __getjson(self):
        nowtime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        try:
            self.mudata = load(open(path.join(self.mudir, 'mucopy.json')))
            self.mudir = path.join(self.mudir, nowtime)
        except Exception as err:
            print(err)
            print('CAN NOT FIND MUCOPY.JSON')
            system('pause')
            exit()

    #检查ip地址的合理性
    def __is_ipv4(ip: str) -> bool:
        return True if [1] * 4 == [
            x.isdigit() and 0 <= int(x) <= 255 for x in ip.split('.')
        ] else False

    #构造生成3个日期列表
    def __geteveryday(self, begindate, enddate):
        #比较起始日期，如果时间早晚不对，则交换起始日期
        if (begindate > enddate):
            begindate, enddate = enddate, begindate
        #遍历日期，生成列表mula 2021-07-08
        while begindate <= enddate:
            date_str = begindate.strftime('%Y-%m-%d')
            self.mula.append(date_str)
            begindate += timedelta(days=1)
        #列表mula生成mulb 2021_07_08
        for date in self.mula:
            self.mulb.append(date.replace('-', '_'))
        #生成mulc 5_9、5_10、5_11
        for date in self.mulb:
            if (date[5] == '0'):
                if (date[8] == '0'):
                    self.mulc.append(date[-4:-2] + date[-1:])
                else:
                    self.mulc.append(date[-4:])
            else:
                if (date[8] == '0'):
                    self.mulc.append(date[-5:-2] + date[-1:])
                else:
                    self.mulc.append(date[-5:])


#Copy类，根据日期复制维修机回放和日志
class MUCopy:
    #初始化，传入路径、列表la、lb、lc
    def __init__(self, mudir, mula, mulb, mulc):
        self.mudir = mudir
        self.mula, self.mulb, self.mulc = mula, mulb, mulc

    #主函数，调用其他函数
    def mucopy(self):
        print('START COPY LOCAL DATA')
        self.__getstationame()
        self.__copywxj()
        self.__copylog()
        self.__unrar()
        print('LOCAL DATA COPY SUCCESSFULLY\n')

    #得到E盘维修机下站名缩写，添加至mudir后面
    def __getstationame(self):
        try:
            stationame = glob(path.join('E:\\jd1awxj', '*w*.RAR'))[0][11:14]
            self.mudir = path.join(self.mudir, stationame)
        except Exception as err:
            print(err)
            print('CAN NOT FIND JA1AWXJ')
            system('pause')
            exit()

    #遍历并复制维修机数据
    def __copywxj(self):
        #遍历jd1awxj
        for root, dirs, files in walk('e:\\jd1awxj'):
            #遍历并新建既有的文件夹目录
            for dir in dirs:
                try:
                    makedirs(path.join(self.mudir + root[2:], dir))
                except Exception as err:
                    print(err)
                    system('pause')
                    exit()
            #遍历文件并判断日期下载文件
            for file in files:
                for s1, s2 in zip(self.mulb, self.mulc):
                    if s1 in file or s2 in file:
                        self.__ccopy(root, file)
            #下载维修机软件包
            for file in files:
                if ('RAR' in file or 'rar' in file) and ('WX' in file
                                                         or 'MW' in file):
                    self.__ccopy(root, file)
                    break

    #遍历并复制LOG数据
    def __copylog(self):
        #遍历mylogserver
        for root, dirs, files in walk('e:\\mylogserver'):
            #遍历并新建既有的文件夹目录
            for dir in dirs:
                try:
                    makedirs(path.join(self.mudir + root[2:], dir))
                except Exception as err:
                    print(err)
                    system('pause')
                    exit()
            #遍历文件并判断日期下载文件
            for file in files:
                for s0 in self.mula:
                    if s0 in file:
                        self.__ccopy(root, file)
            #下载日志软件包
            for file in files:
                if ('RAR' in file or 'rar' in file) and ('MyLogServer_' in file
                                                         or 'LOG' in file):
                    self.__ccopy(root, file)
                    break

    #拼接目录和文件，确定下载路径、复制文件
    def __ccopy(self, root, file):
        try:
            temp = path.join(root, file)
            copy(temp, path.join(self.mudir + root[2:], file))
            print('SUCCESS COPY %s ' % temp)
        except Exception as err:
            print(err)
            print('FAILED COPY %s ' % temp)
            system('pause')
            exit()

    #解压缩软件到相应目录
    def __unrar(self):
        system('start winrar x -y -ikbc -inul %s %s' %
               (path.join(self.mudir, 'JD1AWXJ',
                          '*W*.RAR'), path.join(self.mudir, 'JD1AWXJ')))
        system('start winrar x -y -ikbc -inul %s %s' %
               (path.join(self.mudir, 'MYLOGSERVER',
                          '*LOG*.RAR'), path.join(self.mudir, 'MYLOGSERVER')))


#FTP类，根据IP、日期远程下载维修机回放和日志
class MUFtp:
    #初始化，传入路径、jsondata、列表la、lb、lc等值
    def __init__(self, mudir, mudata, mula, mulb, mulc):
        self.mudir = mudir
        self.mudata = mudata
        self.mula, self.mulb, self.mulc = mula, mulb, mulc

    #主函数，遍历ip下载
    def muftp(self):
        for ip in self.mudata:
            print('START DOWNLOAD REMOTE DATA')
            self.__dlfromip(self.mudata[ip])
            print('REMOTE DATA DOWNLOAD SUCCESSFULLY\n')

    #建立对应IP的FTP连接，调用其他函数
    def __dlfromip(self, ip):
        try:
            ftp = FTP()
            ftp.connect(ip, 21)
            # ftp.login('Remote','jd1awxj')
            ftp.login('Anonymous', 'jd1awxj')
        except Exception as err:
            print(err)
            print('FTP CONNECT ERROR')
            system('pause')
            exit()
        #调用其他函数，保证mudir值在下载完毕后不被修改
        temp = self.mudir
        self.__dlsoft(ftp, ip)
        self.__traverse(ftp)
        self.__unrar()
        self.mudir = temp
        ftp.quit()

    #下载维修机和日志软件包
    def __dlsoft(self, ftp, ip):
        #生成wxj、log文件列表
        wxjnlst = ftp.nlst('jd1awxj')
        mylognlst = ftp.nlst('mylogserver')
        #返回空列表就退出程序
        if (not wxjnlst) or (not mylognlst):
            print('ERROR, NO DATA UNDER THE REMOTE FOLDER')
            system('pause')
            exit()
        #默认站名软件为空
        wxjsoftname = ''
        #遍历wxj文件列表，返回wxj软件名称，多个压缩包只返回第一个
        for ele in self.__searchname(wxjnlst):
            if 'MW' in ele or 'WX' in ele:
                wxjsoftname = ele
                break
        #如果返回wxj站名软件不为空
        if not wxjsoftname is '':
            #生成包含站名、IP的新mudir
            self.mudir = path.join(self.mudir, wxjsoftname[0:3] + '_' + ip)
            #新建wxj、log下各文件夹
            self.__newfile(self.mudir)
            #下载该软件
            q0 = path.join(self.mudir, self.mudir, 'JD1AWXJ', wxjsoftname)
            q1 = 'RETR ' + path.join('JD1AWXJ', wxjsoftname)
            self.__download(ftp, q0, q1)
        #返回wxj站名软件为空
        else:
            #默认名字'ABCMW001.RAR'
            wxjsoftname = 'ABCMW001.RAR'
            #生成包含站名、IP的新mudir
            self.mudir = path.join(self.mudir, wxjsoftname[0:3] + '_' + ip)
            #新建wxj、log下各文件夹
            self.__newfile(self.mudir)
            print('NO WXJ SOFT,DEFAULT NAME ABC')
        #默认log软件为空
        logsoftname = ''
        #遍历log文件列表，返回wxj软件名称，多个压缩包只返回第一个
        for ele in self.__searchname(mylognlst):
            if 'LOG' in ele:
                logsoftname = ele
                break
        #如果返回log站名软件不为空
        if not logsoftname is '':
            #下载该软件
            q2 = path.join(self.mudir, self.mudir, 'MYLOGSERVER', logsoftname)
            q3 = 'RETR ' + path.join('MYLOGSERVER', logsoftname)
            self.__download(ftp, q2, q3)
        #返回log站名软件为空
        else:
            print('NO LOG SOFT')

    #遍历列表，返回以RAR为后缀的文件名
    def __searchname(self, list):
        templist = []
        for ele in list:
            ele = ele.upper()
            if ele.endswith('.RAR'):
                templist.append(ele)
        return templist

    #创建wxj、log下空文件夹
    def __newfile(self, newpath):
        try:
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'replays'))
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'doginfo'))
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'sysinfo'))
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'alarms'))
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'button'))
            makedirs(path.join(self.mudir, newpath, 'jd1awxj', 'errors'))
            makedirs(path.join(self.mudir, newpath, 'mylogserver', 'Data'))
            makedirs(path.join(self.mudir, newpath, 'mylogserver', 'Log'))
        except Exception as err:
            print(err)
            system('pause')
            exit()

    #FTP下载函数，缓冲区1024，二进制方式读写
    def __download(self, ftp, localfile, remotefile):
        try:
            # fp = open(localfile, 'wb')
            # ftp.retrbinary(remotefile, fp.write, 1024)
            # fp.close()
            with open(localfile, 'wb') as fp:
                ftp.retrbinary(remotefile, fp.write, 1024)
            print('SUCCESS DOWNLOAD %s ' % (remotefile[4:]))
            return 1
        except Exception as err:
            print(err)
            print('FAILED DOWNLOAD %s ' % (remotefile))
            return 0

    #遍历各文件夹并下载
    def __traverse(self, ftp):
        #构造列表
        ftpnlst = [
            ftp.nlst('mylogserver/Data'),
            ftp.nlst('mylogserver/Log'),
            ftp.nlst('jd1awxj/doginfo'),
            ftp.nlst('jd1awxj/sysinfo'),
            ftp.nlst('jd1awxj/alarms'),
            ftp.nlst('jd1awxj/button'),
            ftp.nlst('jd1awxj/errors'),
            ftp.nlst('jd1awxj/replays')
        ]
        #遍历文件列表，下载在指定日期的文件
        for Data, Log, doginfo, sysinfo, alarms, button, errors, replays in zip_longest(
                *ftpnlst):
            for s0, s1, s2 in zip(self.mula, self.mulb, self.mulc):
                if Data:
                    if s0 in Data:
                        self.__dllog(ftp, Data, 'Data')
                if Log:
                    if s0 in Log:
                        self.__dllog(ftp, Log, 'Log')
                if doginfo:
                    if s1 in doginfo:
                        self.__dlwxj(ftp, doginfo, 'doginfo')
                if sysinfo:
                    if s1 in sysinfo:
                        self.__dlwxj(ftp, sysinfo, 'sysinfo')
                if alarms:
                    if s2 in alarms:
                        self.__dlwxj(ftp, alarms, 'alarms')
                if button:
                    if s2 in button:
                        self.__dlwxj(ftp, button, 'button')
                if errors:
                    if s2 in errors:
                        self.__dlwxj(ftp, errors, 'errors')
                if replays:
                    if s2 in replays:
                        self.__dlwxj(ftp, replays, 'replays')

    #分别指定wxj的下载位置
    def __dlwxj(self, ftp, file, type):
        ra = path.join(self.mudir, 'JD1AWXJ', type, file)
        rb = 'RETR ' + path.join('JD1AWXJ\\', type, file)
        self.__download(ftp, ra, rb)

    #分别指定log的下载位置
    def __dllog(self, ftp, file, type):
        ra = path.join(self.mudir, 'MYLOGSERVER', type, file)
        rb = 'RETR ' + path.join('MYLOGSERVER\\', type, file)
        self.__download(ftp, ra, rb)

    #解压软件到指定位置
    def __unrar(self):
        system('start winrar x -y -ikbc -inul %s %s' %
               (path.join(self.mudir, 'JD1AWXJ',
                          '*W*.RAR'), path.join(self.mudir, 'JD1AWXJ')))
        system('start winrar x -y -ikbc -inul %s %s' %
               (path.join(self.mudir, 'MYLOGSERVER',
                          '*LOG*.RAR'), path.join(self.mudir, 'MYLOGSERVER')))


#MUJson类实例化并调用函数
Mujson = MUJson()
Mujson.mujson()

#MUFtp类实例化并调用函数
Muftp = MUFtp(Mujson.mudir, Mujson.mudata, Mujson.mula, Mujson.mulb,
              Mujson.mulc)
#MUCopy类实例化并调用函数
Mucopy = MUCopy(Mujson.mudir, Mujson.mula, Mujson.mulb, Mujson.mulc)

#判断是否需要远程,'0':本地,'1':远程,'2':远程+本地,
if Mujson.muremote is '0':
    Mucopy.mucopy()
elif Mujson.muremote is '1':
    Muftp.muftp()
elif Mujson.muremote is '2':
    Muftp.muftp()
    Mucopy.mucopy()

#输出完成信息
print('All DATA COPIED SUCCESSFULLY %s ' % (Mujson.mudir))
print('All DATA COPIED SUCCESSFULLY %s ' % (Mujson.mudir))
print('All DATA COPIED SUCCESSFULLY %s ' % (Mujson.mudir))
system('pause')
exit()