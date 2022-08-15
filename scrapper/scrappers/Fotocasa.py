from .Scrapper import Scrapper, log_warning_if_returns_none
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import tqdm

import logging


class Fotocasa(Scrapper):
    """
    Define class to scrap a Fotocasa property
    """
    def __init__(self, mode, city):
        super().__init__(mode, city)
        # Define child properties
        self.name = 'fotocasa'
        self.main_url = 'https://www.fotocasa.es'
        # Define dictionary to map data to fields
        self.mapping_dict = {
            "Built-up area": "built_up_area",
            "Useable floor area": "usable_floor_area",
            "bdrm.": "n_rooms",
            "Energy consumption": "energy_certificate",
            "bathroom": "n_bathrooms",
            "sqm": "floor_area",
            "Flooring": 'flooring',
            "Floor area": "floor_area",
            "Floor": "floor",
            "Antiquity": "antiquity",
            "Status": "condition",
            "Heating": "heating",
            "Fully equipped kitchen": "equipped_kitchen",
            "Elevator": "lift",
            "Air Conditioning": "air_conditioning",
            "Parking": "garage",
            "Balcony": "own_balcony",
            "Terrace": "terrace",
            "Security Door": "security_system",
            "Orientation": "facing",
            "Swimming pool": "swimming_pool",
            "Garden": "garden"
        }
        # Get URL depending on action and city
        self.url = self.main_url + "/en/" + get_mode_url(self.mode) + "/" + get_location_url(self.city)
        # Add portal to data dictionary
        self.data['portal'] = 'fotocasa'

    def get_all_ads(self, url):
        """
        Given the main website, return all the ads as list
        :param url: url to scrap
        :return: list of ads
        """
        page_downs = 30
        # Start browser
        browser = self.start_browser()
        # Scroll down to get all ads
        browser.get(url)
        time.sleep(2)
        # Wait for pop-up to appear and accept terms
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-testid="TcfAccept"]'))
        ).click()
        # Wait until page loads
        time.sleep(1)
        # Go to the end of the page to load all rows
        self.scroll_to_bottom(browser, page_downs)
        # Get ads from webpage
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ads = soup.find_all("article", {"class": "re-CardPackPremium"})
        # Close browser
        browser.close()
        return ads

    def get_html_from_url_scrolling_to_bottom(self, url):
        """
        It returns the whole html after scrolling down to the bottom
        :param url: url to scrap
        :return: html as string
        """
        page_downs = 10
        # Wait for pop-up to appear and accept terms
        n_trials = 0
        max_n_trials = 3
        while n_trials <= max_n_trials:
            try:
                # Start browser
                browser = self.start_browser()
                # Scroll down to get all ads
                browser.get(url)
                time.sleep(2)
                # Click on accept
                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="TcfAccept"]'))
                ).click()
                break
            except:
                n_trials += 1
        # Return empty if number of trials exceeded
        if n_trials > max_n_trials:
            return ""
        # Wait until page loads
        time.sleep(1)
        # Go to the end of the page to load all rows
        self.scroll_to_bottom(browser, page_downs)
        # Get ads from webpage
        html = browser.page_source
        return html

    def sanity_check(self):
        """
        Check if we could extract the title
        :return:
        """
        return True if self.data.get('title', None) else False

    def extract_data(self, ad_url):
        # Extract html from the given URL
        html = self.get_html_from_url_scrolling_to_bottom(ad_url)
        # Continue only with successful html
        if len(html) > 0:
            soup = BeautifulSoup(html, 'html.parser')
            # Store the easy fields in the dictionary
            self.data['url'] = ad_url
            self.data['price'] = get_price(soup)
            self.data['location'] = get_location(soup)
            self.data['title'] = get_title(soup)
            # Store the difficult fields in the dictionary
            # Get all features from the first box (some of them are missing depending on the flat)
            features_data = soup.find_all("li", {"class": "re-DetailHeader-featuresItem"})
            # Get all features from the bullet points
            extra_data = soup.find_all('div', {'class': 're-DetailFeaturesList-featureContent'})
            # Get info from the tags below
            extra_tags = soup.find_all("li", {"class": "re-DetailExtras-listItem"})
            # Concatenate
            all_features = features_data + extra_data + extra_tags
            # Get a copy of the mapping_dict
            mapping_dict = self.mapping_dict.copy()
            for attribute in all_features:
                # Get all text from attribute
                text = attribute.text
                # Set match to see if we could find an attribute that matched the text
                match = False
                for key in mapping_dict:
                    if key in text:
                        # Convert raw text to a value
                        value = get_value_from_raw_text(key, text)
                        # Store in dictionary
                        self.data[mapping_dict[key]] = value
                        # Set match to true to delete the entry from dictionary
                        match = True
                        break
                if match:
                    # Delete entry from dictionary
                    mapping_dict.pop(key)
        return

    def sanity_check(self):
        """
        Check if the property has a title
        :return:
        """
        return True if len(self.data['title']) > 0 else False

    def scrap(self, pages, db):
        """
        Given the url extract all the required fields and store them in the class
        :param pages: first and last page as a list [1, 10]
        :param db: database connector
        """
        # Assign number of pages
        start_page, last_page = pages
        # Iterate over pages
        for page in range(start_page, last_page + 1):
            logging.info(f"Scrapping page {page}")
            # Replace placeholder with page
            url = add_page_to_url(self.url, page)
            # For this page, get all ads
            all_ads = self.get_all_ads(url)
            # Iterate over all ads
            for ad in tqdm.tqdm(all_ads):
                # Assign ad url
                self.data['url'] = self.main_url + ad.find('a')['href']
                # Update database
                self.update_db(db)


def get_mode_url(mode):
    assert mode in ['buy', 'rent']
    mode_url_dict = {
        'buy': 'buy',
        'rent': 'rental'
    }
    return mode_url_dict[mode]


def get_location_url(city):
    # Check on www.fotocasa.es/en and insert url here
    if city == "barcelona":
        return "homes/barcelona-province/all-zones/l/<page>"
    else:
        logging.error("City not valid. Insert link into code.")
        exit(1)
    return ""


def add_page_to_url(url, page):
    url = url.replace("<page>", str(page))
    return url


@log_warning_if_returns_none
def get_value_from_raw_text(attr, text):
    """
    Look for the attr in the text
    :param attr: field to search for
    :param text: text to searh in
    :return: value of the ifeld found in text
    """
    try:
        if attr == "Energy consumption":
            value = text.replace(attr, "")[0]
        elif attr in ["Parking"]:
            value = 1
        elif attr in ["Antiquity", "Status", "Heating", "Orientation"]:
            value = text.replace(attr, "")
            if attr == "Heating" and value == '':
                value = 'Yes'
        elif attr == "Floor":
            zero_floor_list = ['Ground', 'Main floor', 'Mezzanine', 'Basement', 'Subbasement']
            if any(zero_floor in text for zero_floor in zero_floor_list):
                value = 0
            else:
                value = re.sub(r"[^0-9]", "", text)
        elif attr in ["sqm", "bathroom", "bdrm.", "Parking"]:
            value = re.sub(r"[^0-9]", "", text)
            if (attr in "bathroom") and (value == ''):
                value = None
            elif attr == "Parking" and value == '':
                value = 1
        elif attr in ["Air Conditioning", "Garden", "Swimming pool"]:
            value = "Yes"
        elif attr in ["Terrace", "Balcony", "Fully equipped kitchen", "Security Door", "Elevator"]:
            value = 1
    except:
        value = None
    return value


@log_warning_if_returns_none
def get_price(soup):
    try:
        price = soup.find("span", {"class": "re-DetailHeader-price"}).text
        # Remove currency and .
        price = re.sub(r"[^0-9]", "", price)
        if price == '':
            price = None
        else:
            price = int(price)
    except:
        price = None
    return price


@log_warning_if_returns_none
def get_location(soup):
    try:
        location = soup.find("h2", {"class": "re-DetailMap-address"}).text
    except:
        location = None
    return location


@log_warning_if_returns_none
def get_title(soup):
    try:
        title = soup.find("h1", {"class": "re-DetailHeader-propertyTitle"}).text
    except:
        # Log error
        title = None
    return title





