import datetime
import random
import time
import sys

import requests
from bs4 import BeautifulSoup

from .pisos import Pisos

MAIN_URL = "https://www.pisos.com"
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
        return random.randint(1, 5)
    elif current_hour in fast_search_range:
        return random.randint(1, 3)


# Get part of url according to buy or sell
def get_action_url(action):
    action_url = ''
    if action == "buy":
        action_url = "venta"
    elif action == "rent":
        action_url = "alquiler"
    return action_url


# Get part of url according to location
def get_location_url(city):
    location_url = "pisos-" + city.lower()
    return location_url


# Get maximum number of pages for scrapping
def get_number_of_pages(url):
    # Request HTML
    html = get_html_from_url(url)
    # Convert to soup
    soup = BeautifulSoup(html, 'html.parser')
    # Get number of pages
    pager = soup.find("div", {"class": "pager"})
    # Find all a elements
    page_numbers = pager.find_all("a")
    all_numbers = []
    for page_number in page_numbers:
        try:
            number = int(page_number.text)
            all_numbers.append(number)
        except:
            pass
    n_pages = max(all_numbers)
    # Make sure we have a number
    assert n_pages > 0
    return n_pages


# Get HTML from an URL
def get_html_from_url(url):
    r = requests.get(url)
    raw_html = r.text
    return raw_html


# Soup HTML and get a list with all ads
def get_all_ads(url):
    html = get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    # There highlighted and normal ads
    highlighted_ads = soup.find_all("div", {"class": "row destacado clearfix"})
    ads = soup.find_all("div", {"class": "row clearfix"})
    all_ads = ads + highlighted_ads
    return all_ads


# Add url snippet that accounts for the most recent flats
def get_recent_url():
    url = "/fecharecientedesde-desc/"
    return url


# Scrap
# Function to scrap Pisos.com
def scrap(city, action, pages, db):
    # Scrap webpage to get number of pages
    start_url = MAIN_URL + "/en/" + get_action_url(action) + "/" + get_location_url(city) + get_recent_url()
    # Assign number of pages
    start_page = pages[0]
    last_page = pages[1]
    n_pages = min(get_number_of_pages(start_url), last_page)
    # Start scrapping
    for page in range(start_page, n_pages+1):
        print("Current page:", page)
        # Get ads from url + page
        url = start_url + "/" + str(page)
        all_ads = get_all_ads(url)
        for ad in all_ads:
            print(ad)
            ad_url_snippet = ad['data-navigate-ref']
            ad_url = MAIN_URL + ad_url_snippet
            if not db.is_url_in_database(TABLE_NAME, ad_url):
                html = get_html_from_url(ad_url)
                pisos = Pisos(html, ad_url)
                # Print results
                log_results(pisos)
                # Add to database
                db.insert_object_into_table(TABLE_NAME, pisos)
                sleep_time = get_sleep_time()
                time.sleep(sleep_time)
            #else:
             #   sys.exit("Success: Synchronized.")


