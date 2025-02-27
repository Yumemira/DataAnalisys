

class DataFrame:
    def __init__(self, date, amount: int):
        self.date = date
        self.amount = amount

    def getDate(self):
        return self.date

    def getAmount(self):
        return self.amount
