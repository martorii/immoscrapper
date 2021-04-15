import datetime
import random
import time
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup

from .fotocasa import Fotocasa

MAIN_URL = "https://www.fotocasa.es"
TABLE_NAME = "properties"


# Print all attributes from a class
def log_results(obj):
    attrs = vars(obj)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    return


def get_sleep_time():
    slow_search_range = range(9, 23)
    fast_search_range = range(0, 9)
    current_hour = datetime.datetime.now().hour
    if current_hour in slow_search_range:
        return random.randint(4, 8)
    elif current_hour in fast_search_range:
        return random.randint(1, 4)


# Get part of url according to buy or sell
def get_action_url(action):
    action_url = ''
    if action == "buy":
        action_url = "buy"
    elif action == "rent":
        action_url = "rental"
    return action_url


# Get part of url according to location
def get_location_url(city):
    # Check on www.fotocasa.es/en and insert url here
    if city == "Barcelona":
        location_url = "homes/barcelona-province/all-zones/l/<page>?combinedLocationIds=724,9,8,0,0,0,0,0,0"
    else:
        print("City not valid. Insert link into code.")
        exit(1)
    return location_url


# Get maximum number of pages for scrapping
def get_number_of_pages(url):
    n_pages = 3000
    return n_pages


# Get HTML from an URL
def get_html_from_url(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    raw_html = r.text
    return raw_html


# Go to the bottom to load all rows
def scroll_to_bottom(browser):
    elem = browser.find_element_by_tag_name("body")
    page_downs = 20
    while page_downs:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        page_downs -= 1
    return


# Soup HTML and get a list with all ads
def get_all_ads(url):
    # Start browser
    browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
    # Scroll down to get all ads
    browser.get(url)
    # Wait for pop-up to appear
    time.sleep(5)
    # Accept terms
    browser.find_element_by_xpath('//button[@data-testid="TcfAccept"]').click()
    # Wait until page loads
    time.sleep(3)
    # Go to the end of the page to load all rows
    scroll_to_bottom(browser)
    # Get ads from webpage
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find_all("article", {"div": "re-Card-primary"})
    print(ads[0])
    return ads


# Replace placeholder with page on the url
def add_page_to_url(url, page):
    url = url.replace("<page>", str(page))
    return url


# Scrap
# Function to scrap Pisos.com
def scrap(city, action, pages, db):
    # Scrap webpage to get number of pages
    start_url = MAIN_URL + "/en/" + get_action_url(action) + "/" + get_location_url(city)
    # Assign number of pages
    start_page = pages[0]
    last_page = pages[1]
    n_pages = min(get_number_of_pages(start_url), last_page)
    # Start scrapping
    for page in range(start_page, n_pages + 1):
        print("Current page:", page)
        # Get ads from url + page
        url = add_page_to_url(start_url, page)
        all_ads = get_all_ads(url)
        for ad in all_ads:
            ad_url = ad.find('a')['href']
            print(ad_url)
            exit(8)
            if not db.is_url_in_database(TABLE_NAME, ad_url):
                html = get_html_from_url(ad_url)
                print(html)
                fotocasa = Fotocasa(html, ad_url)
                # Print results
                log_results(pisos)
                # Add to database
                db.insert_object_into_table(TABLE_NAME, pisos)
                sleep_time = get_sleep_time()
                print(f"Wait for {sleep_time} sec.")
                time.sleep(sleep_time)
