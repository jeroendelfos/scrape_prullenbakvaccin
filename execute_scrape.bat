REM put this file in the same directory as scrape_prullenbakvaccin.py
set arg_postalcode=%1
:loop
python scrape_prullenbakvaccin.py %arg_postalcode%
timeout /t 110
goto loop
