import pytest
from service.create_database import create_database
from service.fake_data import fake_data
from service.test import test_create, test_trigger, test_view, test


def main():
    create_database()
    fake_data()


if __name__ == '__main__':
    main()
