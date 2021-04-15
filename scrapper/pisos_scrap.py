# Scrap idealista
from decouple import config
from database.mysql import Database

import pisos.scrapper as pisos_scrapper

# Set connection to database
db = Database(config('db_host'), config('db_port'), config('db_database'), config('db_user'), config('db_password'))

# Wait until connection is available
if not db.test_connection():
    exit(0)


# Define what to search for
city = "Barcelona"
action = "buy"
pages = [45, 2000]

# Scrap
pisos_scrapper.scrap(city, action, pages, db)