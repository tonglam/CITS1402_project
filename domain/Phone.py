class Phone:

    def __init__(self, IMEI, modelNumber, modelName):
        self.IMEI = IMEI
        self.modelNumber = modelNumber
        self.modelName = modelName

    def __str__(self):
        return self.IMEI, self.modelNumber, self.modelName

    def getIMEI(self):
        return self.IMEI

    def setIMEI(self, IMEI):
        self.IMEI = IMEI

    def getModelNumber(self):
        return self.modelNumber

    def setModelNumber(self, modelNumber):
        self.modelNumber = modelNumber

    def getModelName(self):
        return self.modelName

    def setModelName(self, modelName):
        self.modelName = modelName
