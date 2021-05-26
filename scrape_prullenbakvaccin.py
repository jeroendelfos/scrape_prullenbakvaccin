import sys
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import winsound
import schedule

def scrape_url(url, postal_code):
    # Open firefox
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    with driver:
        driver.get(url)
    time.sleep(10)

    # Go to nearest locations
    pc = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/form/input[2]")
    for i in postal_code:
        pc.send_keys(i)
    pc.send_keys(Keys.RETURN)

    time.sleep(1)

    # Get information from page
    locs = driver.find_elements_by_class_name("card-body")
    n = 0
    for loc in locs:
        n += 1
        print("\rChecking location [{}/{}]".format(n, len(locs)), end="")
        if "Heeft geen vaccins" not in loc.text:
            driver.get("https://api.telegram.org/botXXXXXXX/sendmessage?chat_id=XXXXXXXX&text=VaccineAvailable!")
			
    driver.quit()
if __name__ == "__main__":
    # Settings for browsing and notifications
	
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-plugins-discovery")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--disable-blink-features=AutomationControlled")
    #options.headless=True
    #options.add_argument('--headless')
    # Global vars
	
    url = "https://prullenbakvaccin.nl"
    try: 
        postal_code = sys.argv[1]
    except IndexError:
        print("""ERROR: Enter postal code after python/batch run command like "1234AX".""")
        sys.exit(1)
    scrape_url(url, postal_code)
