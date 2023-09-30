import sqlite3

import constants
from tools.imei import generate_imei


def check_schema(cursor):
    table_list = ["Phone", "PhoneModel", "rentalContract", "Customer"]
    # get basic data_type
    table_dict = {}
    with open('tools/createTablesBasic.sql', 'r') as f:
        text = f.read()
        for x in text.split("CREATE TABLE"):
            data_dict = {}
            if len(x) == 0 or x.count("(") != 1 or x.count(")") != 1:
                continue
            for y in x.split("\n"):
                if len(y) == 0 or y.count("(") > 0 or y.count(")") > 0:
                    continue
                y = y.strip().replace(",", "")
                data_type = y.split(" ")
                data_type = [x for x in data_type if len(x) > 0]
                key = data_type[0]
                value = data_type[1]
                data_dict[key] = value
            table_dict[x.split(" ")[1]] = data_dict
    # get data_type from database
    for table in table_list:
        expected_data_dict = table_dict[table]
        sql = "PRAGMA table_info({})".format(table)
        cursor.execute(sql)
        rows = cursor.fetchall()
        assert len(rows) == len(expected_data_dict)
        for row in rows:
            col_name = row[1]
            # check row names
            assert col_name in expected_data_dict
            col_data_type = row[2]
            expected_col_data_type = expected_data_dict[col_name]
            # check data type
            assert expected_col_data_type == col_data_type
            # check primary key
            if table == "Phone" and col_name == "IMEI":
                assert row[5] == 1
            elif table == "PhoneModel" and col_name == "modelNumber":
                assert row[5] == 1
            elif table == "rentalContract" and (col_name == "customerId" or col_name == "IMEI"):
                assert row[5] > 0
            elif table == "Customer" and col_name == "customerId":
                assert row[5] == 1
        # check foreign key
        if table == "Phone":
            sql = "PRAGMA foreign_key_list({})".format(table)
            cursor.execute(sql)
            rows = cursor.fetchall()
            assert len(rows) == 2
            for row in rows:
                assert row[2] == "PhoneModel"
                assert row[3] == "modelNumber" or row[3] == "modelName"
                assert row[4] == "modelNumber" or row[4] == "modelName"
        if table == "rentalContract":
            sql = "PRAGMA foreign_key_list({})".format(table)
            cursor.execute(sql)
            rows = cursor.fetchall()
            assert len(rows) == 2
            for row in rows:
                assert row[2] == "Customer" or row[2] == "Phone"
                assert row[3] == "customerId" or row[3] == "IMEI"
                assert row[4] == "customerId" or row[4] == "IMEI"
                if row[2] == "Phone" and row[3] == "IMEI" and row[4] == "IMEI":
                    assert row[6] == "SET NULL"


def check_primary_key(cursor):
    # check Phone primary key
    cursor.execute('SELECT * FROM Phone')
    phone_list = cursor.fetchall()
    phone_test = phone_list[14]
    try:
        cursor.execute('''
                       INSERT INTO Phone (IMEI, modelNumber, modelName)
                       VALUES (?, ?, ?)
                   ''', phone_test)
        raise Exception("test Phone primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass Phone primary key test')
    # check PhoneModel primary key
    cursor.execute('SELECT * FROM PhoneModel')
    phone_model_list = cursor.fetchall()
    phone_model_test = phone_model_list[14]
    try:
        cursor.execute('''
                       INSERT INTO PhoneModel (modelNumber, modelName, storage, colour, baseCost, dailyCost)
                       VALUES (?, ?, ?, ?, ?, ?)
                   ''', phone_model_test)
        raise Exception("test PhoneModel primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass PhoneModel primary key test')
    # check rentalContract primary key
    cursor.execute('SELECT * FROM rentalContract')
    rental_contract_list = cursor.fetchall()
    rental_contract_test = rental_contract_list[14]
    try:
        cursor.execute('''
                       INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                       VALUES (?, ?, ?, ?, ?)
                   ''', rental_contract_test)
        raise Exception("test rentalContract primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass rentalContract primary key test')
    # check Customer primary key
    cursor.execute('SELECT * FROM Customer')
    customer_list = cursor.fetchall()
    customer_test = customer_list[14]
    try:
        cursor.execute('''
                       INSERT INTO Customer (customerId, customerName, customerEmail)
                       VALUES (?, ?, ?)
                   ''', customer_test)
        raise Exception("test Customer primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass Customer primary key test')


def check_foreign_key(cursor):
    # check Phone foreign key
    cursor.execute('SELECT * FROM Phone')
    phone_list = cursor.fetchall()
    phone_test = (generate_imei(), '99' + phone_list[14][1], '99' + phone_list[14][2])
    print(phone_test.__str__())
    try:
        cursor.execute('''
                          INSERT INTO Phone (IMEI, modelNumber, modelName)
                          VALUES (?, ?, ?)
                      ''', phone_test)
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test:' + str(e))


def check_key_constraints(cursor):
    pass


def test_schema():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    check_schema(cursor)
    cursor.close()
    conn.close()


def test_data():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    # check primary key
    # check_primary_key(cursor)
    # check foreign key
    check_foreign_key(cursor)
    # check key constraints
    # check_key_constraints(cursor)
    cursor.close()
    conn.close()
