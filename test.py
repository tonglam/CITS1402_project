import random
import sqlite3

import constants
from tools.imei import generate_imei
from datetime import datetime, timedelta


def check_schema(conn, cursor):
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
        conn.commit()
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
            conn.commit()
            rows = cursor.fetchall()
            assert len(rows) == 2
            for row in rows:
                assert row[2] == "PhoneModel"
                assert row[3] == "modelNumber" or row[3] == "modelName"
                assert row[4] == "modelNumber" or row[4] == "modelName"
        if table == "rentalContract":
            sql = "PRAGMA foreign_key_list({})".format(table)
            cursor.execute(sql)
            conn.commit()
            rows = cursor.fetchall()
            assert len(rows) == 2
            for row in rows:
                assert row[2] == "Customer" or row[2] == "Phone"
                assert row[3] == "customerId" or row[3] == "IMEI"
                assert row[4] == "customerId" or row[4] == "IMEI"
                if row[2] == "Phone" and row[3] == "IMEI" and row[4] == "IMEI":
                    assert row[6] == "SET NULL"


def check_primary_key(conn, cursor):
    # check Phone primary key
    cursor.execute('SELECT * FROM Phone')
    conn.commit()
    phone_list = cursor.fetchall()
    phone_test = phone_list[14]
    try:
        cursor.execute('''
                       INSERT INTO Phone (IMEI, modelNumber, modelName)
                       VALUES (?, ?, ?)
                   ''', phone_test)
        conn.commit()
        raise Exception("test Phone primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass Phone primary key test')
    # check PhoneModel primary key
    cursor.execute('SELECT * FROM PhoneModel')
    conn.commit()
    phone_model_list = cursor.fetchall()
    phone_model_test = phone_model_list[14]
    try:
        cursor.execute('''
                       INSERT INTO PhoneModel (modelNumber, modelName, storage, colour, baseCost, dailyCost)
                       VALUES (?, ?, ?, ?, ?, ?)
                   ''', phone_model_test)
        conn.commit()
        raise Exception("test PhoneModel primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass PhoneModel primary key test')
    # check rentalContract primary key
    cursor.execute('SELECT * FROM rentalContract')
    conn.commit()
    rental_contract_list = cursor.fetchall()
    rental_contract_test = rental_contract_list[14]
    try:
        cursor.execute('''
                       INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                       VALUES (?, ?, ?, ?, ?)
                   ''', rental_contract_test)
        conn.commit()
        raise Exception("test rentalContract primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass rentalContract primary key test')
    # check Customer primary key
    cursor.execute('SELECT * FROM Customer')
    conn.commit()
    customer_list = cursor.fetchall()
    customer_test = customer_list[14]
    try:
        cursor.execute('''
                       INSERT INTO Customer (customerId, customerName, customerEmail)
                       VALUES (?, ?, ?)
                   ''', customer_test)
        conn.commit()
        raise Exception("test Customer primary key failed, same record should not be inserted")
    except sqlite3.Error:
        print('pass Customer primary key test')


def check_foreign_key(conn, cursor):
    # open foreign key setting, this will only be activated in the current connection
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    # check Phone foreign key
    cursor.execute('SELECT * FROM Phone')
    conn.commit()
    phone_list = cursor.fetchall()
    new_imei = generate_imei()

    phone_test = (new_imei, '99' + phone_list[14][1], phone_list[14][2])
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                          INSERT INTO Phone (IMEI, modelNumber, modelName)
                          VALUES (?, ?, ?)
                      ''', phone_test)
        conn.commit()
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test 1:' + str(e))

    phone_test = (new_imei, phone_list[14][1], '99' + phone_list[14][2])
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                         INSERT INTO Phone (IMEI, modelNumber, modelName)
                         VALUES (?, ?, ?)
                     ''', phone_test)
        conn.commit()
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test 2:' + str(e))

    phone_test = (new_imei, '99' + phone_list[14][1], '99' + phone_list[14][2])
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                        INSERT INTO Phone (IMEI, modelNumber, modelName)
                        VALUES (?, ?, ?)
                    ''', phone_test)
        conn.commit()
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test 3:' + str(e))

    # check rentalContract foreign key
    cursor.execute('SELECT * FROM rentalContract')
    conn.commit()
    contract_list = cursor.fetchall()
    new_imei = generate_imei()

    contract_test = (
        -99,
        contract_list[14][1],
        contract_list[14][2],
        None,
        None
    )
    print("rentalContract foreign key test data:{}".format(contract_test.__str__()))
    try:
        cursor.execute('''
                       INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                       VALUES (?, ?, ?, ?, ?)
                    ''', contract_test)
        conn.commit()
        raise Exception("test rentalContract foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass rentalContract foreign key test 1:' + str(e))

    contract_test = (
        contract_list[14][0],
        new_imei,
        contract_list[14][2],
        None,
        None
    )
    print("rentalContract foreign key test data:{}".format(contract_test.__str__()))
    try:
        cursor.execute('''
                          INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                          VALUES (?, ?, ?, ?, ?)
                       ''', contract_test)
        conn.commit()
        raise Exception("test rentalContract foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass rentalContract foreign key test 2:' + str(e))

    contract_test = (
        -99,
        new_imei,
        contract_list[14][2],
        None,
        None
    )
    print("rentalContract foreign key test data:{}".format(contract_test.__str__()))
    try:
        cursor.execute('''
                             INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                             VALUES (?, ?, ?, ?, ?)
                          ''', contract_test)
        conn.commit()
        raise Exception("test rentalContract foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass rentalContract foreign key test 3:' + str(e))


def check_key_constraints(conn, cursor):
    cursor.execute('SELECT * FROM Phone')
    conn.commit()
    phone_list = cursor.fetchall()
    imei = phone_list[7][0]

    # length of IMEI should be 15
    new_imei = imei[0:7]
    phone_test = (new_imei, phone_list[7][1], phone_list[7][2])
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                       INSERT INTO Phone (IMEI, modelNumber, modelName)
                       VALUES (?, ?, ?)
                       ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 1:' + str(e))

    # IMEI should be all digits
    new_imei = imei[0:14] + 'A'
    phone_test = (new_imei, phone_list[7][1], phone_list[7][2])
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                           INSERT INTO Phone (IMEI, modelNumber, modelName)
                           VALUES (?, ?, ?)
                           ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 2:' + str(e))

    # IMEI should be meet the validation
    new_imei = str(int(imei) - 1)
    phone_test = (new_imei, phone_list[7][1], phone_list[7][2])
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                              INSERT INTO Phone (IMEI, modelNumber, modelName)
                              VALUES (?, ?, ?)
                              ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 3:' + str(e))


def test_schema():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    check_schema(conn, cursor)
    cursor.close()
    conn.close()


def test_data():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    # check primary key
    check_primary_key(conn. cursor)
    # check foreign key
    check_foreign_key(conn, cursor)
    # check key constraints
    check_key_constraints(conn, cursor)
    cursor.close()
    conn.close()


def create_trigger_monitor(conn, cursor):
    # create a trigger_monitor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trigger_monitor (
            trigger_name TEXT,
            trigger_time TEXT
        )
    ''')
    conn.commit()

    # create a trigger_monitor trigger
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trigger_monitor
        AFTER UPDATE ON rentalContract
        BEGIN
            INSERT INTO trigger_monitor (trigger_name, trigger_time)
            VALUES ('trigger_monitor', datetime('now'));
        END
    ''')
    conn.commit()


def trigger_rental_cost(conn, cursor):
    cursor.execute('SELECT * FROM rentalContract')
    rental_contract_list = cursor.fetchall()
    customer_id = rental_contract_list[11][0]
    imei = rental_contract_list[11][1]
    date_out = rental_contract_list[11][2]
    rent_day = random.randint(1, 100)
    date_back = (datetime.strptime(date_out, "%Y-%m-%d") + timedelta(days=rent_day)).strftime("%Y-%m-%d")
    trigger_test = (
        customer_id,
        imei,
        date_out,
        date_back,
        None
    )
    print("Trigger test data:{}".format(trigger_test.__str__()))
    cursor.execute("UPDATE rentalContract SET dateBack = ? WHERE customerId = ? AND IMEI = ? AND rentalCost IS NULL ",
                   (date_back, customer_id, imei))
    conn.commit()


def test_trigger():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    # create a trigger_monitor trigger and a trigger_monitor table
    create_trigger_monitor(conn, cursor)
    # trigger one record
    trigger_rental_cost(conn, cursor)


def test_view():
    pass
