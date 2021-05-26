import sys
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import winsound
from win10toast import ToastNotifier
import schedule
import re



def cloudflare_check(driver):
    try:
        driver.find_element_by_xpath("//meta[@name='robots']")
    except NoSuchElementException:
        return False
    return True


def scrape_url(url, postal_code):
    # Open firefox
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    user_agent = driver.execute_script("return navigator.userAgent;")
    new_user_agent = user_agent.replace("Headless", "")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_user_agent})
    with driver:
        driver.get(url)

    wait_time = 0
    while cloudflare_check(driver) == True:
        print("Hitting cloudflare, waiting for access to url [{}/60]".format(
                                                            wait_time), end="\r")
        if wait_time == 59:
            print("\nCouldn't pass Cloudflare. Aborting...")
            sys.exit()
        else:
            wait_time += 1
            time.sleep(1)

    driver.minimize_window()

    # Go to nearest locations
    pc = driver.find_element_by_xpath(
                    "/html/body/main/div[2]/div[1]/form/input[2]")
    pc.send_keys(postal_code)
    pc.send_keys(Keys.RETURN)

    # Make sure the full page has loaded
    time.sleep(1)

    # Scrape for 24 hours, abort with CTRL-C
    for i in range(1440):
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

        # Get timestamp of refresh
        timestamp_string = driver.find_element_by_xpath("//*[@id=\"locations\"]/p")
        pattern = "\d\d:\d\d:\d\d"
        timestamp = re.findall(pattern, timestamp_string.text)[0]
        print("\tLast refresh at ", timestamp, "\tabort with CTRL-C", end="")

        # Wait for next refresh
        time.sleep(60)
        continue


if __name__ == "__main__":
    # Settings for browsing and notifications
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    #options.headless = True
    toaster = ToastNotifier()

    # Global vars
    url = "https://prullenbakvaccin.nl"
    try: 
        postal_code = sys.argv[1]
    except IndexError:
        print("""ERROR: Enter postal code after python/batch run command like "1234AX".""")
        sys.exit(1)

    scrape_url(url, postal_code)
