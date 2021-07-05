#!/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import subprocess


#字符串处理
def fun(str):
    #非空str以\n结尾，去除
    if str is not '':
        if str[-1:] is '\n':
            str = str[:-1]
    #非空str去除中间' '和'.'
    if str is not '':
        if str.find(' .') < str.find('. '):
            str = str[:str.find(' .')] + str[str.find(' :'):]
        else:
            str = str[:str.find('. ')] + str[str.find(' :'):]
    #非空str去除首尾空格
    if str is not '':
        str = str.strip()
    return str


#将不同网卡分离成多个子列表
def fun1(iplist):
    #长度>3
    if len(iplist) > 3:
        #判断
        if iplist[iplist.index('')] == iplist[iplist.index('') + 2]:
            if iplist[iplist.index('') + 3] is '':
                #去空元素
                templist = iplist[0:3]
                while '' in templist:
                    templist.remove('')
                #添加元素至newlist
                newlist.append(templist)
                #截取iplist
                iplist = iplist[3:]
                #递归
                fun1(iplist)

            else:
                i = 3
                #寻找下一个空元素
                while iplist[iplist.index('') + i] is not '':
                    i += 1
                    if i + 1 > len(iplist):
                        break
                #去空元素
                templist = iplist[:i]
                while '' in templist:
                    templist.remove('')
                #添加元素至newlist
                newlist.append(templist)
                #截取iplist
                iplist = iplist[i:]
                #递归
                fun1(iplist)


def fun2(newlist):
    #有序字典
    dic = OrderedDict()
    #去除空格，以:将字符串分离成字典键值对，添加进新列表
    for ele in newlist:
        if ':' in ele:
            if ele[-1] is ':':
                dic.update({'%s' % (ele[:-1].strip()): ''})
            else:
                n = ele.index(':')
                dic.update(
                    {'%s' % (ele[:n].strip()): '%s' % (ele[n + 1:].strip())})
        else:
            dic.update({'%s' % (ele.strip()): ''})
    ipdic.append(dic)


#生成三个列表
iplist = []
newlist = []
ipdic = []

#解析命令ipconfig，写入analysis_ipconfig.txt
output = subprocess.check_output(
    "ipconfig",
    shell=True,
)
with open('analysis_ipconfig.txt', 'wb') as f:
    f.write(output)
#读取文件analysis_ipconfig.txt
file = open('analysis_ipconfig.txt', 'r', encoding='gbk')

#读文件
try:
    while True:
        text_line = file.readline()
        if text_line:
            #处理字符串，添加到列表
            text_line = fun(text_line)
            iplist.append(text_line)
        else:
            break
finally:
    file.close()

#将不同网卡分离成多个子列表
iplist = fun1(iplist)

#生成字典
for ele in newlist:
    fun2(ele)
#写文件
with open('analysis_ipconfig.txt', 'w', encoding='utf-8') as f:
    f.write(str(ipdic))