import Constants
import sqlite3


def test_schema():
    conn = sqlite3.connect(Constants.database_name)
    cursor = conn.cursor()
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
    conn.close()
    cursor.close()


def test_data():
    print(1)
