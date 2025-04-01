import json
from src.reports import spending_by_category
from src.services import search_by_phone_number
from src.utils import func_read_file_excel
from src.views import main_func

from src.logger import get_logger

logger = get_logger("log.log")

def main():
    # Страница "События"
    date = input('Введите дату в формате dd.mm.YYYY\n')
    period = input('''Задайте период для анализа данных:
    W - полная/неполная неделя текущего месяца
    M - от 1 числа до заданной даты текущего месяца
    Y - от 01 января до заданной даты текущего года
    ALL - все данные из файла с транзакциями\n''')
    df = func_read_file_excel(
        "../data/operations.xlsx")
    df_OK = df.loc[df["Статус"] == "OK"]
    result = main_func(df_OK, date, period)
    logger.info("Получены данные для страницы «События»")
    print(result)

    # Сервисы: поиск по телефонным номерам
    df = func_read_file_excel("../data/operations.xlsx")
    list_of_transactions = df.to_dict(orient="records")
    filtered_list = search_by_phone_number(list_of_transactions)
    json_filtered_list = json.dumps(filtered_list, indent=4, ensure_ascii=False)
    logger.info("Отработал сервис: поиск по телефонным номерам")
    print(json_filtered_list)

    # Отчеты: траты по категориям
    category = input("Введите категорию для поиска\n")
    date = input("Введите дату в формате dd.mm.YYYY\n")
    result_list = spending_by_category(df, category, date).to_dict(orient="records")
    logger.info("Получен отчет: траты по категориям")
    print(result_list)


if __name__ == "__main__":
    main()
