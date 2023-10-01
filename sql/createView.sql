CREATE VIEW CustomerSummary AS
SELECT a.customerId,
       c.modelName,
       julianday(a.dateBack) - julianday(a.dateOut) daysRented,
       CASE
           WHEN strftime('%m-%d', a.dateBack) < '07-01' THEN strftime('%Y', a.dateBack, '-1 year') || '/' ||
                                                            substr(strftime('%Y', a.dateBack), 3)
           ELSE strftime('%Y', a.dateBack) || '/' || substr(strftime('%Y', a.dateBack, '+1 year'), 3)
           END                                      taxYear,
       a.rentalCost
FROM rentalContract a
         JOIN Phone b USING (IMEI)
         JOIN PhoneModel c USING (modelNumber, modelName)
WHERE a.dateBack IS NOT NULL;