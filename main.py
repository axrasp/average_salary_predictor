import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_salary_statistics_hh(language: str):
    vacancies_processed = 0
    total_salary = 0
    vacancies_not_found = {'vacancies found': 0,
                           'vacancies_processed': 0,
                           'average_salary': 0}
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
        if not found_vacancies['items']:
            return vacancies_not_found
        for vacancy in found_vacancies['items']:
            if vacancy['salary']['currency'] == 'RUR':
                salary = predict_rub_salary(
                        payment_from=vacancy['salary']['from'],
                        payment_to=vacancy['salary']['to'])
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
        if not vacancies_processed:
            average_salary = 0
        else:
            average_salary = int(total_salary / vacancies_processed)
        page += 1
        page_number = found_vacancies['pages']
    average_salary_results = {'vacancies found': found_vacancies['found'],
                              'vacancies_processed': vacancies_processed,
                              'average_salary': average_salary}
    return average_salary_results


def get_salary_statistics_sj(language: str, secret_key: str):
    vacancies_processed = 0
    total_salary = 0
    base_api = 'https://api.superjob.ru/2.0'
    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'keyword': language,
        'town': 'Москва'
    }
    response = requests.get(f'{base_api}/vacancies',
                            headers=headers,
                            params=params)
    response.raise_for_status()
    found_vacancies = response.json()
    for vacancy in found_vacancies['objects']:
        if vacancy['currency'] == 'rub':
            salary = predict_rub_salary(
                payment_from=vacancy['payment_from'],
                payment_to=vacancy['payment_to'])
            if salary:
                vacancies_processed += 1
                total_salary += salary
    if not vacancies_processed:
        average_salary = 0
    else:
        average_salary = int(total_salary / vacancies_processed)
    average_salary_results = {'vacancies found': found_vacancies['total'],
                              'vacancies_processed': vacancies_processed,
                              'average_salary': average_salary}
    return average_salary_results


def predict_rub_salary(payment_from, payment_to):
    if not (payment_from and payment_to):
        if payment_from:
            return payment_from * 1.2
        elif payment_to:
            return payment_to * 0.8
    elif payment_from and payment_to:
        return (payment_from + payment_to) / 2
    else:
        return 0


def print_result_table(vacancies_result: dict, title: str):
    salary_results_grouped = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата']]
    for language, results in vacancies_result.items():
        salary_results_grouped\
            .append([language] + [result for result in results.values()])
    salary_table = AsciiTable(salary_results_grouped, title)
    print(salary_table.table)


def main():
    load_dotenv()
    secret_key_sj = os.getenv('SECRET_KEY')
    languages = (os.getenv("LANGUAGES")).split(',')
    grouped_average_salary_hh = {}
    grouped_average_salary_sj = {}

    for language in languages:
        grouped_average_salary_hh[language] \
            = get_salary_statistics_hh(language)
        grouped_average_salary_sj[language] \
            = get_salary_statistics_sj(language=language,
                                       secret_key=secret_key_sj)
    print_result_table(vacancies_result=grouped_average_salary_hh,
                       title='Headhunter Moscow')
    print_result_table(vacancies_result=grouped_average_salary_sj,
                       title='Superjob Moscow')


if __name__ == '__main__':
    main()
