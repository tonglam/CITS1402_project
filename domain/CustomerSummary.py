class CustomerSummary:
    def __init__(self, customerId, modelName, daysRented, taxYear, rentalCost, dateBack):
        self.customerId = customerId
        self.modelName = modelName
        self.daysRented = daysRented
        self.taxYear = taxYear
        self.rentalCost = rentalCost
        self.dateBack = dateBack

    def __str__(self):
        return self.customerId, self.modelName, self.daysRented, self.taxYear, self.rentalCost, self.dateBack

    def getCustomerId(self):
        return self.customerId

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def getModelName(self):
        return self.modelName

    def setModelName(self, modelName):
        self.modelName = modelName

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

    def getDateBack(self):
        return self.dateBack

    def setDateBack(self, dateBack):
        self.dateBack = dateBack
