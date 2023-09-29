class rentalContract:

    def __init__(self, customerId, IMEI, dateOut, dateBack, rentalCost):
        self.customerId = customerId
        self.IMEI = IMEI
        self.dateOut = dateOut
        self.dateBack = dateBack
        self.rentalCost = rentalCost

    def __str__(self):
        return self.customerId, self.IMEI, self.dateOut, self.dateBack, self.rentalCost

    def getCustomerId(self):
        return self.customerId

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def getIMEI(self):
        return self.IMEI

    def setIMEI(self, IMEI):
        self.IMEI = IMEI

    def getDateOut(self):
        return self.dateOut

    def setDateOut(self, dateOut):
        self.dateOut = dateOut

    def getDateBack(self):
        return self.dateBack

    def setDateBack(self, dateBack):
        self.dateBack = dateBack

    def getRentalCost(self):
        return self.rentalCost

    def setRentalCost(self, rentalCost):
        self.rentalCost = rentalCost
