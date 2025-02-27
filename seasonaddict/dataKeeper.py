import datetime
import random

from seasonaddict.DataFrame import DataFrame


class DataKeeper:

    def __init__(self):
        self.data = list()
        self.today = datetime.date(2020, 1, 1)

    def emulateYearOfLife(self, curve: float, intensivity: float, fertility: float, strengthCapacity: float):
        strength = 0.1
        defaultAmount = 10000

        for i in range(1, 365):
            if curve >= 0:
                self.data.append(DataFrame(self.today, defaultAmount*curve))
            else:
                self.data.append(DataFrame(self.today, 0))
            curve += intensivity * strength


            if(curve<2):
                if strength < strengthCapacity:
                    strength += random.random() * 0.3 * fertility
            else:
                if strength > -strengthCapacity:
                    strength -= random.random() * 0.3
            self.today += datetime.timedelta(days=1)

    def getData(self):
        return self.data

    def getToday(self):
        return self.today