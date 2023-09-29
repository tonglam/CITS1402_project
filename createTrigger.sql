CREATE TRIGGER calRentalCost
    AFTER UPDATE
    ON rentalContract
    FOR EACH ROW
BEGIN
    UPDATE rentalContract
    SET rentalCost = (SELECT baseCost + dailyCost * (julianday(NEW.dateBack) - julianday(dateOut))
                      FROM PhoneModel
                      WHERE PhoneModel.modelNumber = (SELECT modelNumber
                                                      FROM Phone
                                                      WHERE IMEI = NEW.IMEI)
                        AND PhoneModel.modelName = (SELECT modelName
                                                    FROM Phone
                                                    WHERE IMEI = NEW.IMEI))
    WHERE customerId = NEW.customerId
      AND IMEI = NEW.IMEI AND dateBack IS NULL;
END;