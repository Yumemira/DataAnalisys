import math

from databasepatientsanalisys.DatabaseWorker import DatabaseWorker
from databasepatientsanalisys.Patient import Patient
import random
import pandas


def generatePatient() -> Patient:
    cholesterol = random.randint(100,1500) # будем считать, что нормальное количество холестерина 316-559(я не знаю, почему в базе данных из задания хранятся целые числа, так что помножил норму на 100)
    gender = random.randint(0, 1)
    diagnose = 0
    if(gender == 1):
        if(cholesterol<316 or cholesterol>559):
            diagnose = 1
    else:
        if(cholesterol<321 or cholesterol>564):
            diagnose = 1
    return Patient(gender, cholesterol, diagnose)

def getEntropy(data: list):
    count = 0
    for i in data:
        if i[2] == 1:
            count+=1

    p = count/len(data)
    p2 = (len(data)-count)/len(data)
    return p*math.log(p,2)+p2*math.log(p2,2)*(-1)


def patientsmain():
    dataset = list() # empty tuple for data
    patients = list()
    databaseworker = DatabaseWorker()  # class worked with database
    datacollector = int(input("Пожалуйста, выберите хранилище данных: 1 - переменная времени исполнения, 2 - база данных postgreSQL\n"))
    while(True):
        try:

            command = int(input("""Пожалуйста, выберите операцию: 1 - сгенерировать новую запись, 2 - заполнить список клиентов,\n
                                3 - показать таблицу, 4 - рассчитать начальную энтропию,\n
                                5 - разделить по полу и просчитать энтропию разницу с общей энтропией,\n
                                 0 - завершить работу\n"""))
            if(command==1):
                numberOfPatients = int(input("Введите количество новых пациентов, для отмены - 0\n"))
                if datacollector==2:
                    for i in range(0, numberOfPatients):
                        databaseworker.insertToDb(generatePatient())
                elif datacollector==1:
                    for i in range(0, numberOfPatients):
                        patients.append(generatePatient())
                print(f"Данные сгенерированы. {'\033[93m'}Не забудьте заполнить список клиентов выбрав операцию 2{'\033[0m'}")

            elif(command==2):
                if datacollector==2:
                    dataset = list(databaseworker.loadData())
                elif datacollector==1:
                    dataset = list()
                    i = 0
                    for patient in patients:
                        dataset.append([patient.getGender(), patient.getCholesterol(), patient.isDiagnosed(), i])
                        i+=1
                print(f"{'\033[92m'}Список клиентов обновлен{'\033[0m'}")
            elif(command==3):
                print(pandas.DataFrame(dataset,  columns=['пол','холестерин','болен','id']))
            elif(command==4):
                print(getEntropy(dataset))
            elif(command==5):
                if len(dataset) == 0:
                    print(f"{'\033[91m'}Список пациентов пуст. Вы заполнили список операцией 2?{'\033[0m'}")
                else:
                    boys=list()
                    girls=list()
                    for datapiece in dataset:
                        if(int(datapiece[0])==0):
                            boys.append(datapiece)
                        else:
                            girls.append(datapiece)
                    boysEntropy = getEntropy(boys)
                    girlsEntropy = getEntropy(girls)
                    print(f'Энтропия мужчин: {boysEntropy}.\n Энтропия женщин: {girlsEntropy}. \n Итоговое уменьшение энтропии: {getEntropy(dataset) - (boysEntropy+girlsEntropy)/2}')

            elif(command==0):
                break
        except:
            print("Не удалось распознать число")

    databaseworker.closeConnection()