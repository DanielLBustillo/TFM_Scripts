import requests
import mysql.connector
import re

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

def insertareconomic(db, datos):
    print(datos)
    mycursor = db.cursor()
    linea = strsplit(datos)
    query = "TRUNCATE TABLE economicpestel"
    mycursor.execute(query)
    print(linea)

    sql_insert = "INSERT INTO economicpestel VALUES({0})"
    ####56 es el valor de las columnas de la tabla
    wildcard = "%s," * 56 + "%s"
    sql_insert = sql_insert.format(wildcard)

    parametros = [linea[i] for i in range(len(linea))]
    parametros = tuple(parametros)

    mycursor.execute(query, parametros)



if __name__ == "__main__":

    url = "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2021/WEOOct2021all.ashx"

    local_filename = 'pestel.economic.xls'

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    file1 = open(local_filename, 'r', encoding="utf-8")
    lines = file1.readlines()

    for line in lines[1:]:

        insertareconomic(mydb, line)
