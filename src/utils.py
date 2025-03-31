import os
from datetime import datetime, timedelta
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename="../logs/utils.log",
    encoding="UTF-8",
    filemode="w",
)
logger = logging.getLogger("utils")

def time_period(date: str, period: str = "M"):
    """Функция, определяет дату окончания по заданному атрибуту"""
    try:
        date1 = datetime.strptime(date, "%d.%m.%Y")
        if period == "W":
            if date1.day > 7:
                date2 = date1 - timedelta(days=7)
            else:
                date2 = datetime(date1.year, date1.month, 1)
        elif period == "M":
            date2 = datetime(date1.year, date1.month, 1)
        elif period == "Y":
            date2 = datetime(date1.year, 1, 1)
        elif period == "ALL":
            date2 = datetime(2017, 1, 1)
        else:
            print(
                "Задан неверный период, для работы программы используем период с начала месяца"
            )
            date2 = datetime(date1.year, date1.month, 1)
        return date1, date2
    except Exception as e:
        logger.error("Задан неверный формат даты")
        print(f"Error: {type(e).__name__}, задан неверный формат даты")
    logger.info("Рассчитан период времени для анализа")


def func_read_file_excel(path: str) -> list:
    """Функция: считывает данные из файла excel и возвращает список словарей транзакций"""
    try:
        df = pd.read_excel(path)
        logger.info("При чтении файла excel получен датафрейм")
        return df
    except FileNotFoundError:
        logger.error("Файл не найден")
        print("Файл не найден")
        return []


def filter_by_period(date1: datetime, date2: datetime, df):
    """Функция фильтрует датафрейм: попадают данные между заданными датами"""
    df = df.copy()
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )
    filtered_df = df.loc[
        (df["Дата операции"] <= date1) & (df["Дата операции"] >= date2)
    ]
    logger.info("Данные отфильтрованы по заданному периоду")
    return filtered_df


def func_read_file_json(path: str) -> dict:
    """функция: читает данные из json-файла пользовательских настроек"""
    try:
        with open(path, encoding="utf-8") as file:
            try:
                user_settings = json.load(file)
                logger.info("Данные пользовательских настроек получены")
                return user_settings
            except json.JSONDecodeError:
                print("Ошибка декодирования файла")
                logger.error("Ошибка декодирования файла")
                return {}
    except FileNotFoundError:
        print("Файл не найден")
        logger.error("Файл не найден")
        return {}


def converse_cur_by_date(cur_code: str, date: datetime):
    """функция конвертирует валюту в рубли на заданную дату"""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur_code}&amount=1&date={date}"
    load_dotenv(dotenv_path="../.env")
    API_KEY = os.getenv("API_KEY")
    payload = {}
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers, data=payload)
    print(response.json())
    if response.status_code != 200:
        raise ValueError("Failed to get currency rate")
        logger.error("Не удалось получить курс валюты")
    result = round((response.json()["result"]), 2)
    logger.info("Курс валюты успешно получен")
    return result


def get_price_stock_promotion(code_promotion, date: datetime):
    """Функция: получает цену указанной акции на заданную дату"""
    load_dotenv(dotenv_path="../.env")
    api_key = os.getenv("API_key")
    symbol = code_promotion  # Символ акции, например, Apple "AAPL"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    # Получаем данные для указанной даты
    if date in data["Time Series (Daily)"]:
        daily_data = data["Time Series (Daily)"][date]
        price_promotion = round(float(daily_data["4. close"]), 2)
        logger.info("Курс акции успешно получен")
        return price_promotion
    else:
        logger.info("Курс акции на заданную дату не найден")
        print(f"Данные на {date} не найдены.")
# print(get_price_stock_promotion('AAPL', '2020-09-10'))
