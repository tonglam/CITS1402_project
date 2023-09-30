import os
import sqlite3

import constants


def create_database():
    # drop database if exists
    if os.path.exists(constants.database_name):
        os.remove(constants.database_name)
    # create database
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    try:
        # create table
        with open('sql/createTables.sql', 'r') as sql_file:
            create_tables = sql_file.read()
        cursor.executescript(create_tables)
        # create trigger
        with open('sql/createTrigger.sql', 'r') as sql_file:
            create_trigger = sql_file.read()
        cursor.executescript(create_trigger)
        # create view
        with open('sql/createView.sql', 'r') as sql_file:
            create_view = sql_file.read()
        cursor.executescript(create_view)
        conn.commit()
        # open foreign key setting
        foreign_key_setting = False
        while not foreign_key_setting:
            cursor.execute("PRAGMA foreign_keys = ON")
            conn.commit()
            cursor.execute("PRAGMA foreign_keys")
            rows = cursor.fetchall()
            if rows[0][0] == 1:
                foreign_key_setting = True
    except sqlite3.Error as e:
        print('execute project sql files failed: ', e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    create_database()
