import sys
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import winsound
from win10toast import ToastNotifier
import schedule

def scrape_url(url, postal_code):
    # Open firefox
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get(url)

    # Go to nearest locations
    pc = driver.find_element_by_xpath(
                    "/html/body/main/div[2]/div[1]/form/input[2]")
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
            print("ER IS EEN VACCIN BESCHIKBAAR: \n{}".format(loc.text))
            toaster.show_toast("PrullenbakVaccin", 
                                "Er is een vaccin beschikbaar!")
            winsound.Beep(1500, 5000)

if __name__ == "__main__":
    # Settings for browsing and notifications
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.headless = True
    toaster = ToastNotifier()

    # Global vars
    url = "https://prullenbakvaccin.nl"
    try: 
        postal_code = sys.argv[1]
    except IndexError:
        print("""ERROR: Enter postal code after python/batch run command like "1234AX".""")
        sys.exit(1)

    scrape_url(url, postal_code)
