import pandas
from statsmodels.tsa.statespace.sarimax import SARIMAX

class SarimaSuggest:
    def __init__(self):
        pass

    def doTraining(self, data: list, steps):
        daily_sales = pandas.DataFrame(data)
        traindata = daily_sales.iloc[:-steps]
        model = SARIMAX(traindata,
                        order=(1, 1, 1),
                        seasonal_order=(1, 1, 1, 12),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        self.steps = steps
        self.trained = model.fit()

    def doSuggest(self, date, steps):
        try:
            suggest = self.trained.get_forecast(steps=steps)
            result = list()
            for suggestion in suggest.predicted_mean:
                result.append(int(suggestion))

            suggest_index = pandas.date_range(start=date, periods=steps+1, freq='D')[1:]
            return pandas.DataFrame(result, index=suggest_index, columns=['Predicted Sales'])
        except:
            print("Ваша модель не была обучена")
            return 0