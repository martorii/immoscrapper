from decouple import config
from mysql import Database

# Set connection to database
db = Database(config('db_host'), config('db_port'), config('db_database'), config('db_user'), config('db_password'))

# Wait until connection is available
if not db.test_connection():
    exit(0)

# Configure database
db.run_initial_scripts()