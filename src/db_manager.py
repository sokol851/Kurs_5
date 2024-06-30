import psycopg2
from config import config


class DBManager:
    """ Класс для работы с базой данных. """
    name: str

    def __init__(self, name):
        self.__name = name

    def __execute_query(self, query: str) -> list[set]:
        """ Открывает соединение с БД и закрывает после передачи запроса, выводит полученный результат. """
        conn = psycopg2.connect(dbname=self.__name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self) -> list:
        """ Получает список всех компаний и количество вакансий у каждой. """
        return self.__execute_query('SELECT name, count_vac FROM employers')

    def get_all_vacancies(self) -> list[set]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        return self.__execute_query('SELECT * FROM vacancies')

    def get_avg_salary(self) -> int:
        """ Получает среднюю зарплату по вакансиям. """
        avg_salary = self.__execute_query('SELECT AVG(salary_from) FROM vacancies')
        return round(*avg_salary[0])

    def get_vacancies_with_higher_salary(self) -> list[set]:
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
        return self.__execute_query(f'SELECT * FROM vacancies WHERE salary_from >= {self.get_avg_salary()}')

    def get_vacancies_with_keyword(self, keyword: str) -> list[set]:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. """
        keywords_lower = keyword.replace(' ', '').lower().split(',')
        keywords_title = keyword.replace(' ', '').title().split(',')
        list_vacancies = []
        for i in keywords_lower:
            list_vacancies.append(self.__execute_query(f"SELECT * FROM vacancies WHERE name LIKE '%{i}%'"))
        for i in keywords_title:
            list_vacancies.append(self.__execute_query(f"SELECT * FROM vacancies WHERE name LIKE '%{i}%'"))
        vac_list = []
        for vacancy in list_vacancies:
            for vac in vacancy:
                vac_list.append(vac)
        return vac_list

    def delete_vacancies(self, id_vacancy: str) -> None:
        """ Удаляет вакансию из БД по ID. """
        list_id = id_vacancy.replace(' ', '').lower().split(',')
        conn = psycopg2.connect(dbname=self.__name, **config())
        with conn:
            with conn.cursor() as cur:
                for id_vac in list_id:
                    cur.execute(f'DELETE FROM vacancies WHERE id = {id_vac}')
        conn.close()


if __name__ == "__main__":
    db = DBManager('data_kurs')
    # print(db.get_companies_and_vacancies_count())
    # print(db.get_all_vacancies())
    # print(db.get_avg_salary())
    # print(db.get_vacancies_with_higher_salary())
    # print(db.get_vacancies_with_keyword(input('Слово ввести')))
