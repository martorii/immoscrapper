# Scrap idealista
from decouple import config
import time
from database.mysql import Database
import pisos.scrapper as pisos_scrapper

# Set connection to database
db = Database(config('db_host'), config('db_port'), config('db_database'), config('db_user'), config('db_password'))

# Wait until connection is available
if not db.test_connection():
    exit(0)

# Configure database
db.run_initial_scripts()

# Define what to search for
province = "Barcelona"
city = "Barcelona"
action = "buy"

pisos_scrapper.scrap(city, action, db)