CREATE VIEW CustomerSummary AS
SELECT a.customerId,
       c.modelName,
       julianday(a.dateBack) - julianday(a.dateOut) daysRented,
       CASE
           WHEN strftime('%m-%d', a.dateOut) >= '07-01' THEN strftime('%Y', a.dateOut) || '/' ||
                                                             strftime('%Y', a.dateOut, '+1 year', '-1 day')
           ELSE strftime('%Y', a.dateOut, '-1 year') || '/' || strftime('%Y', a.dateOut)
           END                                      taxYear,
       a.rentalCost
FROM rentalContract a
         JOIN Phone b USING (IMEI)
         JOIN PhoneModel c USING (modelNumber, modelName)
WHERE a.rentalCost IS NOT NULL;