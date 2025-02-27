import os
from databasepatientsanalisys.Patient import Patient
from dotenv import load_dotenv
import psycopg

load_dotenv()

class DatabaseWorker:
    def __init__(self):
        self.openConnection()
        # self.cursor = self.connection.cursor()

    def insertToDb(self, patient: Patient):
        cursor = self.connection.cursor()
        data = (patient.getGender(), patient.getCholesterol(), patient.isDiagnosed())
        cursor.execute("INSERT into public.patient_data (gender, cholesterol, diagnosed) VALUES (%s, %s, %s)",
                        data)
        self.connection.commit()

    def loadData(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from public.patient_data")
        return cursor.fetchall()


    def openConnection(self):
        self.connection = psycopg.connect(dbname=os.getenv("DATABASENAME"),
                                          user=os.getenv("LOGIN"),
                                          password=os.getenv("PASS"),
                                          host=os.getenv("HOST"), port=os.getenv("PORT"))
        return self.connection
    def closeConnection(self):
        self.connection.close()