from seasonaddict.SarimaSuggest import SarimaSuggest
from seasonaddict.dataKeeper import DataKeeper
from dateutil.relativedelta import relativedelta
import pandas

def calculateAveregeNum(data: list):
    sum = 0
    for num in data:
        sum+=num
    return sum/len(data)

def seasonmain():
    dataKeeper = DataKeeper()
    sarima = SarimaSuggest()
    separateByMonth = {}
    while(True):
        command = int(input("""Пожалуйста, выберите операцию: 1 эмулировать год жизни, 2 показать список продаж\n
        3 рассчитать месячный сезонный индекс, 4 предсказать следующие месяцы\n
        5 обучение SARIMA, 6 предсказание с помощью SARIMA\n 
        0 завершить работу обработчика\n"""))
        if(command == 1):
            curve = float(input("Введите дробное число от 0 до 1 - текущий уровень дохода, чем он больше, тем успеешнее день, значение стремится к 1\n"))
            intensivity = float(input("Выберите интенсивность изменения цены, можно указать как 0.1 так и 10\n"))
            fertility = float(input("Введите урожайность этого года, чем больше значение тем больше прирост положительной тенденции\n"))
            strCapacity = float(input("Введите ограничители силы изменения кривой(0.5 рекомендуется)\n"))
            dataKeeper.emulateYearOfLife(curve, intensivity, fertility, strCapacity)
            print(f"{'\033[92m'}Данные заполнены, вы можете ознакомиться с ними, выбрав операцию 2{'\033[0m'}")
        if(command == 2):
            bakedData = list()
            for data in dataKeeper.getData():
                bakedData.append([data.getDate(), int(data.getAmount())])
            print(pandas.DataFrame(bakedData, columns=['Дата', 'Количество продаж']))
        if(command == 3):
            separateByMonth = {}
            printData = list()
            allOrders = list()

            for frame in dataKeeper.getData():
                allOrders.append(frame.getAmount())
                if separateByMonth.get(f"{frame.getDate().year}:{frame.getDate().month}", 'none')=='none':
                    separateByMonth[f"{frame.getDate().year}:{frame.getDate().month}"] = list()
                separateByMonth.get(f"{frame.getDate().year}:{frame.getDate().month}").append(frame.getAmount())

            for key in separateByMonth:
                printData.append([key, int(calculateAveregeNum(separateByMonth.get(key))), calculateAveregeNum(separateByMonth.get(key))/calculateAveregeNum(allOrders)])
                separateByMonth[key] = [calculateAveregeNum(separateByMonth.get(key)), calculateAveregeNum(separateByMonth.get(key))/calculateAveregeNum(allOrders)]

            print(pandas.DataFrame(printData, columns=['Месяц и год', 'Средние продажи', 'сезонный индекс']))
        if command == 4:
            suggestionData = list()
            monthsAmount = int(input("Введите количество месяцев для предсказания(но не более 12)\n"))
            for months in range(1, monthsAmount+1):
                suggestionDate = dataKeeper.getToday() + relativedelta(months=months)
                suggestionIndex = 0
                amount = 0
                year = suggestionDate.year-1
                while separateByMonth.get(f"{year}:{suggestionDate.month}", "none") != "none":
                    suggestionIndex += separateByMonth.get(f"{year}:{suggestionDate.month}")[1]
                    amount += 1
                    year -= 1
                try:
                     suggestionData.append([f"{suggestionDate.month}.{suggestionDate.year}",suggestionIndex/amount])
                except:
                    print(f"{suggestionDate.month}.{suggestionDate.year} - Данный месяц невозможно предсказать имея текущие данные")

            print(pandas.DataFrame(suggestionData, columns=['Месяц и год', 'предполагаемый сезонный индекс']))
        if command == 5:
            steps = int(input("Выберите количество данных для обучения\n"))
            allOrders = list()
            for frame in dataKeeper.getData():
                allOrders.append(int(frame.getAmount()))
            sarima.doTraining(allOrders, steps)
        if command == 6:
            steps = int(input("Выберите количество дней для предсказания\n"))
            print(sarima.doSuggest(dataKeeper.getToday(), steps).head())
        if command == 0:
            break