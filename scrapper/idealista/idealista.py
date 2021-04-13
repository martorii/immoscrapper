class Idealista:

    def __init__(self, province, city, action):
        self.province = province
        self.city = city
        self.action = action
        self.main_url = "https://www.idealista.com/" + self.get_action_url + "/" + self.get_location_url() + "/"

    # Get the url part corresponding to buy or rent
    @property
    def get_action_url(self):
        if self.action == "buy":
            action_url = "venta-viviendas"
        elif self.action == "rent":
            action_url = "alquiler-viviendas"
        return action_url

    # Get the url part corresponding to the location
    def get_location_url(self):
        location_url = self.province.lower() + "-" + self.city.lower()
        return location_url

    def extract_info(self, raw_html):
        # Get information
        pass
