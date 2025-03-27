from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
from unicodedata import category

from src.utils import func_read_file_excel, filter_by_period


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

    filtered_df = filter_by_period(date1, date2, df_OK) # вызываем функцию для фильтрации датафрейма по датам
    print(filtered_df)
    expenses_df = filtered_df[filtered_df['Сумма операции'] < 0] # фильтруем только расходные операции
    total_amount_expenses = round(expenses_df['Сумма операции с округлением'].sum()) # определяем сумму расходных операций
    category_grouped_expenses_df = expenses_df.groupby('Категория')['Сумма операции с округлением'].sum()
    category_expenses_df = category_grouped_expenses_df.sort_values(ascending=False)
    category_expenses_dict = category_expenses_df.to_dict()
    print(category_expenses_dict)






def expenses(df: list) -> list:
    # sum = 0
    # expenses_trans = []
    # for trans in df:
    #     if float(trans['Сумма платежа']) < 0:
    #         sum += float(trans['Сумма операции с округлением'])
    #         trans['Сумма операции с округлением'] = float(trans['Сумма операции с округлением'])
    #         expenses_trans.append(trans)
    #         sum_of_expenses = round(sum) # сумма всех расходных операций

    pass






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