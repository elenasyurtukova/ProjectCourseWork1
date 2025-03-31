from datetime import datetime
from typing import Optional
import pandas as pd
from src.utils import filter_by_period
from typing import Any, Callable
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename="../logs/reports.log",
    encoding="UTF-8",
    filemode="w",
)
logger = logging.getLogger("reports")


def write_file(filename: str | None = None) -> Callable:
    """Декоратор, записывает результат работы функции в файл"""
    def wrapped(function: Callable) -> Callable:
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            result_json = result.to_json(orient="records", force_ascii=False)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result_json)
            logger.info("Отчет записан в json-файл")
            return result
        return inner
    return wrapped


# @write_file(filename="result.json")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Функция принимает датафрейм, фильтрует его по категории за 3 месяца до указанной даты"""
    if date is not None:
        date1 = datetime.strptime(date, "%d.%m.%Y")
    else:
        date1 = datetime.now()
    if date1.month > 3:
        try:
            month_2 = date1.month - 3
            date2 = datetime(year=date1.year, month=month_2, day=date1.day)
        except ValueError as e:
            logger.error("Ошибка существования даты")
            print(f"Error: {type(e).__name__}, полученная дата не существует")
    else:
        try:
            year_2 = date1.year - 1
            month_2 = date1.month + 12 - 3
            date2 = datetime(year=year_2, month=month_2, day=date1.day)
        except ValueError as e:
            logger.error("Ошибка существования даты")
            print(f"Error: {type(e).__name__}, полученная дата не существует")
    filtered_df = filter_by_period(date1, date2, transactions)
    category_df = filtered_df[filtered_df["Категория"] == category]
    logger.info("Датафрейм отфильтрован по датам и категории")
    return category_df
