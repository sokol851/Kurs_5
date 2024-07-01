import requests


class HHParser:
    """ Класс для работы с HeadHunter. """

    @staticmethod
    def __get_request(keywords) -> list[dict]:
        """ Получение списка работодателей по ключевым словам или топ. """
        keyword = keywords.replace(' ', '').split(',')
        list_list_vac = []
        for i in keyword:
            params = {'text': i, 'per_page': 10, 'sort_by': 'by_vacancies_open', 'only_with_vacancies': True}
            response = requests.get("https://api.hh.ru/employers", params=params)
            if response.status_code == 200:
                list_list_vac.append(response.json()['items'])
        list_vac = []
        for v in list_list_vac:
            for vac in v:
                if vac not in list_vac:
                    list_vac.append(vac)
        return list_vac

    def get_employers(self, keyword=None) -> list[dict]:
        """ Формирование списка работодателей для удобства. """
        employers = []
        data = self.__get_request(keyword)
        for employer in data:
            employers.append(
                {'id': employer['id'], "name": employer['name'], 'count_vac': employer['open_vacancies'],
                 'url': employer['alternate_url']})
        return employers

    @staticmethod
    def __get_vacancies_on_employer(employer_id) -> list[dict]:
        """ Получение списка вакансий от работодателей полученных в get_employers. """
        params = {'employer_id': employer_id, 'per_page': 100}
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_all_vacancies(self, keyword=None) -> list[dict]:
        """ Формирование списка вакансий для удобства. """
        employers = self.get_employers(keyword)
        all_vacancies = []
        for employer in employers:
            vacancies = self.__get_vacancies_on_employer(employer['id'])
            for vacancy in vacancies:
                if vacancy['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                    salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
                all_vacancies.append({'id': vacancy['id'],
                                      'name': vacancy['name'],
                                      'url': vacancy['alternate_url'],
                                      'salary_from': salary_from,
                                      'salary_to': salary_to,
                                      'employer': employer['name'],
                                      'area': vacancy['area']['name']
                                      })
        return all_vacancies
