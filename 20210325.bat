@echo off
cls
echo easycopy v0.4 by aki 20210516
echo

set wxjpath=E:\JD1AWXJ\
set mylogserverpath=E:\MYLOGSERVER\

rem 定义维修机日志路径

setlocal enabledelayedexpansion
for %%i in (%wxjpath%*.rar) do (set "stationame=%%~nxi")
set abbreviation=%stationame:~0,3%
rem 获取站名简写
set thisday=%date:~0,4%%date:~5,2%%date:~8,2%
rem 获取即时日期
set currentdirectory=%~dp0
rem 获取当前目录
for %%i in (%currentdirectory%*.bat) do (set "copydata=%%~nxi")
rem 获取需要拷贝的数据日期
set year=%copydata:~0,4%
set month=%copydata:~4,2%
set day=%copydata:~6,2%
echo %year%,%month%,%day%
rem 解析为年月日
if %month:~0,1% EQU 0 (set wxjtime=%month:~-1%_%day%) else (set wxjtime=%month%_%day%)
set mylogservertime=%year%-%month%-%day%
rem 构造维修机和日志程序格式
set savepath=%currentdirectory%%abbreviation%%thisday%\
if not exist %savepath% ( md %savepath% ) else (rd /s /q %savepath% && md %savepath% )
echo %savepath% Has Been Created
rem 设置并新建文件保存路径

%currentdirectory%xcopy.exe %wxjpath%*.rar %savepath%JD1AWXJ\ /d /y
%currentdirectory%xcopy.exe %wxjpath%replays\replay%wxjtime%.* %savepath%JD1AWXJ\replays\ /s /e /d /y
%currentdirectory%xcopy.exe %wxjpath%alarms\alm%wxjtime%.* %savepath%JD1AWXJ\alarms\ /s /e /d /y
%currentdirectory%xcopy.exe %wxjpath%button\btn%wxjtime%.* %savepath%JD1AWXJ\button\ /s /e /d /y
%currentdirectory%xcopy.exe %wxjpath%errors\err%wxjtime%.* %savepath%JD1AWXJ\errors\ /s /e /d /y
%currentdirectory%xcopy.exe %wxjpath%sysinfo\sys*%wxjtime%.txt %savepath%JD1AWXJ\sysinfo\ /s /e /d /y
rem 拷贝维修机数据

echo %mylogserverpath%
%currentdirectory%xcopy.exe %mylogserverpath%*LOG*.rar %savepath%MYLOGSERVER\ /d /y
%currentdirectory%xcopy.exe %mylogserverpath%Data\*%mylogservertime%.* %savepath%MYLOGSERVER\Data\ /s /e /d /y
%currentdirectory%xcopy.exe %mylogserverpath%Log\*%mylogservertime%.* %savepath%MYLOGSERVER\Log\ /s /e /d /y
rem 拷贝日志数据

if exist %savepath%JD1AWXJ\replays\replay%wxjtime%.* ( echo success ) else ( echo no data)
rem 判断是否拷贝成功

start winrar x -y -r- -ikbc -inul %savepath%JD1AWXJ\*MW*.rar *.* %savepath%JD1AWXJ\
start winrar x -y -r- -ikbc -inul %savepath%MYLOGSERVER\*LOG*.rar *.* %savepath%MYLOGSERVER\
rem 解压程序
start winrar m -y -r -ep1 -inul %savepath%JD1AWXJ-%year%%month%%day%.rar %savepath%JD1AWXJ\*
start winrar m -y -r -ep1 -inul %savepath%MYLOGSERVER-%year%%month%%day%.rar %savepath%MYLOGSERVER\*
rem 压缩程序
echo Wait To Complete

pause
echo Wait To Clear Temp file
if exist %savepath%JD1AWXJ\ ( rd /s /q %savepath%JD1AWXJ\ ) else (echo  )
if exist %savepath%MYLOGSERVER\ ( rd /s /q %savepath%MYLOGSERVER\ ) else (echo  )
rem 删除多余目录
pause