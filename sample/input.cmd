

SET VARIABLE1=%~dp0
IF "%VARIABLE1:~-1%" == "\" SET VARIABLE1=%VARIABLE1:~0,-1%


IF "%FLG%" == "1" (
    SET MYDIR=%SHARE_DIR_ROOT%\path\to\dir
) else (
    REM noop
)

IF NOT EXIST c:\path\to\my.exe set flag=true
if not exist "d:\path\to\Program Files\my.exe" set flag=true


call %BIN_PATH%\MyProcess.cmd
call %BIN_PATH%\MyProcess2.cmd %_MyVariable% 1234

FOR /F "delims= " %%i IN ('DATE /T') DO SET YMD=%%i
FOR /F "tokens=1*" %%i IN ('MyCommand.exe') DO CALL :SUBROUTINE %%i %%j %%k %%l %%m %%n
for /f %%p in (%FILEPATH%) do CALL :SUBROUTINE %%p

FOR /F "delims= " %%i IN ("1 2 3") DO (
    FOR /F "delims= " %%i IN ("4 5 6") DO (
        echo %%i %%j
    )
)

FOR /F "delims= " %%i IN ("1 2 3") DO FOR /F "delims= " %%i IN ("4 5 6") DO echo %%i %%j


ECHO ---------- TEST TEXT ----------
ECHO ---------- TEST TEXT ---------- >> %OUTPUT_LOG%

echo 123 && echo 456 || echo 789

echo aaa | echo bbb

