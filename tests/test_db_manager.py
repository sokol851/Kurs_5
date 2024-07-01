import pytest
from src.db_manager import DBManager
from config import config
from utils.utils import create_database, create_tables
import psycopg2


@pytest.mark.usefixtures
def create_exemplar():
    return DBManager('test_db')


def test_create_db_and_table():
    create_database('test_db')
    create_tables('test_db')
    conn = psycopg2.connect(dbname='test_db', **config())
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO employers VALUES (1, 'ЮИТ', 2, 'hh.ru/id1');
            INSERT INTO employers VALUES (2, 'Пятёрочка', 1, 'hh.ru/id2')""")
        cur.execute(f"""
            INSERT INTO vacancies VALUES (1, 'Грузчик', 'hh.ru/url1', 50000, 60000, 'Москва', 'ЮИТ');
            INSERT INTO vacancies VALUES (2, 'Крановщик', 'hh.ru/url2', 40000, 50000, 'CПб', 'ЮИТ');
            INSERT INTO vacancies VALUES (3, 'Продавец', 'hh.ru/url3', 30000, 40000, 'Казань', 'Пятёрочка')""")
    conn.commit()
    conn.close()


def test_get_companies_and_vacancies_count():
    assert create_exemplar().get_companies_and_vacancies_count() == [('ЮИТ', 2), ('Пятёрочка', 1)]


def test_get_all_vacancies():
    assert create_exemplar().get_all_vacancies() == [(1, 'Грузчик', 'hh.ru/url1', 50000, 60000, 'Москва', 'ЮИТ'),
                                                     (2, 'Крановщик', 'hh.ru/url2', 40000, 50000, 'CПб', 'ЮИТ'),
                                                     (3, 'Продавец', 'hh.ru/url3', 30000, 40000, 'Казань', 'Пятёрочка')]


def test_get_avg_salary():
    assert create_exemplar().get_avg_salary() == 45000


def test_get_vacancies_with_higher_salary():
    assert create_exemplar().get_vacancies_with_higher_salary() == [
        (1, 'Грузчик', 'hh.ru/url1', 50000, 60000, 'Москва', 'ЮИТ')]


def test_get_vacancies_with_keyword():
    assert create_exemplar().get_vacancies_with_keyword('Грузчик') == [
        (1, 'Грузчик', 'hh.ru/url1', 50000, 60000, 'Москва', 'ЮИТ')]
    assert create_exemplar().get_vacancies_with_keyword('Продавец') == [
        (3, 'Продавец', 'hh.ru/url3', 30000, 40000, 'Казань', 'Пятёрочка')]


def test_delete_vacancies():
    create_exemplar().delete_vacancies('1')
    assert create_exemplar().get_all_vacancies() == [(2, 'Крановщик', 'hh.ru/url2', 40000, 50000, 'CПб', 'ЮИТ'),
                                                     (3, 'Продавец', 'hh.ru/url3', 30000, 40000, 'Казань', 'Пятёрочка')]


def test_clean_db():
    create_exemplar().clean_db()
    assert create_exemplar().get_all_vacancies() == []
