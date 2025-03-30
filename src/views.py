from datetime import datetime, timedelta
import json
from src.utils import (
    func_read_file_excel,
    filter_by_period,
    func_read_file_json,
    converse_cur_by_date,
    get_price_stock_promotion,
)
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename="../logs/views.log",
    encoding="UTF-8",
    filemode="w",
)
logger = logging.getLogger("views")


def main_func(date: str, period: str = "M"):
    """Функция анализа данных за период, конвертации валюты и получения цен акций"""
    # получаем 2 даты, между которыми будем анализировать данные
    try:
        date1 = datetime.strptime(date, "%d.%m.%Y")
    except Exception as e:
        logger.error("Задан неверный формат даты")
        print(f"Error: {type(e).__name__}, задан неверный формат даты")
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
    logger.info("Рассчитан период времени для анализа")
    df = func_read_file_excel(
        "../data/operations.xlsx"
    )  # вызываем функцию для получения данных из файла excel
    df_OK = df.loc[df["Статус"] == "OK"]  # фильтруем только успешные операции
    filtered_df = filter_by_period(
        date1, date2, df_OK
    )  # вызываем функцию для фильтрации датафрейма по датам
    logger.info("Отфильтрованы данные со статусом 'ОК' в заданном временном интервале")
    # расходная часть
    expenses_df = filtered_df[
        filtered_df["Сумма операции"] < 0
    ]  # фильтруем только расходные операции
    total_amount_expenses = round(
        expenses_df["Сумма операции с округлением"].sum()
    )  # определяем сумму расходных операций
    category_grouped_expenses_df = expenses_df.groupby("Категория")[
        "Сумма операции с округлением"
    ].sum()
    category_expenses_df = category_grouped_expenses_df.sort_values(ascending=False)
    category_expenses_dict = category_expenses_df.to_dict()
    if len(category_expenses_dict) <= 7:
        category_expenses_list = []
        for key, value in category_expenses_dict.items():
            elem = {}
            elem["category"] = key
            elem["amount"] = round(value)
            category_expenses_list.append(elem)
    elif len(category_expenses_dict) > 7:
        category_expenses_list = [
            {"category": key, "amount": round(value)}
            for key, value in category_expenses_dict.items()
        ]
        elem_7 = category_expenses_list[:7]
        elem_last = category_expenses_list[7:]
        sum_last = sum(elem["amount"] for elem in elem_last)
        last_value = {"category": "Остальное", "amount": round(sum_last)}
        category_expenses_list = elem_7 + [last_value]

    # определяем сумму операций c наличными и переводами
    amount_cash = round(
        filtered_df[filtered_df["Категория"] == "Наличные"]["Сумма операции"].sum()
    )
    amount_transfers = round(
        filtered_df[filtered_df["Категория"] == "Переводы"]["Сумма операции"].sum()
    )
    list_cash_transfers = [
        {"category": "Наличные", "amount": amount_cash},
        {"category": "Переводы", "amount": amount_transfers},
    ]
    # доходная часть
    incoming_df = filtered_df[
        filtered_df["Сумма операции"] > 0
    ]  # фильтруем только доходные операции
    total_amount_incoming = round(
        incoming_df["Сумма операции с округлением"].sum()
    )  # определяем сумму доходных операций
    category_grouped_incoming_df = incoming_df.groupby("Категория")[
        "Сумма операции с округлением"
    ].sum()
    category_incoming_df = category_grouped_incoming_df.sort_values(ascending=False)
    category_incoming_dict = category_incoming_df.to_dict()
    category_incoming_list = [
        {"category": key, "amount": round(value)}
        for key, value in category_incoming_dict.items()
    ]

    user_settings = func_read_file_json("../user_settings.json")
    # {'user_currencies': ['USD', 'EUR'], 'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']}

    currency_rates = []
    for i in range(len(user_settings["user_currencies"])):
        cur_code = user_settings["user_currencies"][i]
        date = date1.strftime("%Y-%m-%d")
        cur_value = converse_cur_by_date(cur_code, date)
        elem = {"currency": cur_code, "rate": cur_value}
        currency_rates.append(elem)

    stock_prices = []
    for i in range(len(user_settings["user_stocks"])):
        code_promotion = user_settings["user_stocks"][i]
        date = date1.strftime("%Y-%m-%d")
        price_value = get_price_stock_promotion(code_promotion, date)
        elem = {"stock": code_promotion, "price": price_value}
        stock_prices.append(elem)
    result = {}
    expenses_dict = {}
    expenses_dict["total_amount"] = total_amount_expenses
    expenses_dict["main"] = category_expenses_list
    expenses_dict["transfers_and_cash"] = list_cash_transfers
    income_dict = {}
    income_dict["total_amount"] = total_amount_incoming
    income_dict["main"] = category_incoming_list
    result["expenses"] = expenses_dict
    result["income"] = income_dict
    result["currency_rates"] = currency_rates
    result["stock_prices"] = stock_prices
    json_result = json.dumps(result, indent=4, ensure_ascii=False)
    logger.info("Данные проанализированы и получен результат в формате json")
    return json_result
