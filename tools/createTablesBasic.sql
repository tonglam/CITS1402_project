CREATE TABLE PhoneModel (
  modelNumber TEXT,
  modelName TEXT,
  storage INTEGER,
  colour TEXT,
  baseCost REAL,
  dailyCost REAL
);

CREATE TABLE Customer (
  customerId INTEGER,
  customerName TEXT,
  customerEmail TEXT
);

CREATE TABLE Phone (
  modelNumber TEXT,
  modelName TEXT,
  IMEI TEXT
);

CREATE TABLE rentalContract (
    customerId INTEGER,
    IMEI  TEXT,
    dateOut TEXT,
    dateBack TEXT,
    rentalCost REAL
);
