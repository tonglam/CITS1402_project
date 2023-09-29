class Customer:
    def __init__(self, customerId, customerName, customerEmail):
        self.customerId = customerId
        self.customerName = customerName
        self.customerEmail = customerEmail

    def __str__(self):
        return self.customerId, self.customerName, self.customerEmail

    def getCustomerId(self):
        return self.customerId

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def getCustomerName(self):
        return self.customerName

    def setCustomerName(self, customerName):
        self.customerName = customerName

    def getCustomerEmail(self):
        return self.customerEmail

    def setCustomerEmail(self, customerEmail):
        self.customerEmail = customerEmail
