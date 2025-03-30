# Страница "События"
from src.views import main_func


def main():
    date = input('Введите дату в формате dd.mm.YYYY\n')
    period = input('''Задайте период для анализа данных:
    W - полная/неполная неделя текущего месяца
    M - от 1 числа до заданной даты текущего месяца
    Y - от 01 января до заданной даты текущего года
    ALL - все данные из файла с транзакциями\n''')

    result = main_func(date, period)
    print(result)

