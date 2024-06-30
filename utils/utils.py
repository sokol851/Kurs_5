import psycopg2
from src.parser import HHParser
from src.db_manager import DBManager
from config import config


def create_database(db_name):
    """ Создаёт базу данных с указанным названием. """
    conn = psycopg2.connect(dbname='postgres', **config())

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name):
    """ Создаёт таблицы в базе данных. """
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers
             (id INTEGER PRIMARY KEY,
             name VARCHAR(100) UNIQUE NOT NULL,
             count_vac INT NOT NULL,
             url VARCHAR(100) NOT NULL)
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
    """ Запись данных о вакансиях и работодателях в БД. """
    hh = HHParser()
    keyword = input('Введите ключевые слова для поиска в названии и описании компаний.\n'
                    'Или нажмите Enter, чтобы вывести компании с максимальным кол-вом вакансий.\n')
    employers = hh.get_employers(keyword)
    vacancies = hh.get_all_vacancies(keyword)
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""INSERT INTO employers VALUES (%s, %s, %s, %s)""",
                            (employer['id'], employer['name'], employer['count_vac'], employer['url']))
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
    """ Вывод вакансий в консоль для пользователя. """
    for i in vac_list:
        print(f'ID вакансии: {i[0]}\n'
              f'Вакансия: {i[1]}\n'
              f'Работодатель: {i[6]}\n'
              f'Заработная плата: от {i[3]} до {i[4]}\n'
              f'Местоположение: {i[5]}\n'
              f'Сcылка на ваканисию: {i[2]}\n')


def choice_menu():
    """ Меню для пользователя. """
    db = DBManager('data_kurs')
    print('Приветствую! Данное меню предназначено для работы с вакансиями на HeadHunter.ru')
    while True:
        print('\n1. Обновить БД вакансий по работодателям.\n'
              '2. Вывести список вакансий из БД.\n'
              '3. Получить список компаний и количество вакансий у каждой.\n'
              '4. Получить среднюю оплату по вакансиям в БД.\n'
              '5. Список вакансия в оплатой выше средней.\n'
              '6. Фильтр вакансий по ключевому слову.\n'
              '7. Удалить вакансию из БД по ID.\n'
              '8. Завершить работу.')
        number = input('Выберите необходимое действие (цифра от 1 до 8):\n')
        number = number.strip(' ')
        while not number.isdigit() or int(number) not in range(1, 9):
            print('Вы ввели неверный номер! Повторите:')
            number = input('Выберите необходимое действие (цифра от 1 до 8):\n')
            number = number.strip(' ')
        if int(number) == 1:
            create_database('data_kurs')
            create_tables('data_kurs')
            insert_data_in_tables('data_kurs')
        if int(number) == 2:
            output_vacancies_for_user(db.get_all_vacancies())
        if int(number) == 3:
            for i in db.get_companies_and_vacancies_count():
                print(f'Компания: {i[0]}\n'
                      f'Количество вакансий: {i[1]}\n')
        if int(number) == 4:
            print(f'Средняя заработная плата по выборке: {db.get_avg_salary()}')
        if int(number) == 5:
            print(db.get_vacancies_with_higher_salary())
        if int(number) == 6:
            output_vacancies_for_user(
                db.get_vacancies_with_keyword(input('Введите ключевые слова (можно несколько, через запятую): ')))
        if int(number) == 7:
            id_list = input('Введите ID вакансии для удаления из базы: ')
            db.delete_vacancies(id_list)
            print('Вакансия удалена.')
        if int(number) == 8:
            return print('Работа завершена!')


if __name__ == "__main__":
    # create_database('data_kurs')
    # create_tables('data_kurs')
    # insert_data_in_tables('data_kurs')
    db = DBManager('data_kurs')
    # choice_menu()
