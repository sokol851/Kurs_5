import psycopg2
from src.parser import HHParser
from src.db_manager import DBManager
from config import config


def create_database(db_name):
    conn = psycopg2.connect(dbname='postgres', **config())

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers
             (id INTEGER PRIMARY KEY,
             name VARCHAR(100) UNIQUE NOT NULL)
             """)
            cur.execute("""CREATE TABLE vacancies
             (id INTEGER PRIMARY KEY,
             name VARCHAR(100) NOT NULL,
             url VARCHAR(100) NOT NULL,
             salary_from INTEGER,
             salary_to INTEGER,
             area VARCHAR(100) NOT NULL,
             employer VARCHAR(100) REFERENCES employers(name))
            """)
    conn.close()


def insert_data_in_tables(db_name):
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.get_all_vacancies()
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""INSERT INTO employers VALUES (%s, %s)""", (employer['id'], employer['name']))
            for vacancy in vacancies:
                cur.execute("""INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (vacancy['id'],
                             vacancy['name'],
                             vacancy['url'],
                             vacancy['salary_from'],
                             vacancy['salary_to'],
                             vacancy['area'],
                             vacancy['employer']))
    conn.close()


def output_vacancies_for_user(vac_list):
    for i in vac_list:
        print(f'ID вакансии: {i[0]}\n'
              f'Вакансия: {i[1]}\n'
              f'Работодатель: {i[6]}\n'
              f'Заработная плата: от {i[3]} до {i[4]}\n'
              f'Местоположение: {i[5]}\n'
              f'Сcылка на ваканисию: {i[2]}\n')


def choice_menu():
    db = DBManager('data_kurs')
    print('Приветствую! Данное меню предназначено для работы с вакансиями на HeadHunter.ru')
    while True:
        print('\n1. Вывести список всех вакансий.\n'
              '2. Добавить вакансию по URL.\n'
              '3. Удалить вакансию по URL.\n'
              '4. Просмотр сохранённого списка.\n'
              '5. Фильтр вакансий по ключевому слову.\n'
              '6. Фильтр вакансий по заработной плате.\n'
              '7. Фильтр вакансий по городу.\n'
              '8. Сортировка вакансий по заработной плате (По возрастанию).\n'
              '9. Сортировка вакансий по заработной плате (По убыванию).\n'
              '10. Очистка сохранённого списка.\n'
              '11. Завершить работу.')
        number = input('Выберите необходимое действие (цифра от 1 до 11):\n')
        number = number.strip(' ')
        while not number.isdigit() or int(number) not in range(1, 12):
            print('Вы ввели неверный номер! Повторите:')
            number = input('Выберите необходимое действие (цифра от 1 до 11):\n')
            number = number.strip(' ')
        if int(number) == 1:
            output_vacancies_for_user(db.get_all_vacancies())


if __name__ == "__main__":
    # create_database('data_kurs')
    # create_tables('data_kurs')
    # insert_data_in_tables('data_kurs')
    # output_vacancies_for_user([(1, 'a', 'lol'), (2, 'b', 'kek')])
    # db = DBManager('data_kurs')
    choice_menu()
