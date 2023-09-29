import Constants
import os
import sqlite3


def create_database():
    # drop database if exists
    if os.path.exists(Constants.database_name):
        os.remove(Constants.database_name)
    conn = sqlite3.connect(Constants.database_name)
    cursor = conn.cursor()
    try:
        # create table
        with open('../sql/createTables.sql', 'r') as sql_file:
            create_tables = sql_file.read()
        cursor.executescript(create_tables)
        conn.commit()
        # create trigger
        with open('../sql/createTrigger.sql', 'r') as sql_file:
            create_trigger = sql_file.read()
        cursor.executescript(create_trigger)
        conn.commit()
        # create view
        with open('../sql/createView.sql', 'r') as sql_file:
            create_view = sql_file.read()
        cursor.executescript(create_view)
        conn.commit()
    except sqlite3.Error as e:
        print('execute project sql files failed: ', e)
