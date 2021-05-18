REM put this file in the same directory as scrape_prullenbakvaccin.py
:loop
python scrape_prullenbakvaccin.py
timeout /t 110
goto loop
