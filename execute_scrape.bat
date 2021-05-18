@echo off

REM put this file in the same directory as scrape_prullenbakvaccin.py

set arg_postalcode=%1
if [%1]==[] goto loop
@echo Error: You did not pass a postal code. Use 'execute_scrape.bat "1234AX"'
goto EOF

:loop
python scrape_prullenbakvaccin.py %arg_postalcode%
timeout /t 110
goto loop

exit /B 1
