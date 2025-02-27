class Patient:
    def __init__(self, gender, cholesterol, diagnosed):
        self.gender = gender
        self.cholesterol = cholesterol
        self.diagnosed = diagnosed

    def getGender(self):
        return self.gender

    def getCholesterol(self):
        return self.cholesterol

    def isDiagnosed(self):
        return self.diagnosed