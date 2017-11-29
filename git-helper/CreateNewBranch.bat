::Script which create new branch and overwrite the origin partner file with customized one

::IF WANT TO GET Version from user
::@echo off
::set /p id=Enter ID: 
::echo %id%
::GOTO:ENDVER

ECHO OFF

::spliting the version number
For /F "tokens=1,2,3 delims=." %%G IN (branch.txt) do SET id1=%%G
For /F "tokens=1,2,3 delims=." %%G IN (branch.txt) do SET id2=%%H
For /F "tokens=1,2,3 delims=." %%G IN (branch.txt) do SET id3=%%I

::Increase the version number in 1
SET /A "id3=id3+1"
IF %id3% GTR 9 SET /A "id3=0"
IF %id3% EQU 0 SET /A "id2=id2+1"
IF %id2% GTR 9 SET /A "id3=id3+1"

SET "id=%id1%.%id2%.%id3%"
:ENDVER

echo Version number:  %id%

::Saving number in text file for next branch version
echo %id% > branch.txt
"C:\Program Files (x86)\Git\bin\git.exe" reset --hard
"C:\Program Files (x86)\Git\bin\git.exe" checkout master
"C:\Program Files (x86)\Git\bin\git.exe" pull origin master
"C:\Program Files (x86)\Git\bin\git.exe" checkout -b KmsGoOleg-%id%

:end
Pause