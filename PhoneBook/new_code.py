import psycopg2
import csv
import os

config = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Muhammed4ever")
current = config.cursor()

current.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone_number VARCHAR(20)
);
""")
config.commit()

def insert():
    insert_table = "INSERT INTO contacts VALUES(%s, %s, %s);"
    count = int(input('1 если хотите ввести через терминал, 2 иначе: '))
    if count == 1:
        last_name = input("Введите имя: ")
        first_name = input("Введите фамилию: ")
        phone_number = input("Введите номер телефона: ")
        current.execute(insert_table, (last_name, first_name, phone_number))
        config.commit()
    if count == 2:
        if os.path.exists("example.csv"):
            with open("example.csv", "r", encoding="utf-8") as file:
                f = csv.reader(file, delimiter=",")
                for row in f:
                    if len(row) == 3:
                        current.execute(insert_table, row)
                config.commit()
        else:
            print("Файл example.csv не найден!")

def delete():
    delete_q = "DELETE FROM contacts WHERE last_name = %s;"
    last_name = input("Введите имя: ")
    current.execute(delete_q, (last_name,))
    config.commit()

def update():
    update_q = "UPDATE contacts SET phone_number = %s WHERE last_name = %s;"
    last_name = input("Введите имя: ")
    phone_number = input("Введите номер: ")
    current.execute(update_q, (phone_number, last_name))
    config.commit()

def select():
    select_q = "SELECT * FROM contacts;"
    current.execute(select_q)
    print(current.fetchall(), sep='\n')
    config.commit()

while True:
    command = input("insert,update,delete,select,exit: \n")
    if command == 'insert':
        insert()
    if command == 'delete':
        delete()
    if command == 'update':
        update()
    if command == 'select':
        select()
    if command == 'exit':
        break

current.close()
config.commit()
config.close()