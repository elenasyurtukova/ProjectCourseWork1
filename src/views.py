from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
from unicodedata import category

from src.utils import func_read_file_excel, filter_by_period, func_read_file_json


def main_func(date: str, period: str = 'M'):
    # получаем 2 даты, между которыми будем анализировать данные
    date1 = datetime.strptime(date, "%d.%m.%Y")
    if period == 'W':
        if date1.day > 7:
            date2 = date1 - timedelta(days=7)
        else:
            date2 = datetime(date1.year, date1.month, 1)
    elif period == 'M':
        date2 = datetime(date1.year, date1.month, 1)
    elif period == 'Y':
        date2 = datetime(date1.year, 1, 1)
    elif period == 'ALL':
        date2 = datetime(2017, 1, 1)

    df = func_read_file_excel('../data/operations.xlsx')  # вызываем функцию для получения данных из файла excel
    print(date1, date2)
    df_OK = df.loc[df['Статус'] == 'OK'] # фильтруем только успешные операции
    print(df_OK)
    filtered_df = filter_by_period(date1, date2, df_OK) # вызываем функцию для фильтрации датафрейма по датам
    print(filtered_df)

   # расходная часть
    expenses_df = filtered_df[filtered_df['Сумма операции'] < 0] # фильтруем только расходные операции
    total_amount_expenses = round(expenses_df['Сумма операции с округлением'].sum()) # определяем сумму расходных операций
    category_grouped_expenses_df = expenses_df.groupby('Категория')['Сумма операции с округлением'].sum()
    category_expenses_df = category_grouped_expenses_df.sort_values(ascending=False)
    category_expenses_dict = category_expenses_df.to_dict()
    print(category_expenses_dict)
    print(type(category_expenses_dict))
    print(len(category_expenses_dict))
    if len(category_expenses_dict) <= 7:
        category_expenses_list = []
        for key, value in category_expenses_dict.items():
            elem = {}
            elem['category'] = key
            elem['amount'] = round(value)
            category_expenses_list.append(elem)
        print(category_expenses_list)
    elif len(category_expenses_dict) > 7:
        category_expenses_list = [{'category': key, 'amount': round(value)} for key, value in category_expenses_dict.items()]
        elem_7 = category_expenses_list[:7]
        elem_last = category_expenses_list[7:]
        sum_last = sum(elem['amount'] for elem in elem_last)
        last_value = {'category': 'Остальное', 'amount': round(sum_last)}
        category_expenses_list = elem_7 + [last_value]
        print(category_expenses_list)

    # определяем сумму операций c наличными и переводами
    amount_cash = round(filtered_df[filtered_df['Категория'] == 'Наличные']['Сумма операции'].sum())
    amount_transfers = round(filtered_df[filtered_df['Категория'] == 'Переводы']['Сумма операции'].sum())
    list_cash_transfers = [{'category': 'Наличные', 'amount': amount_cash},
                           {'category': 'Переводы', 'amount': amount_transfers}]
    # доходная часть
    incoming_df = filtered_df[filtered_df['Сумма операции'] > 0]  # фильтруем только доходные операции
    total_amount_incoming = round(incoming_df['Сумма операции с округлением'].sum())  # определяем сумму доходных операций
    category_grouped_incoming_df = incoming_df.groupby('Категория')['Сумма операции с округлением'].sum()
    category_incoming_df = category_grouped_incoming_df.sort_values(ascending=False)
    category_incoming_dict = category_incoming_df.to_dict()
    category_incoming_list = [{'category': key, 'amount': round(value)} for key, value in
                              category_incoming_dict.items()]
    print(category_incoming_list)

    user_settings = func_read_file_json('../user_settings.json')








if __name__ == "__main__":
   main_func('17.09.2020', 'W')



# {
#   "expenses": {
#     "total_amount": 32101,
#     "main": [
#       {
#         "category": "Супермаркеты",
#         "amount": 17319
#       },
#       {
#         "category": "Фастфуд",
#         "amount": 3324
#   },
#       {
#         "category": "Топливо",
#         "amount": 2289
#       },
#       {
#         "category": "Развлечения",
#         "amount": 1850
#       },
#       {
#         "category": "Медицина",
#         "amount": 1350
#       },
#       {
#         "category": "Остальное",
#         "amount": 2954
#       }
#     ],
#     "transfers_and_cash": [
#       {
#         "category": "Наличные",
#         "amount": 500
#       },
#       {
#         "category": "Переводы",
#         "amount": 200
#       }
#     ]
#   },
#   "income": {
#     "total_amount": 54271,
#     "main": [
#       {
#         "category": "Пополнение_BANK007",
#         "amount": 33000
#       },
#       {
#         "category": "Проценты_на_остаток",
#         "amount": 1242
#       },
#       {
#         "category": "Кэшбэк",
#         "amount": 29
#       }
#     ]
#   },
#   "currency_rates": [
#     {
#       "currency": "USD",
#       "rate": 73.21
#     },
#     {
#       "currency": "EUR",
#       "rate": 87.08
#     }
#   ],
#   "stock_prices": [
#     {
#       "stock": "AAPL",
#       "price": 150.12
#     },
#     {
#       "stock": "AMZN",
#       "price": 3173.18
#     },
#     {
#       "stock": "GOOGL",
#       "price": 2742.39
#     },
#     {
#       "stock": "MSFT",
#       "price": 296.71
#     },
#     {
#       "stock": "TSLA",
#       "price": 1007.08
#     }
#   ]
# }