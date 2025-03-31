import tempfile
import os
import pandas as pd
import pytest

from src.reports import spending_by_category, write_file


@pytest.fixture()
def df():
    return pd.DataFrame(
        {
            "Валюта операции": ["RUB", "RUB", "RUB"],
            "Дата операции": pd.to_datetime(
                ["03.12.2021 16:44:00", "15.02.2021 12:22:00", "25.11.2021 10:02:00"],
                format="%d.%m.%Y %H:%M:%S",
            ),
            "Категория": ["Мобильная связь", "Супермаркеты", "Супермаркеты"],
            "Статус": ["OK", "OK", "OK"],
            "Сумма операции": [-3000.0, -200.0, -10000.0],
        }
    )


@pytest.mark.parametrize(
    "date, category, expected_df",
    [
        (
            "10.12.2021",
            "Супермаркеты",
            pd.DataFrame(
                {
                    "Валюта операции": ["RUB"],
                    "Дата операции": pd.to_datetime(
                        ["25.11.2021 10:02:00"], format="%d.%m.%Y %H:%M:%S"
                    ),
                    "Категория": ["Супермаркеты"],
                    "Статус": ["OK"],
                    "Сумма операции": [-10000.0],
                }
            ),
        ),
        (
            "15.12.2021",
            "Мобильная связь",
            pd.DataFrame(
                {
                    "Валюта операции": ["RUB"],
                    "Дата операции": pd.to_datetime(
                        ["03.12.2021 16:44:00"], format="%d.%m.%Y %H:%M:%S"
                    ),
                    "Категория": ["Мобильная связь"],
                    "Статус": ["OK"],
                    "Сумма операции": [-3000.0],
                }
            ),
        ),
    ],
)
def test_spending_by_category(df, date, category, expected_df):
    result_df = spending_by_category(df, category, date)
    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True), expected_df.reset_index(drop=True)
    )

def test_spending_by_category_unknown_date(df):
    assert spending_by_category(df, 'Супермаркеты', '29.05.2019') == None

def test_write_file():
    # Тестирование с временным файлом
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    try:
        # Применяем декоратор с временным файлом
        @write_file(filename=filename)
        def my_function():
            return (pd.DataFrame(
                {
                    "Валюта операции": ["RUB"],
                    "Дата операции": ["03.12.2021 16:44:00"],
                    "Категория": ["Мобильная связь"],
                    "Статус": ["OK"],
                    "Сумма операции": [-3000.0],
                }
            ))

        # Вызываем функцию
        my_function()

        # Проверяем содержимое временного файла
        with open(filename, "r", encoding="utf-8") as file:
            result = file.read()
            assert result == ('[{"Валюта операции":"RUB","Дата операции":"03.12.2021 16:44:00","Категория":"Мобильная связь","Статус":"OK","Сумма операции":-3000.0}]')

    finally:
        # Удаляем временный файл
        os.remove(filename)
