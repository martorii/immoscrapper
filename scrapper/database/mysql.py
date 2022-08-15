from sqlalchemy import create_engine, insert, Table, MetaData, func, inspect, text, update
from sqlalchemy.orm import Session
import datetime
import time
import os


class Database:
    def __init__(self, host, port, database, user, password):
        self.user = user
        self.password = password
        self.host = host
        # self.host = "localhost"
        self.database = database
        self.port = port
        self.engine_url = "mysql+pymysql://" + str(self.user) + ":" + str(self.password) + "@" + self.host + ":" + \
                          self.port + "/" + str(self.database)
        parent_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
        self.initial_scripts_directory = parent_dir + "/initial_scripts"
        self.engine = create_engine(self.engine_url)

    def test_connection(self):
        print("Test: Database connection.")
        n_max_retries = 3
        n_retries = 0
        waiting_time = 5
        connected = False
        while not connected:
            try:
                self.engine.connect()
                print("Success: Connection to database.")
                connected = True
                return True
            except:
                print("Retrying...")
                n_retries += 1
                if n_retries == n_max_retries:
                    print("Error: Connection to database.")
                    break
                time.sleep(waiting_time)
        return False

    def run_initial_scripts(self):
        print("Running initial scripts...")
        # Iterate over all files in initial_scripts
        for script_name in os.listdir(self.initial_scripts_directory):
            script_path = os.path.join(self.initial_scripts_directory, script_name)
            with open(script_path, "r") as script_file:
                script = script_file.read()
                self.engine.execute(script)
        print("Success: database is ready to go.")
        return

    def insert_object_into_table(self, table, data_dict):
        """
        Insert a scrapper instance into the database as a new record
        :param table: table to insert into
        :param data_dict: dictionary containing the keys and values to insert
        :return:
        """
        session = Session(self.engine, future=True)
        db_table = self.get_sqlalchemy_table(table)
        session.execute(db_table.insert().values(data_dict))
        session.commit()
        return

    # def update_last_seen(self, table, url):
    #     """
    #     Update field "last_seen" in the database with the current date
    #     :param table: table to update
    #     :param url: primary key to identify the property
    #     :return:
    #     """
    #     db_table = self.get_sqlalchemy_table(table)
    #     u = update(db_table)
    #     u = u.values({"last_seen": datetime.date.today().strftime("%Y-%m-%d")})
    #     u = u.where(db_table.c.url == url)
    #     session = Session(self.engine, future=True)
    #     session.execute(u)
    #     session.commit()
    #     return

    def get_sqlalchemy_table(self, table):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        db_table = meta.tables[table]
        return db_table

    # def is_url_in_database(self, url):
    #     url_where = url
    #     db_table = self.get_sqlalchemy_table(table)
    #     stmt = db_table.select().where(db_table.c.url == url_where)
    #     result = self.engine.execute(stmt).fetchall()
    #     if len(result) > 0:
    #         return True
    #     else:
    #         return False

    def exists_in_db(self, table, value, field):
        """
        Check if a row in the table where field = value exists
        :param table: table to search for
        :param value: value to match
        :param field: field to match
        :return:
        """
        db_table = self.get_sqlalchemy_table(table)
        stmt = db_table.select().where(db_table.c[field] == value)
        result = self.engine.execute(stmt).fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def update_last_seen(self, table, url):
        """
        Update field "last_seen" in the database with the current date
        :param table: table to update
        :param url: primary key to identify the property
        :return:
        """
        db_table = self.get_sqlalchemy_table(table)
        last_seen = datetime.date.today().strftime("%Y-%m-%d")
        stmt = db_table.update().where(db_table.c.url == url).values(last_seen=last_seen)
        session = Session(self.engine, future=True)
        session.execute(stmt)
        session.commit()
        return

    def get_columns(self, table):
        db_table = self.get_sqlalchemy_table(table)
        return db_table.columns

    def select_table(self, table):
        db_table = self.get_sqlalchemy_table(table)
        stmt = db_table.select()
        result = self.engine.execute(stmt).fetchall()
        return result

    def select_unique_query(self, query):
        session = Session(self.engine, future=True)
        query_result = session.execute(query).fetchall()
        session.commit()
        result = [r[0] for r in query_result]
        return result
