@echo off

REM check if argument is passed
if "%~1"=="" (
	echo Error: You did not pass a postal code. Use 'execute_scrape.bat "1234AX"'
	goto end
) else (
    	goto filecheck
)

REM check if file exists
:filecheck
if exist "scrape_prullenbakvaccin.py" (
	goto loop
) else (
	echo Error: scrape_prullenbakvaccin.py not found. Place batch file in same directory as python file
	goto end

REM execute script until manual exit
:loop
python scrape_prullenbakvaccin.py %1%
timeout /t 110
goto loop

REM exit program after error
:end
exit /B 1
