import constants
import os
import pytest
from create_database import create_database
from fake_data import fake_data


def drop_database():
    if os.path.exists(constants.database_name):
        os.remove(constants.database_name)


def main():
    create_database()
    # fake_data()
    # test()


if __name__ == '__main__':
    create_database()
