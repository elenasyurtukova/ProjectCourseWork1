from collections import Counter
from datetime import datetime, timedelta
import pandas as pd

def main_func(df, date: str, period: str = 'M'):
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

    filtered_transactions = []
    df_OK = df.loc[df.Статус == 'OK']
    # for trans in df:
    df_date = df.loc[(date2 <= datetime.strptime(df_OK['Дата операции'], '%d.%m.%Y %H:%M:%S') <= date1)]
    # date = datetime.strptime(df_OK['Дата операции'], '%d.%m.%Y %H:%M:%S')
        # if trans['Статус'] == 'OK':
        #     if date2 <= date <= date1:
        #         filtered_transactions.append(trans)
    return df_date

def expenses(df: list) -> list:
    # sum = 0
    # expenses_trans = []
    # for trans in df:
    #     if float(trans['Сумма платежа']) < 0:
    #         sum += float(trans['Сумма операции с округлением'])
    #         trans['Сумма операции с округлением'] = float(trans['Сумма операции с округлением'])
    #         expenses_trans.append(trans)
    #         sum_of_expenses = round(sum) # сумма всех расходных операций

    return df1




def func_read_file_excel(path: str) -> list:
    """Функция: считывает данные из файла excel и возвращает список словарей транзакций"""
    try:
        df = pd.read_excel(path)
        # list_of_transactions = df.to_dict(orient="records")
        return df
    except FileNotFoundError:
        print("Файл не найден")
        return []

if __name__ == "__main__":
   df = func_read_file_excel('../data/operations.xlsx')

   df1 = main_func(df, '25.07.2018', 'ALL')
   print(expenses(df1))



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