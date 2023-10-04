import random
import sqlite3
import pytest

import constants
from tools.imei import generate_imei
from datetime import datetime, timedelta
from domain.CustomerSummary import CustomerSummary


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
                # check ON_DELETE
                if row[3] == "IMEI" and row[4] == "IMEI":
                    assert row[6] == "SET NULL"


def check_primary_key(conn, cursor):
    # check Phone primary key
    cursor.execute('SELECT * FROM Phone')
    conn.commit()
    phone_list = cursor.fetchall()
    phone_test = phone_list[14]
    try:
        cursor.execute('''
                       INSERT INTO Phone (modelNumber, modelName, IMEI)
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
    foreign_key_flag = False
    while not foreign_key_flag:
        cursor.execute("PRAGMA foreign_keys")
        conn.commit()
        if cursor.fetchall()[0][0]:
            foreign_key_flag = True
        else:
            cursor.execute("PRAGMA foreign_keys = ON")
            conn.commit()
    # check Phone foreign key
    cursor.execute('SELECT * FROM Phone')
    conn.commit()
    phone_list = cursor.fetchall()
    new_imei = generate_imei()

    phone_test = ('99' + phone_list[14][0], phone_list[14][1], new_imei)
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                          INSERT INTO Phone (modelNumber, modelName, IMEI)
                          VALUES (?, ?, ?)
                      ''', phone_test)
        conn.commit()
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test 1:' + str(e))

    phone_test = (phone_list[14][0], '99' + phone_list[14][1], new_imei)
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                         INSERT INTO Phone (modelNumber, modelName, IMEI)
                         VALUES (?, ?, ?)
                     ''', phone_test)
        conn.commit()
        raise Exception("test Phone foreign key failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone foreign key test 2:' + str(e))

    phone_test = ('99' + phone_list[14][0], '99' + phone_list[14][1], new_imei)
    print("Phone foreign key test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                        INSERT INTO Phone (modelNumber, modelName, IMEI)
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
    imei = phone_list[7][2]

    # length of IMEI should be 15
    new_imei = imei[0:7]
    phone_test = (phone_list[7][0], phone_list[7][1], new_imei)
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                       INSERT INTO Phone (modelNumber, modelName, IMEI)
                       VALUES (?, ?, ?)
                       ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 1:' + str(e))

    # IMEI should be all digits
    new_imei = imei[0:14] + 'A'
    phone_test = (phone_list[7][0], phone_list[7][1], new_imei)
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                           INSERT INTO Phone (modelNumber, modelName, IMEI)
                           VALUES (?, ?, ?)
                           ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 2:' + str(e))

    # IMEI should be meet the validation
    new_imei = str(int(imei) - 1)
    phone_test = (phone_list[7][0], phone_list[7][1], new_imei)
    print("Phone key constraints test data:{}".format(phone_test.__str__()))
    try:
        cursor.execute('''
                              INSERT INTO Phone (modelNumber, modelName, IMEI)
                              VALUES (?, ?, ?)
                              ''', phone_test)
        conn.commit()
        raise Exception("test Phone key constraints failed, record should not be inserted")
    except sqlite3.Error as e:
        print('pass Phone key constraints test 3:' + str(e))


def check_trigger_exists(conn, cursor):
    cursor.execute("SELECT count(1) FROM sqlite_master WHERE type='trigger' AND tbl_name = 'rentalContract' ")
    conn.commit()
    rows = cursor.fetchall()
    # this program has set up a trigger for rentalContract table
    assert rows[0][0] > 1, "trigger does not exist"


def trigger_rental_cost(conn, cursor, number=1):
    cursor.execute('SELECT * FROM rentalContract WHERE rentalCost IS NULL')
    rental_contract_list = cursor.fetchall()
    for i in range(number):
        sample = random.sample(range(len(rental_contract_list)), number)[0]
        trigger_rental_one_cost(conn, cursor, rental_contract_list[sample])


def trigger_rental_one_cost(conn, cursor, rental_contract):
    customer_id = rental_contract[0]
    imei = rental_contract[1]
    date_out = rental_contract[2]
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
    # check result
    check_trigger_result(conn, cursor)


def check_trigger_result(conn, cursor):
    # check trigger times
    cursor.execute("SELECT * FROM rentalContract WHERE rentalCost IS NOT NULL ")
    conn.commit()
    rental_list = cursor.fetchall()
    rental_count = len(rental_list)
    cursor.execute("SELECT count(1) FROM trigger_monitor ")
    conn.commit()
    monitor_count = cursor.fetchall()[0][0]
    assert rental_count == monitor_count, "trigger times error, check the record manually to find out why"
    # check trigger result
    for x in rental_list:
        imei = x[1]
        rental_cost = x[4]
        cursor.execute(
            "SELECT b.baseCost, b.dailyCost FROM Phone a JOIN PhoneModel b USING (modelNumber, modelName) WHERE IMEI = ? ",
            (imei,))
        conn.commit()
        rows = cursor.fetchall()
        expect_rental_cost = rows[0][0] + rows[0][1] * (
                datetime.strptime(x[3], "%Y-%m-%d") - datetime.strptime(x[2], "%Y-%m-%d")).days
        assert rental_cost == expect_rental_cost, "trigger result error, expect rental cost is {}, actual rental cost is {}".format(
            expect_rental_cost, rental_cost)


def trigger_duplicate_rental_cost(conn, cursor):
    cursor.execute('SELECT * FROM rentalContract WHERE rentalCost IS NOT NULL')
    conn.commit()
    rental_contract_all_list = cursor.fetchall()
    rental_contract_key_set = set([str(x[0]) + "+" + x[1] for x in rental_contract_all_list])
    sample_index = random.sample(range(len(rental_contract_all_list)), 30)
    rental_contract_list = [rental_contract_all_list[x] for x in sample_index]
    duplicate_list = []
    for rental_contract in rental_contract_list:
        # duplicate times
        customer_id = rental_contract[0]
        imei = rental_contract[1]
        date_out = rental_contract[2]
        duplicate_times = random.randint(1, 10)
        for i in range(duplicate_times):
            key = str(customer_id) + "+" + imei
            if key in rental_contract_key_set:
                continue
            duplicate_list.append((customer_id, imei, date_out, None, None))
    # insert
    cursor.executemany('''
                       INSERT INTO rentalContract (customerId, IMEI, dateOut, dateBack, rentalCost)
                       VALUES (?, ?, ?, ?, ?)
                   ''', duplicate_list)
    conn.commit()
    # update
    for x in duplicate_list:
        customer_id = x[0]
        imei = x[1]
        date_out = x[2]
        rent_day = random.randint(1, 100)
        date_back = (datetime.strptime(date_out, "%Y-%m-%d") + timedelta(days=rent_day)).strftime("%Y-%m-%d")
        cursor.execut("UPDATE rentalContract SET dateBack = ? WHERE customerId = ? AND IMEI = ?",
                      (date_back, customer_id, imei))
        conn.commit()


def check_view(conn, cursor):
    # select all valid rental contract records
    cursor.execute('''
                    SELECT a.*, b.modelName FROM rentalContract a, Phone b 
                    WHERE a.IMEI = b.IMEI AND a.dateBack IS NOT NULL
                    ''')
    conn.commit()
    summary_dict = {}
    valid_list = []
    for x in cursor.fetchall():
        customer_id = x[0]
        date_out = x[2]
        date_back = x[3]
        rental_cost = x[4]
        model_name = x[5]
        # calculate rent days
        rent_days = (datetime.strptime(date_back, "%Y-%m-%d") - datetime.strptime(date_out, "%Y-%m-%d")).days
        # get tax year
        tax_year = get_tax_year(datetime.strptime(date_back, "%Y-%m-%d"))
        # summary data
        customer_summary = CustomerSummary(
            customer_id,
            model_name,
            date_out,
            date_back,
            rent_days,
            tax_year,
            rental_cost
        )
        valid_list.append(customer_summary)
    for x in valid_list:
        key = str(x.customerId) + '+' + x.modelName + "+" + x.taxYear
        if key in summary_dict:
            old = summary_dict[key]
            new = CustomerSummary(
                x.customerId,
                x.modelName,
                x.dateOut,
                x.dateBack,
                old.daysRented + x.daysRented,
                x.taxYear,
                old.rentalCost + x.rentalCost
            )
            summary_dict[key] = new
        else:
            summary_dict[key] = x
    # get data from view
    cursor.execute("SELECT * FROM customerSummary")
    view_list = cursor.fetchall()
    # check length
    assert len(summary_dict) == len(view_list), "view data error, check the record manually to find out why"
    # check data
    for x in view_list:
        key = str(x[0]) + '+' + x[1] + '+' + x[3]
        summary = summary_dict[key]
        print("view test data:{}".format(summary.__str__()))
        assert summary.customerId == x[
            0], "view data customerId error, key:[{}], check the record manually to find out why".format(key)
        assert summary.modelName == x[
            1], "view data modelName error, key:[{}], check the record manually to find out why".format(key)
        assert summary.daysRented == x[
            2], "view data days rented error, key:[{}], check the record manually to find out why".format(key)
        assert summary.taxYear == x[
            3], "view data taxYear error, key:[{}], check the record manually to find out why".format(key)
        assert summary.rentalCost == x[
            4], "view data rentalCost error, key:[{}], check the record manually to find out why".format(key)


def get_tax_year(date):
    year = date.year
    month = date.month
    if month < 7:
        return "{}/{}".format(year - 1, str(year)[2:4])
    else:
        return "{}/{}".format(year, str(year + 1)[2:4])


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
    check_primary_key(conn, cursor)
    # check foreign key
    check_foreign_key(conn, cursor)
    # check key constraints
    check_key_constraints(conn, cursor)
    cursor.close()
    conn.close()


def test_trigger():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    # check trigger exists
    check_trigger_exists(conn, cursor)
    # trigger one record
    trigger_rental_cost(conn, cursor)
    # trigger 50 records
    trigger_rental_cost(conn, cursor, 50)
    # trigger duplicate records
    trigger_duplicate_rental_cost(conn, cursor)
    cursor.close()
    conn.close()


def test_view():
    conn = sqlite3.connect(constants.database_name)
    cursor = conn.cursor()
    check_view(conn, cursor)
    cursor.close()
    conn.close()


def test():
    print('\nstart 1402 project test\n')
    test_schema()
    test_data()
    test_trigger()
    test_view()
    print('\nCongratulations!!!!\n')
    print('pass 1402 project test\n')
