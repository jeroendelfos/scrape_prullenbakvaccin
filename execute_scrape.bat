@echo off

if "%~1"=="" (
    goto end
) else (
    goto loop
)

:loop
python scrape_prullenbakvaccin.py %1%
timeout /t 110
goto loop

:end
echo Error: You did not pass a postal code. Use 'execute_scrape.bat "1234AX"'
exit /B 1
