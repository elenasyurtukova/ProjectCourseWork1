from datetime import datetime
import pandas as pd
import json

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
