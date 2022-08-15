import time
import pprint
import datetime
import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

DRIVER_PATH = r"C:\Users\EMLZ\OneDrive - metafinanz Informationssysteme GmbH\Projects\immoscrapper\scrapper\scrappers\drivers\chromedriver_103.exe"


def log_warning_if_returns_none(func):
    """
    This decorator logs a warning if the attribute was not found
    :param func: function that returns the attribute
    """
    def wrapper(*args):
        func_name = func.__name__
        ret = func(*args)
        if ret is None:
            logging.warning(f"{func_name} could not find a non-null value.")
        return ret
    return wrapper


class Scrapper:
    def __init__(self, mode, city):
        self.mode = mode
        self.city = city
        self.data = {
            'sale_or_rent': mode,
            'last_seen': datetime.date.today().strftime("%Y-%m-%d"),
            'extraction_date': datetime.date.today().strftime("%Y-%m-%d")
        }
        self.sql_table = "properties"

    def __str__(self):
        return pprint.pformat(self.data, indent=2)

    def extract_data(self, ad_url):
        """
        This method will be overridden in each child
        :param ad_url:
        :return:
        """
        pass

    def sanity_check(self):
        pass

    def update_db(self, db):
        """
        Update database with the new property. If it does not exist yet, insert it, otherwise update.
        :param db: Database Class
        :return: success or failure
        """
        try:
            if not db.exists_in_db(self.sql_table, self.data['url'], 'url'):
                # Extract data according to the overridden method
                self.extract_data(self.data['url'])
                if self.sanity_check():
                    # Add to database
                    db.insert_object_into_table(self.sql_table, self.data)
            else:
                db.update_last_seen(self.sql_table, self.data['url'])
        except Exception as e:
            logging.warning(f"Error {str(e)} for url = \n {self.data['url']}")
        # Sleep a bit
        sleep_time = self.get_sleep_time()
        time.sleep(sleep_time)
        return

    @staticmethod
    def start_browser():
        """
        Add options to browser and start it
        :return:
        """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
        return browser

    @staticmethod
    def scroll_to_bottom(browser, page_downs):
        elem = browser.find_element(By.TAG_NAME, "body")
        while page_downs:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            page_downs -= 1
        return

    @staticmethod
    def get_sleep_time():
        slow_search_range = range(9, 23)
        fast_search_range = range(0, 9)
        current_hour = datetime.datetime.now().hour
        if current_hour in slow_search_range:
            return random.randint(1, 3)
        elif current_hour in fast_search_range:
            return random.randint(1, 2)


