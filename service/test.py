import Constants
import sqlite3

conn = sqlite3.connect(Constants.database_name)
cursor = conn.cursor()


def test_create():
    # primary key
    try:
        print(1)
    except sqlite3.Error as e:
        print('test create table -  primary key failed: ', e)

    # foreign key
    # IMEI validation


def test_trigger():
    print(1)


def test_view():
    print(1)


def test():
    test_create()
    test_trigger()
    test_view()


if __name__ == '__main__':
    test()
