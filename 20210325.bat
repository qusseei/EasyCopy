@echo off
cls
echo easycopy v0.4 by aki 20210426
echo

set wxjpath=E:\JD1AWXJ\
set mylogserverpath=E:\MYLOGSERVER\
setlocal enabledelayedexpansion
for %%i in (%wxjpath%*.rar) do (set "stationame=%%~nxi")
set abbreviation=%stationame:~0,3%
set thisday=%date:~0,4%%date:~5,2%%date:~8,2%
set currentdirectory=%~dp0
for %%i in (%currentdirectory%*.bat) do (set "copydata=%%~nxi")
set year=%copydata:~0,4%
set month=%copydata:~4,2%
set day=%copydata:~6,2%
echo %year%,%month%,%day%
set wxjtime=%month:~-1%_%day%
set mylogservertime=%year%-%month%-%day%

set savepath=%currentdirectory%%abbreviation%%thisday%\
if not exist %savepath% ( md %savepath% ) else (rd /s /q %savepath% && md %savepath% )
echo %currentdirectory%%savepath% Has Been Created

xcopy %wxjpath%*.rar %savepath%JD1AWXJ\ /d /y
xcopy %wxjpath%replays\replay%wxjtime%.* %savepath%JD1AWXJ\replays\ /s /e /d /y
xcopy %wxjpath%alarms\alm%wxjtime%.* %savepath%JD1AWXJ\alarms\ /s /e /d /y
xcopy %wxjpath%button\btn%wxjtime%.* %savepath%JD1AWXJ\button\ /s /e /d /y
xcopy %wxjpath%errors\err%wxjtime%.* %savepath%JD1AWXJ\errors\ /s /e /d /y
xcopy %wxjpath%sysinfo\sys*%wxjtime%.txt %savepath%JD1AWXJ\sysinfo\ /s /e /d /y

echo %mylogserverpath%
xcopy %mylogserverpath%*LOG*.rar %savepath%MYLOGSERVER\ /d /y
xcopy %mylogserverpath%Data\*%mylogservertime%.* %savepath%MYLOGSERVER\Data\ /s /e /d /y
xcopy %mylogserverpath%Log\*%mylogservertime%.* %savepath%MYLOGSERVER\Log\ /s /e /d /y

if exist %savepath%JD1AWXJ\replays\replay%wxjtime%.* ( echo success ) else ( echo no data) 

start winrar x -y -r- -ikbc -inul %savepath%JD1AWXJ\*MW*.rar *.* %savepath%JD1AWXJ\
start winrar x -y -r- -ikbc -inul %savepath%MYLOGSERVER\*LOG*.rar *.* %savepath%MYLOGSERVER\

start winrar m -y -r -ep1 -inul %savepath%JD1AWXJ-%year%%month%%day%.rar %savepath%JD1AWXJ\*
start winrar m -y -r -ep1 -inul %savepath%MYLOGSERVER-%year%%month%%day%.rar %savepath%MYLOGSERVER\*

echo Wait To Complete

pause

if exist %savepath%JD1AWXJ\ ( rd /s /q %savepath%JD1AWXJ\ ) else (echo  )
if exist %savepath%MYLOGSERVER\ ( rd /s /q %savepath%MYLOGSERVER\ ) else (echo  )

pause