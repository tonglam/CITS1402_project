import csv
import random
import sqlite3
import string

from faker import Faker

import constants
from domain.Customer import Customer
from domain.Phone import Phone
from domain.PhoneModel import PhoneModel
from domain.rentalContract import rentalContract
from tools.imei import generate_imei

fake = Faker()
phone_models_list = []


def customer_data(conn, cursor):
    customer_list = []
    for i in range(100):
        customer = Customer(i + 1, fake.name(), fake.email())
        customer_list.append(customer.__str__())
    try:
        cursor.execute("DELETE FROM Customer")
        cursor.executemany('''
            INSERT INTO Customer (customerId, customerName, customerEmail)
            VALUES (?, ?, ?)
        ''', customer_list)
        conn.commit()
    except sqlite3.Error as e:
        print('fake customer data failed: ', e)


def read_phone_model():
    with open('tools/cleaned_all_phones.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            phone_model = PhoneModel(
                generate_model_number(),
                row['phone_name'] + row['brand'],
                row['storage(GB)'],
                generate_color(),
                row['price(USD)'],
                round(float(row['price(USD)']) / 365, 2)
            )
            phone_models_list.append(phone_model.__str__())


def phone_model_data(conn, cursor):
    try:
        cursor.execute("DELETE FROM PhoneModel")
        cursor.executemany('''
            INSERT INTO PhoneModel (modelNumber, modelName, storage, colour, baseCost, dailyCost)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', phone_models_list)
        conn.commit()
    except sqlite3.Error as e:
        print('fake phone model data failed: ', e)


def generate_model_number():
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(10))
    return random_string


def generate_color():
    colors = ["red", "blue", "green", "yellow", "pink", "purple", "orange", "brown", "black", "white"]
    random_color = random.choice(colors)
    return random_color


def phone_data(conn, cursor):
    phone_list = []
    for x in phone_models_list:
        imei = generate_imei()
        phone = Phone(
            imei,
            x[0],
            x[1]
        )
        phone_list.append(phone.__str__())
    try:
        cursor.execute("DELETE FROM Phone")
        cursor.executemany('''
            INSERT INTO Phone (IMEI, modelNumber, modelName)
            VALUES (?, ?, ?)
        ''', phone_list)
        conn.commit()
    except sqlite3.Error as e:
        print('make up phone data failed: ', e)


def rental_contract_data(conn, cursor):
    cursor.execute('SELECT imei FROM Phone')
    imei_list = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT customerId FROM Customer')
    customer_list = [row[0] for row in cursor.fetchall()]
    rental_contract_list = []
    ket_set = set()
    for i in range(500):
        customer_id = random.choice(customer_list)
        imei = random.choice(imei_list)
        key = str(customer_id) + imei
        if key in ket_set:
            continue
        ket_set.add(key)
        rental_contract = rentalContract(
            customer_id,
            imei,
            fake.date_between(start_date='-1y', end_date='today'),
            None,
            None
        )
        rental_contract_list.append(rental_contract.__str__())
    try:
        cursor.execute("DELETE FROM rentalContract")
        cursor.executemany('''
                    INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                    VALUES (?, ?, ?, ?, ?)
                ''', rental_contract_list)
        conn.commit()
    except sqlite3.Error as e:
        print('make up rental contract data failed: ', e)


def fake_data():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    # fake
    customer_data(conn, cursor)
    read_phone_model()
    phone_model_data(conn, cursor)
    phone_data(conn, cursor)
    rental_contract_data(conn, cursor)
    cursor.close()
    conn.close()
