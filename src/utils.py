import os
from datetime import datetime
import pandas as pd
import json

import requests
from dotenv import load_dotenv


def func_read_file_excel(path: str) -> list:
    """Функция: считывает данные из файла excel и возвращает список словарей транзакций"""
    try:
        df = pd.read_excel(path)
        # list_of_transactions = df.to_dict(orient="records")
        return df
    except FileNotFoundError:
        print("Файл не найден")
        return []


def filter_by_period(date1: datetime, date2: datetime, df):
    """Функция фильтрует датафрейм: попадают данные между заданными датами"""
    df = df.copy()  # Создаем копию DataFrame, чтобы избежать предупреждений
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered_df = df.loc[(df['Дата операции'] <= date1)&(df['Дата операции'] >= date2)]
    return filtered_df

def func_read_file_json(path: str) -> dict:
    """функция: читает данные из json-файла пользовательских настроек"""
    try:
        with open(path, encoding="utf-8") as file:
            try:
                user_settings = json.load(file)
                return user_settings
            except json.JSONDecodeError:
                print("Ошибка декодирования файла")
                return {}
    except FileNotFoundError:
        print("Файл не найден")
        return {}

def converse_cur_by_date(cur_code: str, date: datetime):
    """функция конвертирует валюту в рубли на заданную дату"""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur_code}&amount=1&date={date}"
    load_dotenv(dotenv_path="../.env")
    API_KEY = os.getenv("API_KEY")
    payload = {}
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise ValueError("Failed to get currency rate")
    result = round((response.json()["result"]), 2)
    return result

def get_price_stock_promotion(code_promotion, date: datetime):
    load_dotenv(dotenv_path="../.env")
    api_key = os.getenv("API_key")
    symbol = code_promotion  # Символ акции, например, Apple "AAPL"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    # Получаем данные для указанной даты
    if date in data["Time Series (Daily)"]:
        daily_data = data["Time Series (Daily)"][date]
        price_promotion = round(float(daily_data['4. close']),2)
        return price_promotion
    else:
        print(f"Данные на {date} не найдены.")

print(get_price_stock_promotion('AAPL', '2020-09-10'))