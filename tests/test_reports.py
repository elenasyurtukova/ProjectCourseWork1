import pandas as pd
import pytest

from src.reports import spending_by_category


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
