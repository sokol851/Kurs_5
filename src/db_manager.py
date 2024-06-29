import psycopg2
from config import config


class DBManager:

    def __init__(self, name):
        self.__name = name

    def __execute_query(self, query):
        conn = psycopg2.connect(dbname=self.__name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании. """
        return self.__execute_query('SELECT employer, COUNT(*) FROM vacancies GROUP BY employer')

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        return self.__execute_query('SELECT * FROM vacancies')

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям. """
        avg_salary = self.__execute_query('SELECT AVG(salary_from) FROM vacancies')
        return round(*avg_salary[0])

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
        return self.__execute_query('SELECT * FROM vacancies WHERE salary_from >= 73792')

    def get_vacancies_with_keyword(self, keyword):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. """
        keywords_lower = keyword.replace(' ', '').lower().split(',')
        keywords_title = keyword.replace(' ', '').title().split(',')
        vac = []
        for i in keywords_lower:
            if i not in vac:
                vac.append(self.__execute_query(f"SELECT * FROM vacancies WHERE name LIKE '%{i}%'"))
        for i in keywords_title:
            if i not in vac:
                vac.append(self.__execute_query(f"SELECT * FROM vacancies WHERE name LIKE '%{i}%'"))
        return vac


if __name__ == "__main__":
    db = DBManager('data_kurs')
    # print(db.get_companies_and_vacancies_count())
    # print(db.get_all_vacancies())
    # print(db.get_avg_salary())
    # print(db.get_vacancies_with_higher_salary())
    # print(db.get_vacancies_with_keyword(input('Слово ввести')))
