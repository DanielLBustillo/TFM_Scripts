import requests
import mysql.connector
import datetime
import re

def convertirfecha(dato):
    format = '%Y-%m'
    datetime_obj = datetime.datetime.strptime(dato, format)
    return datetime_obj.strftime("%Y-%m-%d")

def strsplit(string, delimiter=',', ignore='"'):
    parts = list()
    index = 0
    next = 0
    while next < len(string):
        if string[next] == delimiter:
            parts.append(string[index:next])
            index = next+1
        elif string[next] == ignore:
            next = next+1
            while string[next] != ignore:
                next = next+1
            parts.append(string[index+1:next])
            next = next+1
            index = next+1
        next = next+1

    if index < next:
        parts.append(string[index:next])
    return parts

def insertarfunding(db, datos):
    print(datos)
    mycursor = db.cursor()
    linea = strsplit(datos)
    query = "SELECT * FROM db_melinda_bill WHERE `GRANT ID` = %s"
    parametros = (linea[0],)
    mycursor.execute(query, parametros)
    mycursor.fetchall()
    print(linea)
    if mycursor.rowcount == 0:
        query = "insert into db_melinda_bill values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        parametros = (linea[0], linea[1], linea[2], linea[3], convertirfecha(linea[4]), linea[5], linea[6], linea[7], linea[8], linea[9],linea[10], linea[11], linea[12])
        mycursor.execute(query, parametros)

#Lectura de las pasword de las bases de datos.
file1 = open('PS', 'r')
lines = file1.readlines()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user= lines[0],
    password= lines[1],
    database="Name_dataBase"
)

keywords = ["Tuberculosis", "COVID"]
fundingmelindabill = 'funding_melinda_bill.txt'
file1 = open(fundingmelindabill, 'w', encoding="utf-8")

url = "https://www.gatesfoundation.org/-/media/files/bmgf-grants.csv"
resp = requests.get(url)
csv = resp.text
csvlineas = csv.split("\n")
dictiorary = dict()

for k in keywords:
    dictiorary[k] = 0

for i in csvlineas:
    escribir = False
    for k in keywords:
        if k.lower() in i.lower():
            escribir = True
            dictiorary[k] = dictiorary[k]+1
    if escribir:
        file1.write(i)
        insertarfunding(mydb, i)

mydb.commit()

file1.close()
print(dictiorary)