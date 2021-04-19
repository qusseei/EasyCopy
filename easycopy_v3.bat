@echo off
cls

echo.
echo easycopy v0.3 by aki 2021.4.19
echo.
echo Welcome To Try EasyCopy
echo Copy The Data First,Then Compress
echo.

echo Type Enter To Created Save Path
set /p Typestart=

set wxjpath=E:\JD1AWXJ\
set mylogserverpath=E:\MYLOGSERVER\
setlocal enabledelayedexpansion
for %%i in (%wxjpath%*.rar) do (set "stationame=%%~nxi")
set abbreviation=%stationame:~0,3%
set thisday=%date:~0,4%%date:~5,2%%date:~8,2%
set current_directory=%~dp0
set savepath=%currentdirectory%%abbreviation%%thisday%\
if not exist %savepath% ( md %savepath% ) else (rd /s /q %savepath% && md %savepath% )
echo %current_directory%%savepath% Has Been Created

:judge
echo 
echo y:Copying Data;n:Compress Data? y/n
set /p typechoice=
if not %typechoice%==y goto compress

echo Year (Such As 2020,2021)
set /p year=
echo Month(Such As 08,09,10,11)
set /p month=
echo Day(Such As 08,09,10,11)
set /p day=
set typetime=%month:~-1%_%day%
set typetime1=%year%-%month%-%day%

:copying
echo "Copying Now"
echo %wxjpath%
xcopy %wxjpath%*.rar %savepath%JD1AWXJ\ /d /y
xcopy %wxjpath%replays\replay%typetime%.* %savepath%JD1AWXJ\replays\ /s /e /d /y
xcopy %wxjpath%alarms\alm%typetime%.* %savepath%JD1AWXJ\alarms\ /s /e /d /y
xcopy %wxjpath%button\btn%typetime%.* %savepath%JD1AWXJ\button\ /s /e /d /y
xcopy %wxjpath%errors\err%typetime%.* %savepath%JD1AWXJ\errors\ /s /e /d /y
xcopy %wxjpath%sysinfo\sys*%typetime%.txt %savepath%JD1AWXJ\sysinfo\ /s /e /d /y

echo %mylogserverpath%
xcopy %mylogserverpath%*LOG*.rar %savepath%MYLOGSERVER\ /d /y
xcopy %mylogserverpath%Data\*%typetime1%.* %savepath%MYLOGSERVER\Data\ /s /e /d /y
xcopy %mylogserverpath%Log\*%typetime1%.* %savepath%MYLOGSERVER\Log\ /s /e /d /y

if exist %savepath%replays\replay%typetime%.* goto judge else goto nodata

:nodata
echo No Data For savepath
goto judge

:compress
echo Type Enter To Start Unpack
set /p unpack=
start winrar x -y -r- -ikbc -inul %savepath%JD1AWXJ\*MW*.rar *.* %savepath%JD1AWXJ\
start winrar x -y -r- -ikbc -inul %savepath%MYLOGSERVER\*LOG*.rar *.* %savepath%MYLOGSERVER\

echo Type Enter To Create Compressed Package
set /p continue=
start winrar m -y -r -ep1 -inul %savepath%JD1AWXJ-%year%%month%%day%.rar %savepath%JD1AWXJ\*
start winrar m -y -r -ep1 -inul %savepath%MYLOGSERVER-%year%%month%%day%.rar %savepath%MYLOGSERVER\*

echo Wait To Complete

pause

if exist %savepath%JD1AWXJ\ ( rd /s /q %savepath%JD1AWXJ\ ) else (echo  )
if exist %savepath%MYLOGSERVER\ ( rd /s /q %savepath%MYLOGSERVER\ ) else (echo  )

@echo on

