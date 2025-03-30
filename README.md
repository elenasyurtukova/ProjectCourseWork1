# Проект создания виджета банковских операций клиента:
Приложение для анализа банковских операций

## В проекте реализованы функции:
* в модуле utils реализована функция чтения из excel-файла и json-файла, 
  функция фильтрации данных по заданному промежутку между двумя датами, 
  функция конвертации заданной валюты на указанную дату,
  функция получения цены заданной акции на указанную дату
  Для работы функций нужно иметь ключи APY_KEY с сайта https://apilayer.com 
  и https://www.alphavantage.co
* в модуле views реализована функция анализа данных за период, конвертации валюты
  и получения цен акций на заданную дату с использованием функций из модуля utils
* в модуле services реализована функция сортировки операций с мобильными номерами в описании
* в модуле reports реализована функция, которая принимает датафрейм, 
  фильтрует его по категории за 3 месяца до указанной даты, и декоратор, 
  который записывает результат работы функции в файл
* в модуле main реализована логика проекта: по условиям, 
  которые задает пользователь

## Установка:
1. Клонируйте репозиторий:
```git clone git@github.com:elenasyurtukova/ProjectCourseWork1.git```

2. Установите библиотеки из pyproject.toml:
```poetry install```

## Тесты:
Каждый модуль проекта протестирован с помощью фреймворка pytest.
Чтобы запустить его (все тесты), выполните команду: ```pytest```.
Покрытие кода тестами составляет 94%    