import Constants
import os
import pytest
from create_database import create_database
from fake_data import fake_data


def drop_database():
    if os.path.exists(Constants.database_name):
        os.remove(Constants.database_name)


def main():
    create_database()
    # fake_data()
    # test()


if __name__ == '__main__':
    main()
