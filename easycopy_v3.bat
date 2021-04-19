@echo off
cls
color 7d
echo.
echo easycopy v0.2 by aki 2020.09.11
echo.
echo.
echo Welcome To Try EasyCopy
echo Copy The Data First,Then Compress
echo.

echo Type Enter To Created Save Path
set /p Typestart=

set wxjpath=E:\JD1AWXJ\
setlocal enabledelayedexpansion
for %%i in (%wxjpath%*.rar) do (set "stationame=%%~nxi")
set abbreviation=%stationame:~0,3%
set thisday=%date:~0,4%%date:~5,2%%date:~8,2%
set string1=E:\
set string2=\
set thisday=%string1%%abbreviation%%thisday%%string2%
if not exist %thisday% ( md %thisday% ) else (rd /s /q %thisday% && md %thisday% )
echo %thisday% Has Been Created

:judge
echo y:Copying Data;n:Compress Data? y/n
set /p typechoice=
if not %typechoice%==y goto compress
echo Type Date(Such As 7_09,11_23)
set /p typetime=

:copying
echo "Copying Now"
echo %wxjpath%
xcopy %wxjpath%*.rar %thisday% /d /y
xcopy %wxjpath%replays\replay%typetime%.* %thisday%\replays\ /s /e /d /y
xcopy %wxjpath%alarms\alm%typetime%.* %thisday%\alarms\ /s /e /d /y
xcopy %wxjpath%button\btn%typetime%.* %thisday%\button\ /s /e /d /y
xcopy %wxjpath%errors\err%typetime%.* %thisday%\errors\ /s /e /d /y
xcopy %wxjpath%sysinfo\sys*%typetime%.txt %thisday%\sysinfo\ /s /e /d /y
if exist %thisday%replays\replay%typetime%.* goto judge else goto nodata

:nodata
echo No Data For Thisday
goto judge

:compress
echo Type Enter To Start Unpack
set /p unpack=
start winrar x -r -ikbc -inul %thisday%*mw*.rar *.* %thisday%

echo Type Enter To Create Compressed Package
set /p continue=
start winrar m -r -agyyyymmdd-nn -ep1 -inul %thisday%%typetime%__.rar %thisday%\*

echo Wait To Complete

pause
@echo on