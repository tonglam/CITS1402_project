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
        # create trigger monitor
        create_trigger_monitor(conn, cursor)
    except sqlite3.Error as e:
        print('execute project sql files failed: ', e)
    finally:
        cursor.close()
        conn.close()


def create_trigger_monitor(conn, cursor):
    # create a trigger_monitor table
    cursor.execute("DROP TABLE IF EXISTS trigger_monitor")
    cursor.execute('''
        CREATE TABLE trigger_monitor (
            trigger_name TEXT,
            trigger_time TEXT
        )
    ''')
    conn.commit()
    # create a trigger_monitor trigger
    cursor.execute("DROP TRIGGER IF EXISTS trigger_monitor")
    cursor.execute('''
        CREATE TRIGGER trigger_monitor
        AFTER UPDATE OF rentalCost ON rentalContract
        BEGIN
            INSERT INTO trigger_monitor (trigger_name, trigger_time)
            VALUES ('trigger_monitor', datetime('now'));
        END
    ''')
    conn.commit()


if __name__ == '__main__':
    create_database()
