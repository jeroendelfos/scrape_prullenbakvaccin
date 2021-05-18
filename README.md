# scrape_prullenbakvaccin
Python file uses selenium to scrape https://prullenbakvaccin.nl/. User needs to specify her postal code in the python script. Batch file runs the python file every 110 seconds. With a runtime of approximately 10 seconds, an update should be given every two minutes. 

To run the batchfile, making the python script run repeatedly:
`execute_scrape.bat "1234AB"`

To run the python script once:
`python scrape_prullenbakvaccin.py "1234AB"`
