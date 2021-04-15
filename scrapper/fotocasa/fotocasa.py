import datetime

from bs4 import BeautifulSoup
import re

# Define mapping website --> attribute_name
data_dict = {
            "Built-up area": "built_up_area",
            "Useable floor area": "usable_floor_area",
            "Rooms": "n_rooms",
            "Bathrooms": "n_bathrooms",
            "Flooring": 'flooring',
            "Floor area": "floor_area",
            "Floor": "floor",
            "Antiquity": "antiquity",
            "Condition": "condition",
            "Heating": "heating",
            "Equipped kitchen": "equipped_kitchen",
            "Lift": "lift",
            "Air con": "air_conditioning",
            "Garage": "garage",
            "Own balcony": "balcony",
            "Terrace": "terrace",
            "Security system": "security_system",
            "Facing": "facing",
            "Swimming pool": "swimming_pool",
            "Garden": "garden"
        }


def log_attribute_not_found(attribute):
    print(f"{attribute} not found")
    return


def log_attribute_found(attribute, value):
    print(f"{attribute} = {value}")
    return


def get_price(soup):
    price = None
    try:
        price = soup.find("span", {"class": "h1 jsPrecioH1"}).text
        # Remove currency and .
        price = re.sub(r"[^0-9]", "", price)
    except:
        # Log error
        log_attribute_not_found("price")
    return price


def get_location(soup):
    location = None
    try:
        location = soup.find("h2", {"class": "position"}).text
    except:
        # Log error
        log_attribute_not_found("location")
    return location


def get_title(soup):
    title = None
    try:
        title = soup.find("h1", {"class": "title"}).text
    except:
        # Log error
        log_attribute_not_found("title")
    return title


def get_energy_certificate(soup):
    certificate = None
    try:
        certificate = soup.find('div', {"class": "sel"}).text
    except:
        pass
    return certificate


def get_value_from_raw_text(key, text):
    value = None
    if not "Sin especificar" in text:
        try:
            if key == "Garage":
                if ":" in text:
                    value = re.sub(r"[^0-9]", "", text)
                else:
                    value = 1
            if key == "Garden":
                if ":" in text:
                    value = text.split(":")[1].strip()
                else:
                    value = "private"
            if key in ["Heating", "Air con"]:
                if ":" in text:
                    value = text.split(":")[1].strip()
                else:
                    value = "yes"
            if key == "Floor":
                if ("Basement" in text) or ("Ground floor" in text):
                    value = 0
                else:
                    value = re.sub(r"[^0-9]", "", text.split(":")[1].strip())
            if key in ["Built-up area", "Useable floor area", "Rooms", "Bathrooms", "Floor area"]:
                value = re.sub(r"[^0-9]", "", text)
            elif key in ["Condition", "Antiquity",  "Facing", "Flooring", "Swimming pool"]:
                value = text.split(":")[1].strip()
            elif key in ["Own Balcony", "Terrace", "Security system", "Equipped kitchen", "Lift"]:
                value = True
        except:
            print("This key could not be matched:", key)
    return value


class Fotocasa:

    def __init__(self, html, url):
        self.url = url
        # Convert html to soup
        soup = BeautifulSoup(html, 'html.parser')
        # Get easy attributes
        self.extraction_date = datetime.date.today().strftime("%Y-%m-%d")
        self.price = get_price(soup)
        self.location = get_location(soup)
        self.title = get_title(soup)
        self.energy_certificate = get_energy_certificate(soup)
        # Set all remaining attributes
        self.set_data(soup)

    def set_data(self, soup):
        data_dict_temp = data_dict.copy()
        # Get all features from the first box (some of them are missing depending on the flat)
        basic_data = soup.find_all("li", {"class": "charblock-element more-padding"})
        # Get all features from the bullet points
        extra_data = soup.find_all('li', {'class': 'charblock-element element-with-bullet'})
        # Concatenate
        all_data = basic_data + extra_data
        for attribute in all_data:
            # Get all text from attribute
            text = attribute.text.replace("\n", "")
            # Set match to see if we could find an attribute that matched the text
            match = False
            for key in data_dict_temp:
                if key in text:
                    # Convert raw text to a value
                    value = get_value_from_raw_text(key, text)
                    # Set attribute dynamically
                    self.__setattr__(data_dict_temp[key], value)
                    # Set match to true to delete the entry from dictionary
                    match = True
                    break
            if match:
                # Delete entry from dictionary
                data_dict_temp.pop(key)
        return
