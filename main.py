import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def main():
    load_dotenv()
    languages = os.getenv("LANGUAGES")
    languages_average_salary = {}

    def predict_rub_salary_hh():
        for language in languages:
            vacancies_processed = 0
            total_salary = 0
            base_api = "https://api.hh.ru"
            page = 0
            page_number = 1
            while page < page_number:
                params = {
                    'text': language,
                    'area': '1',
                    'only_with_salary': True,
                    'page': page
                        }
                response = requests.get(f'{base_api}/vacancies', params=params)
                response.raise_for_status()
                found_vacancies = response.json()
                for vacancy in found_vacancies['items']:
                    if vacancy['salary']['currency'] == 'RUR':
                        vacancies_processed += 1
                        total_salary += predict_rub_salary(payment_from=vacancy['salary']['from'],
                                                           payment_to=vacancy['salary']['to'])
                page += 1
                page_number = found_vacancies['pages']
            total_average_salary = int(total_salary / vacancies_processed)
            languages_average_salary[language] = {'vacancies found': found_vacancies['found'], 'vacancies_processed': vacancies_processed, 'average_salary': total_average_salary}
        return languages_average_salary

    def predict_rub_salary_sj():
        for language in languages:
            vacancies_processed = 0
            average_salary = 0
            total_salary = 0
            base_api = 'https://api.superjob.ru/2.0'
            secret_key_sj = os.getenv('SECRET_KEY')
            headers = {
                'X-Api-App-Id': secret_key_sj,
            }
            params = {
                'keyword': language,
                'town': 'Москва'
            }
            response = requests.get(f'{base_api}/vacancies', headers=headers, params=params)
            response.raise_for_status()
            found_vacancies = response.json()
            for vacancy in found_vacancies['objects']:
                if vacancy['currency'] == 'rub':
                    vacancies_processed += 1
                    total_salary += predict_rub_salary(payment_from=vacancy['payment_from'], payment_to=vacancy['payment_to'])
                    average_salary = int(total_salary/vacancies_processed)
            languages_average_salary[language] = {'vacancies found': found_vacancies['total'], 'vacancies_processed': vacancies_processed, 'average_salary': average_salary}
        return languages_average_salary

    def predict_rub_salary(payment_from: int, payment_to: int):
        if (payment_from == 0) or (payment_from is None):
            return payment_to*0.8
        elif (payment_to == 0) or (payment_to is None):
            return payment_from/1.2
        else:
            return (payment_from+payment_to)/2

    def print_result_table(vacancies_result: dict, title: str):
        salary_results_grouped = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
        for language, results in vacancies_result.items():
            salary_results_grouped.append([language] + [result for result in results.values()])
        salary_table = AsciiTable(salary_results_grouped, title)
        print(salary_table.table)

    predict_rub_salary_hh()
    print_result_table(vacancies_result=predict_rub_salary_hh(), title='Headhunter Moscow')
    print_result_table(vacancies_result=predict_rub_salary_sj(), title='Superjob Moscow')


if __name__ == '__main__':
    main()