CREATE TABLE Phone
(
    IMEI        TEXT,
    modelNumber TEXT,
    modelName   TEXT,
    PRIMARY KEY (IMEI),
    FOREIGN KEY (modelNumber, modelName) REFERENCES PhoneModel (modelNumber, modelName),
    CHECK (

                length(IMEI) == 15 and
                IMEI GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' and
                (
                        substr(IMEI, 1, 1) +
                        substr(IMEI, 3, 1) +
                        substr(IMEI, 5, 1) +
                        substr(IMEI, 7, 1) +
                        substr(IMEI, 9, 1) +
                        substr(IMEI, 11, 1) +
                        substr(IMEI, 13, 1) +
                        substr(IMEI, 15, 1) +
                        CASE
                            WHEN substr(IMEI, 2, 1) == '0' THEN 0
                            WHEN substr(IMEI, 2, 1) == '1' THEN 2
                            WHEN substr(IMEI, 2, 1) == '2' THEN 4
                            WHEN substr(IMEI, 2, 1) == '3' THEN 6
                            WHEN substr(IMEI, 2, 1) == '4' THEN 8
                            WHEN substr(IMEI, 2, 1) == '5' THEN 1
                            WHEN substr(IMEI, 2, 1) == '6' THEN 3
                            WHEN substr(IMEI, 2, 1) == '7' THEN 5
                            WHEN substr(IMEI, 2, 1) == '8' THEN 7
                            WHEN substr(IMEI, 2, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 4, 1) == '0' THEN 0
                            WHEN substr(IMEI, 4, 1) == '1' THEN 2
                            WHEN substr(IMEI, 4, 1) == '2' THEN 4
                            WHEN substr(IMEI, 4, 1) == '3' THEN 6
                            WHEN substr(IMEI, 4, 1) == '4' THEN 8
                            WHEN substr(IMEI, 4, 1) == '5' THEN 1
                            WHEN substr(IMEI, 4, 1) == '6' THEN 3
                            WHEN substr(IMEI, 4, 1) == '7' THEN 5
                            WHEN substr(IMEI, 4, 1) == '8' THEN 7
                            WHEN substr(IMEI, 4, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 6, 1) == '0' THEN 0
                            WHEN substr(IMEI, 6, 1) == '1' THEN 2
                            WHEN substr(IMEI, 6, 1) == '2' THEN 4
                            WHEN substr(IMEI, 6, 1) == '3' THEN 6
                            WHEN substr(IMEI, 6, 1) == '4' THEN 8
                            WHEN substr(IMEI, 6, 1) == '5' THEN 1
                            WHEN substr(IMEI, 6, 1) == '6' THEN 3
                            WHEN substr(IMEI, 6, 1) == '7' THEN 5
                            WHEN substr(IMEI, 6, 1) == '8' THEN 7
                            WHEN substr(IMEI, 6, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 8, 1) == '0' THEN 0
                            WHEN substr(IMEI, 8, 1) == '1' THEN 2
                            WHEN substr(IMEI, 8, 1) == '2' THEN 4
                            WHEN substr(IMEI, 8, 1) == '3' THEN 6
                            WHEN substr(IMEI, 8, 1) == '4' THEN 8
                            WHEN substr(IMEI, 8, 1) == '5' THEN 1
                            WHEN substr(IMEI, 8, 1) == '6' THEN 3
                            WHEN substr(IMEI, 8, 1) == '7' THEN 5
                            WHEN substr(IMEI, 8, 1) == '8' THEN 7
                            WHEN substr(IMEI, 8, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 10, 1) == '0' THEN 0
                            WHEN substr(IMEI, 10, 1) == '1' THEN 2
                            WHEN substr(IMEI, 10, 1) == '2' THEN 4
                            WHEN substr(IMEI, 10, 1) == '3' THEN 6
                            WHEN substr(IMEI, 10, 1) == '4' THEN 8
                            WHEN substr(IMEI, 10, 1) == '5' THEN 1
                            WHEN substr(IMEI, 10, 1) == '6' THEN 3
                            WHEN substr(IMEI, 10, 1) == '7' THEN 5
                            WHEN substr(IMEI, 10, 1) == '8' THEN 7
                            WHEN substr(IMEI, 10, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 12, 1) == '0' THEN 0
                            WHEN substr(IMEI, 12, 1) == '1' THEN 2
                            WHEN substr(IMEI, 12, 1) == '2' THEN 4
                            WHEN substr(IMEI, 12, 1) == '3' THEN 6
                            WHEN substr(IMEI, 12, 1) == '4' THEN 8
                            WHEN substr(IMEI, 12, 1) == '5' THEN 1
                            WHEN substr(IMEI, 12, 1) == '6' THEN 3
                            WHEN substr(IMEI, 12, 1) == '7' THEN 5
                            WHEN substr(IMEI, 12, 1) == '8' THEN 7
                            WHEN substr(IMEI, 12, 1) == '9' THEN 9
                            END +
                        CASE
                            WHEN substr(IMEI, 14, 1) == '0' THEN 0
                            WHEN substr(IMEI, 14, 1) == '1' THEN 2
                            WHEN substr(IMEI, 14, 1) == '2' THEN 4
                            WHEN substr(IMEI, 14, 1) == '3' THEN 6
                            WHEN substr(IMEI, 14, 1) == '4' THEN 8
                            WHEN substr(IMEI, 14, 1) == '5' THEN 1
                            WHEN substr(IMEI, 14, 1) == '6' THEN 3
                            WHEN substr(IMEI, 14, 1) == '7' THEN 5
                            WHEN substr(IMEI, 14, 1) == '8' THEN 7
                            WHEN substr(IMEI, 14, 1) == '9' THEN 9
                            END
                    )
                    % 10 == 0
        )
);

CREATE TABLE PhoneModel
(
    modelNumber TEXT,
    modelName   TEXT,
    storage     INTEGER,
    colour      TEXT,
    baseCost    REAL,
    dailyCost   REAL,
    PRIMARY KEY (modelNumber)
);

CREATE TABLE rentalContract
(
    customerId INTEGER,
    IMEI       TEXT,
    dateOut    TEXT,
    dateBack   TEXT,
    rentalCost REAL,
    PRIMARY KEY (customerId, IMEI),
    FOREIGN KEY (IMEI) REFERENCES Phone (IMEI) ON DELETE SET NULL,
    FOREIGN KEY (customerId) REFERENCES Customer (customerId)
);

CREATE TABLE Customer
(
    customerId    INTEGER,
    customerName  TEXT,
    customerEmail TEXT,
    PRIMARY KEY (customerId)
);