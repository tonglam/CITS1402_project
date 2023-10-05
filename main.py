import constants
import os
from create_database import create_database
from fake_data import fake_data
from test import test


def drop_database():
    if os.path.exists(constants.database_name):
        os.remove(constants.database_name)


def main():
    drop_database()
    create_database()
    fake_data()
    test()


if __name__ == '__main__':
    for i in range(100):
        print("start test time: {}".format(i + 1))
        main()
        print("finish test time: {}".format(i + 1))
