import json
from src.reports import spending_by_category
from src.services import search_by_phone_number
from src.utils import func_read_file_excel


def main():
    # Страница "События"
    # date = input('Введите дату в формате dd.mm.YYYY\n')
    # period = input('''Задайте период для анализа данных:
    # W - полная/неполная неделя текущего месяца
    # M - от 1 числа до заданной даты текущего месяца
    # Y - от 01 января до заданной даты текущего года
    # ALL - все данные из файла с транзакциями\n''')

    # result = main_func(date, period)
    # print(result)

    # Сервисы: поиск по телефонным номерам
    df = func_read_file_excel("../data/operations.xlsx")
    list_of_transactions = df.to_dict(orient="records")
    filtered_list = search_by_phone_number(list_of_transactions)
    json_filtered_list = json.dumps(filtered_list, indent=4, ensure_ascii=False)
    print(json_filtered_list)

    # Отчеты: траты по категориям
    category = input("Введите категорию для поиска\n")
    date = input("Введите дату в формате dd.mm.YYYY\n")
    print(spending_by_category(df, category, date))


if __name__ == "__main__":
    main()
