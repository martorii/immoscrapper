from decouple import config
from database.mysql import Database

from scrappers.Fotocasa import Fotocasa

# Set connection to database
db = Database(config('db_host'), config('db_port'), config('db_database'), config('db_user'), config('db_password'))

# Wait until connection is available
# if not db.test_connection():
#    exit(0)


# Define what to search for
city = "barcelona"
mode = "buy"
pages = [1, 3000]

fotocasa = Fotocasa(
    mode=mode,
    city=city
)

# Scrap
fotocasa.scrap(pages, db)
