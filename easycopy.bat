@ECHO off
CLS
COLOR 7D

ECHO.
ECHO EasyCopy V0.1 by Aki 2020.07.17
ECHO.

SET SavePath=C:\WXJDATA\
SET WxjPath=E:\JD1AWXJ\
SET TempPath=C:\Users\Aki-Pc\Desktop\jd1awxJ\

ECHO Type Enter To Start Copy Data
SET /p Time=
ECHO Please Type The SavePath(Such As D:\ABC\,or Blank Means D:\WXJDATA\)
SET /p SavePath=

:JUDGE
ECHO %SavePath% Already Exists, y:Copying Data;n:Compress Data? y/n
SET /p ans=
IF NOT %ans%==y GOTO COMPRESS
ECHO Please Type Time(Such As 7_09,11_23)
SET /p Time=

:COPYING
ECHO "Copying Now"
ECHO %TempPath%
XCOPY %TempPath%*.rar %SavePath% /d /y
XCOPY %TempPath%replays\replay%Time%.* %SavePath%\replays\ /s /e /d /y
XCOPY %TempPath%alarms\alm%Time%.* %SavePath%\alarms\ /s /e /d /y
XCOPY %TempPath%button\btn%Time%.* %SavePath%\button\ /s /e /d /y
XCOPY %TempPath%errors\err%Time%.* %SavePath%\errors\ /s /e /d /y
XCOPY %TempPath%sysinfo\sys*%Time%.txt %SavePath%\sysinfo\ /s /e /d /y
IF EXIST %SavePath%replays\replay%Time%.* GOTO JUDGE ELSE GOTO NODATA

:NODATA
ECHO No Data For This Date
GOTO JUDGE

:COMPRESS
echo Type Enter To Start Unpack
SET /p Unpack=
start winrar x -r -ikbc -inul %SavePath%*mw*.rar *.* %SavePath%

ECHO Type Enter To Continue
SET /p Continue=
start winrar m -r -agYYYYMMDD-NN -ep1 -inul %SavePath%%Time%__.rar %SavePath%\*

ECHO Type Enter To Complete

PAUSE
@ECHO ON