from databasepatientsanalisys.patientsmain import patientsmain
from seasonaddict.seasonmain import seasonmain

while(True):
    try:
        operation = int(input("Добро пожаловать. Выберите обработчик: 1 - рассчёт энтропии, 2 - рассчет сезонности\n 0 - завершение работы\n"))
        if(operation == 1):
            patientsmain()
        if operation == 2:
            seasonmain()
        if(operation == 0):
            break
    except:
        print("Не удалось распознать число")