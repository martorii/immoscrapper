# import datetime
#
# from bs4 import BeautifulSoup
# import re
#
# # Define mapping website --> attribute_name
# data_dict = {
#             "Built-up area": "built_up_area",
#             "Useable floor area": "usable_floor_area",
#             "bdrm.": "n_rooms",
#             "Energy consumption": "energy_certificate",
#             "bathroom": "n_bathrooms",
#             "sqm": "floor_area",
#             "Flooring": 'flooring',
#             "Floor area": "floor_area",
#             "Floor": "floor",
#             "Antiquity": "antiquity",
#             "Status": "condition",
#             "Heating": "heating",
#             "Fully equipped kitchen": "equipped_kitchen",
#             "Elevator": "lift",
#             "Air Conditioning": "air_conditioning",
#             "Parking": "garage",
#             "Balcony": "own_balcony",
#             "Terrace": "terrace",
#             "Security Door": "security_system",
#             "Orientation": "facing",
#             "Swimming pool": "swimming_pool",
#             "Garden": "garden"
#         }
#
#
# def log_attribute_not_found(attribute):
#     print(f"{attribute} not found")
#     return
#
#
# def log_attribute_found(attribute, value):
#     print(f"{attribute} = {value}")
#     return
#
#
# def get_price(soup):
#     price = None
#     try:
#         price = soup.find("span", {"class": "re-DetailHeader-price"}).text
#         # Remove currency and .
#         price = re.sub(r"[^0-9]", "", price)
#         if price == '':
#             price = -1
#     except:
#         # Log error
#         log_attribute_not_found("price")
#     return price
#
#
# def get_location(soup):
#     location = None
#     try:
#         location = soup.find("h2", {"class": "re-DetailMap-address"}).text
#     except:
#         # Log error
#         log_attribute_not_found("location")
#     return location
#
#
# def get_title(soup):
#     title = None
#     try:
#         title = soup.find("h1", {"class": "re-DetailHeader-propertyTitle"}).text
#     except:
#         # Log error
#         log_attribute_not_found("title")
#     return title
#
#
# def get_value_from_raw_text(key, text):
#     value = None
#     try:
#         if key == "Energy consumption":
#             value = text.replace(key, "")[0]
#         elif key in ["Parking"]:
#             value = 1
#         elif key in ["Antiquity", "Status", "Heating", "Orientation"]:
#             value = text.replace(key, "")
#             if key == "Heating" and value == '':
#                 value = 'Yes'
#         elif key == "Floor":
#             zero_floor_list = ['Ground', 'Main floor', 'Mezzanine', 'Basement', 'Subbasement']
#             if any(zero_floor in text for zero_floor in zero_floor_list):
#                 value = 0
#             else:
#                 value = re.sub(r"[^0-9]", "", text)
#         elif key in ["sqm", "bathroom", "bdrm.", "Parking"]:
#             value = re.sub(r"[^0-9]", "", text)
#             if (key in "bathroom") and (value == ''):
#                 value = None
#             elif key == "Parking" and value == '':
#                 value = 1
#         elif key in ["Air Conditioning", "Garden", "Swimming pool"]:
#             value = "Yes"
#         elif key in ["Terrace", "Balcony", "Fully equipped kitchen", "Security Door", "Elevator"]:
#             value = 1
#     except:
#         print("This key could not be matched:", key)
#     return value
#
#
# class Fotocasa:
#
#     def __init__(self, html, url, action):
#         self.url = url
#         self.portal = "fotocasa"
#         # Convert html to soup
#         soup = BeautifulSoup(html, 'html.parser')
#         # Get easy attributes
#         self.extraction_date = datetime.date.today().strftime("%Y-%m-%d")
#         self.price = get_price(soup)
#         self.location = get_location(soup)
#         self.title = get_title(soup)
#         self.sale_or_rent = action
#         # Set all remaining attributes
#         self.set_data(soup)
#
#     def set_data(self, soup):
#         data_dict_temp = data_dict.copy()
#         # Get all features from the first box (some of them are missing depending on the flat)
#         features_data = soup.find_all("li", {"class": "re-DetailHeader-featuresItem"})
#         # Get all features from the bullet points
#         extra_data = soup.find_all('div', {'class': 're-DetailFeaturesList-featureContent'})
#         # Get info from the tags below
#         extra_tags = soup.find_all("li", {"class": "re-DetailExtras-listItem"})
#         # Concatenate
#         all_data = features_data + extra_data + extra_tags
#         for attribute in all_data:
#             # Get all text from attribute
#             text = attribute.text
#             # Set match to see if we could find an attribute that matched the text
#             match = False
#             for key in data_dict_temp:
#                 if key in text:
#                     # Convert raw text to a value
#                     value = get_value_from_raw_text(key, text)
#                     # Set attribute dynamically
#                     self.__setattr__(data_dict_temp[key], value)
#                     # Set match to true to delete the entry from dictionary
#                     match = True
#                     break
#             if match:
#                 # Delete entry from dictionary
#                 data_dict_temp.pop(key)
#         return
