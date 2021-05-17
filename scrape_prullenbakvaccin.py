from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import requests
import time
import winsound
from win10toast import ToastNotifier
import schedule

def scrape_url(url, postal_code):
    # Open firefox
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Go to nearest locations
    pc = driver.find_element_by_xpath(
                    "/html/body/main/div[2]/div[1]/form/input[2]")
    pc.send_keys(postal_code)
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
    options = Options()
    options.headless = True
    toaster = ToastNotifier()

    # Global vars
    url = "https://prullenbakvaccin.nl"
    postal_code = None

    scrape_url(url, postal_code)
