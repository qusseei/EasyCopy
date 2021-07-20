#!/bin/python
# -*- coding: utf-8 -*-
from json import load
from glob import glob
from ftplib import FTP
from shutil import copy2
from re import compile, search
from time import strptime, mktime, time
from datetime import datetime, timedelta
from os import system, getcwd, makedirs, walk, utime, path


#Json类，读取mucopy.json,检查该json,生成构造日期list
class MUJson:
    #初始化
    def __init__(self):
        #mudir F:\  musa 2021-07-08 musb 2021_07_08 musc 5_9、5_10
        self.mudir = getcwd()
        self.mudata = {}
        self.muremote = '0'
        self.musa, self.musb, self.musc = [set() for i in range(3)]

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
        with open(path.join(self.mudir, 'mucopy.json')) as f:
            self.mudata = load(f)
            self.mudir = path.join(self.mudir, nowtime)

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
        #遍历日期，生成列表musa 2021-07-08
        while begindate <= enddate:
            date_str = begindate.strftime('%Y-%m-%d')
            self.musa.add(date_str)
            begindate += timedelta(days=1)
        #列表musa生成musb 2021_07_08
        for date in self.musa:
            self.musb.add(date.replace('-', '_'))
        #生成musc 5_9、5_10、5_11
        for date in self.musb:
            if (date[5] == '0'):
                if (date[8] == '0'):
                    self.musc.add(date[-4:-2] + date[-1:])
                else:
                    self.musc.add(date[-4:])
            else:
                if (date[8] == '0'):
                    self.musc.add(date[-5:-2] + date[-1:])
                else:
                    self.musc.add(date[-5:])


#Copy类，根据日期复制维修机回放和日志
class MUCopy:
    #初始化，传入路径、列表la、lb、lc
    def __init__(self, mudir, musa, musb, musc):
        self.mudir = mudir
        self.musa, self.musb, self.musc = musa, musb, musc
        self.pattern = compile(r'\d{0,4}[-_]{0,1}\d{1,2}[-_]{1}\d{1,2}')
        self.slog = {'e:\mylogserver\Data', 'e:\mylogserver\Log'}
        self.swxj = {
            'e:\jd1awxj', 'e:\jd1awxj\images', 'e:\jd1awxj\ini',
            'e:\jd1awxj\\netmap'
        }

    #主函数，调用其他函数
    def mucopy(self):
        print('START COPY LOCAL DATA')
        self.__getstationame()
        self.__copywxj()
        self.__copylog()
        print('LOCAL DATA COPY SUCCESSFULLY\n')

    #得到E盘维修机下站名缩写，添加至mudir后面
    def __getstationame(self):
        try:
            stationame = glob(path.join('E:\\jd1awxj', '*w*.RAR'))[0][11:14]
            self.mudir = path.join(self.mudir, stationame)
        except Exception as err:
            print(err)
            print('CAN NOT FIND JA1AWXJ SOFT, SET DEFAULT NAME "ABC"')
            self.mudir = path.join(self.mudir, 'ABC')

    #遍历并复制维修机数据
    def __copywxj(self):
        #遍历jd1awxj
        for root, dirs, files in walk('e:\\jd1awxj'):
            #创建root
            if root:
                try:
                    makedirs(path.join(self.mudir, root[3:]))
                except Exception as err:
                    print(err)
                    system('pause')
                    exit()
            #指定目录，直接下载
            if root in self.swxj or root[:-2] in self.swxj:
                for file in files:
                    self.__ccopy(root, file)
            #其他目录，遍历文件剥离出日期并判断是否在列表中，下载文件
            else:
                for file in files:
                    newstr = self.pattern.search(file).group()
                    if newstr in self.musb or newstr in self.musc:
                        self.__ccopy(root, file)

    #遍历并复制LOG数据
    def __copylog(self):
        #遍历mylogserver
        for root, dirs, files in walk('e:\\mylogserver'):
            #创建root
            if root:
                try:
                    makedirs(path.join(self.mudir, root[3:]))
                except Exception as err:
                    print(err)
                    system('pause')
                    exit()
            #遍历文件，判断日期
            if root in self.slog:
                for file in files:
                    if self.pattern.search(file).group() in self.musa:
                        self.__ccopy(root, file)
            #其他文件直接下载
            else:
                for file in files:
                    self.__ccopy(root, file)

    #拼接目录和文件，确定下载路径、复制文件
    def __ccopy(self, root, file):
        try:
            temp = path.join(root, file)
            copy2(temp, path.join(self.mudir + root[2:], file))
            print('SUCCESS COPY %s ' % temp)
        except Exception as err:
            print(err)
            print('FAILED COPY %s ' % temp)
            system('pause')
            exit()


#FTP类，根据IP、日期远程下载维修机回放和日志
class MUFtp:
    #初始化，传入路径、jsondata、列表la、lb、lc等值
    def __init__(self, mudir, mudata, musa, musb, musc):
        self.mudir = mudir
        self.mudata = mudata
        self.musa, self.musb, self.musc = musa, musb, musc
        self.pattern = compile(r'\d{0,4}[-_]{0,1}\d{1,2}[-_]{1}\d{1,2}')
        self.slog = {'\mylogserver\Data', '\mylogserver\Log'}
        self.swxj = {
            '\jd1awxj', '\jd1awxj\images', '\jd1awxj\ini', '\jd1awxj\\netmap'
        }

    #主函数，遍历ip下载
    def muftp(self):
        for ip in self.mudata:
            print('START DOWNLOAD REMOTE DATA')
            self.__dlfromip(self.mudata[ip])
            print('REMOTE DATA DOWNLOAD SUCCESSFULLY\n')

    #建立对应IP的FTP连接，调用其他函数
    def __dlfromip(self, ip):
        with FTP(ip, 'Anonymous', 'jd1awxj', timeout=10) as ftp:
            ftp.encoding = 'GB18030'
            print(ftp.getwelcome())
            #调用其他函数，保证mudir值在下载完毕后不被修改
            temp = self.mudir
            self.__getstationame(ftp, ip)
            self.__rtwxj(ftp, 'jd1awxj')
            ftp.cwd('..')
            self.__rtmylog(ftp, 'mylogserver')
            self.mudir = temp
            ftp.quit()

    def __getstationame(self, ftp, ip):
        wxjnlst = ftp.nlst('jd1awxj')
        if wxjnlst:
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
            #返回wxj站名软件为空
            else:
                #默认名字'ABCMW001.RAR'
                wxjsoftname = 'ABCMW001.RAR'
                #生成包含站名、IP的新mudir
                self.mudir = path.join(self.mudir, wxjsoftname[0:3] + '_' + ip)
                print('NO WXJ SOFT,DEFAULT NAME ABC')
        else:
            ftp.quit()

    #遍历列表，返回以RAR为后缀的文件名
    def __searchname(self, list):
        templist = []
        for ele in list:
            ele = ele.upper()
            if ele.endswith('.RAR'):
                templist.append(ele)
        return templist

    def __rtwxj(self, ftp, dic):
        ftp.cwd(dic)
        filelist = []
        ftp.retrlines('LIST', filelist.append)
        ss = ftp.pwd().replace('/', '\\')
        makedirs(path.join(self.mudir, ss[1:]))
        for file in filelist:
            if file.startswith('d'):
                file = file[55:]
                if file == '.':
                    pass
                elif file == '..':
                    pass
                else:
                    self.__rtwxj(ftp, file)
                    ftp.cwd('..')
            elif file.startswith('-'):
                file = file[55:]
                if ss in self.swxj or ss[:-2] in self.swxj:
                    localfile = path.join(self.mudir, ss[1:], file)
                    remotefile = 'RETR ' + path.join(ss, file)
                    self.__download(ftp, localfile, remotefile)
                else:
                    newstr = self.pattern.search(file).group()
                    if newstr in self.musb or newstr in self.musc:
                        localfile = path.join(self.mudir, ss[1:], file)
                        remotefile = 'RETR ' + path.join(ss, file)
                        self.__download(ftp, localfile, remotefile)

    def __rtmylog(self, ftp, dic):
        ftp.cwd(dic)
        filelist = []
        ftp.retrlines('LIST', filelist.append)
        ss = ftp.pwd().replace('/', '\\')
        makedirs(path.join(self.mudir, ss[1:]))
        for file in filelist:
            if file.startswith('d'):
                if file[55:] == '.':
                    pass
                elif file[55:] == '..':
                    pass
                else:
                    self.__rtmylog(ftp, file[55:])
                    ftp.cwd('..')
            elif file.startswith('-'):
                file = file[55:]
                if ss in self.slog:
                    if self.pattern.search(file).group() in self.musa:
                        localfile = path.join(self.mudir, ss[1:], file)
                        remotefile = 'RETR ' + path.join(ss, file)
                        self.__download(ftp, localfile, remotefile)
                else:
                    localfile = path.join(self.mudir, ss[1:], file)
                    remotefile = 'RETR ' + path.join(ss, file)
                    self.__download(ftp, localfile, remotefile)

    #FTP下载函数，缓冲区1024，二进制方式读写,获取文件原始修改时间，并写入
    def __download(self, ftp, localfile, remotefile):
        try:
            #打开文件，下载
            with open(localfile, 'wb') as fp:
                ftp.retrbinary(remotefile, fp.write, 1024)
            #获取ftp上文件原始修改时间字符串
            m_time = ftp.sendcmd('MDTM ' + remotefile[5:])[4:]
            #字符串转为time对象
            m_time = strptime(m_time, '%Y%m%d%H%M%S')
            #返回10位时间戳
            m_time = int(mktime(m_time))
            #获取当前时间，生成10位时间戳
            a_time = int(time())
            #设置文件的访问时间和修改时间
            utime(localfile, (a_time, m_time))
            print('SUCCESS DOWNLOAD %s ' % (remotefile[4:]))
        except Exception as err:
            self.__download(ftp, localfile, remotefile)
            print(err)
            print('FAILED DOWNLOAD %s ' % (remotefile))


#MUJson类实例化并调用函数
Mujson = MUJson()
Mujson.mujson()

#MUFtp类实例化并调用函数
Muftp = MUFtp(Mujson.mudir, Mujson.mudata, Mujson.musa, Mujson.musb,
              Mujson.musc)
#MUCopy类实例化并调用函数
Mucopy = MUCopy(Mujson.mudir, Mujson.musa, Mujson.musb, Mujson.musc)

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