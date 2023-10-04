class CustomerSummary:
    def __init__(self, customerId, modelName, dateOut, dateBack, daysRented, taxYear, rentalCost):
        self.customerId = customerId
        self.modelName = modelName
        self.dateOut = dateOut
        self.dateBack = dateBack
        self.daysRented = daysRented
        self.taxYear = taxYear
        self.rentalCost = rentalCost

    def __str__(self):
        return ("customerId:{}, modelName:{}, dateOut:{}, dateBack:{}, daysRented:{}, taxYear:{}, rentalCost:{}"
                .format(self.customerId, self.modelName, self.dateOut, self.dateBack, self.daysRented, self.taxYear,
                        self.rentalCost))

    def getCustomerId(self):
        return self.customerId

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def getModelName(self):
        return self.modelName

    def setModelName(self, modelName):
        self.modelName = modelName

    def getDateOut(self):
        return self.dateOut

    def setDateOut(self, dateOut):
        self.dateOut = dateOut

    def getDateBack(self):
        return self.dateBack

    def setDateBack(self, dateBack):
        self.dateBack = dateBack

    def getDaysRented(self):
        return self.daysRented

    def setDaysRented(self, daysRented):
        self.daysRented = daysRented

    def getTaxYear(self):
        return self.taxYear

    def setTaxYear(self, taxYear):
        self.taxYear = taxYear

    def getRentalCost(self):
        return self.rentalCost

    def setRentalCost(self, rentalCost):
        self.rentalCost = rentalCost
