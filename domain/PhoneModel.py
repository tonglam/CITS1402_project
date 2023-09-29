class PhoneModel:

    def __init__(self, modelNumber, modelName, storage, colour, baseCost, dailyCost):
        self.modelNumber = modelNumber
        self.modelName = modelName
        self.storage = storage
        self.colour = colour
        self.baseCost = baseCost
        self.dailyCost = dailyCost

    def __str__(self):
        return self.modelNumber, self.modelName, self.storage, self.colour, self.baseCost, self.dailyCost

    def getModelNumber(self):
        return self.modelNumber

    def setModelNumber(self, modelNumber):
        self.modelNumber = modelNumber

    def getModelName(self):
        return self.modelName

    def setModelName(self, modelName):
        self.modelName = modelName

    def getStorage(self):
        return self.storage

    def setStorage(self, storage):
        self.storage = storage

    def getColour(self):
        return self.colour

    def setColour(self, colour):
        self.colour = colour

    def getBaseCost(self):
        return self.baseCost

    def setBaseCost(self, baseCost):
        self.baseCost = baseCost

    def getDailyCost(self):
        return self.dailyCost

    def setDailyCost(self, dailyCost):
        self.dailyCost = dailyCost
