# Расчет средних зарплат популярных языков программирования

Код позволяет сделать расчет средних зарплата по данным сайтов https://hh.ru/ и https://www.superjob.ru/:


## Как установить

Python3 должен быть уже установлен. Затем используйте ``pip`` (или ``pip3``, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
Создайте файл ``.env`` в корневой папке и поместите в него переменную с указанием ключевых слов(языков) для анализа вакансий (через запятую без пробелов)
```
LANGUAGES="Ruby,C++"
```

### Получите secret_key для работы API Superjob:

Зарегистрируйте приложение на сервисе https://api.superjob.ru/register
При регистрации приложения от вас потребуют указать сайт. Введите любой, они не проверяют.
Поместите secret_key в файл ``.env``

```
SECRET_KEY="v3.r.136514968.0647435edaa59e7cc5f73f822183f4766fadee3e.e193b3a15e7f3c3f35828079e770f6e2694d2f3e"```
```

### Запуск скрипта

Запуск скрипта производится командой

```
python3 main.py
```

## Пример использования

```
$ python3 main.py
+Headhunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Ruby                  | 79               | 56                  | 173300           |
| PHP                   | 813              | 753                 | 150263           |
| C++                   | 543              | 498                 | 152592           |
| CSS                   | 957              | 866                 | 135436           |
| Python                | 1093             | 956                 | 168003           |
| Java                  | 715              | 631                 | 203092           |
| Javascript            | 1526             | 1312                | 160974           |
| Go                    | 352              | 299                 | 186560           |
| ReactJS               | 640              | 524                 | 191470           |
+-----------------------+------------------+---------------------+------------------+
+Superjob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Ruby                  | 4                | 4                   | 77416            |
| PHP                   | 87               | 20                  | 110866           |
| C++                   | 42               | 20                  | 111558           |
| CSS                   | 74               | 20                  | 74708            |
| Python                | 114              | 20                  | 88250            |
| Java                  | 64               | 20                  | 100125           |
| Javascript            | 120              | 20                  | 81658            |
| Go                    | 14               | 14                  | 79702            |
| ReactJS               | 2                | 2                   | 62916            |
+-----------------------+------------------+---------------------+------------------+
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.

## Лицензия

Код распространяется свободно согласно MIT License
