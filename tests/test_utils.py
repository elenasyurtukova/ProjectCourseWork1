import json
import unittest
from unittest.mock import patch, Mock

import pandas as pd
import pytest

from src.utils import func_read_file_json, filter_by_period, converse_cur_by_date
from src.views import func_read_file_excel


class TestReadExcelFile(unittest.TestCase):
    def test_valid_data(self):
        mock_data = pd.DataFrame(
            {'Дата операции': ['31.12.2021 16:44:00'],
             'Номер карты': [None], 'Статус': ['OK'],
             'Сумма операции': [-3000.0], 'Валюта операции': ['RUB'],
             'Кэшбэк': [None], 'Категория': ['Переводы'],
             'Описание': ['Линзомат ТЦ Юность'],
             }
        )
        with patch("pandas.read_excel", return_value=mock_data):
            result = func_read_file_excel("operations.xlsx")
            self.assertEqual(len(result), 1)
            self.assertEqual(result["Дата операции"][0], "31.12.2021 16:44:00")

    def test_file_not_found(self):
        with patch("pandas.read_excel", side_effect=FileNotFoundError):
            result = func_read_file_excel("operations.xlsx")
            self.assertEqual(result, [])

class TestJsonReader(unittest.TestCase):
    @patch("builtins.open")
    @patch("json.load")
    def test_func_read_file_json(self: "TestJsonReader", mock_json_load, mock_open):
        # Задаю тестовые данные
        mock_json_load.return_value = [
            {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
            }
        ]
        # Вызываю функцию и проверяю результат
        result = func_read_file_json("path/to/file.json")
        self.assertEqual(result, [
                    {
                    "user_currencies": ["USD", "EUR"],
                    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
                    }
            ],
        )
        mock_json_load.return_value = []
        # Вызываю функцию и проверяю результат
        result = func_read_file_json("path/to/file.json")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_open):
        # Вызываю свою функцию и проверяю, что она возвращает пустой список
        result = func_read_file_json("path/to/nonexistent/file.json")
        self.assertEqual(result, {})

@pytest.fixture()
def df():
    return pd.DataFrame({'Валюта операции': ['RUB', 'RUB', 'RUB'],
                         'Дата операции': ['30.12.2021 16:44:00', '29.12.2021 12:22:00', '28.12.2021 10:02:00'],
                          'Статус': ['OK', 'OK', 'OK'], 'Сумма операции': [-3000.0, -200.0, -10000.0],
                          })

@pytest.mark.parametrize(
    "date1, date2, expected_df",
    [
        ("31.12.2021 16:44:00", "25.12.2021 16:44:00", pd.DataFrame({
            'Валюта операции': ['RUB', 'RUB', 'RUB'],
            'Дата операции': pd.to_datetime(['30.12.2021 16:44:00', '29.12.2021 12:22:00', '28.12.2021 10:02:00'],
                                            format='%d.%m.%Y %H:%M:%S'),
            'Статус': ['OK', 'OK', 'OK'],
            'Сумма операции': [-3000.0, -200.0, -10000.0],
        })),
        ("31.12.2021 16:44:00", "30.12.2021 00:44:00", pd.DataFrame({
            'Валюта операции': ['RUB'],
            'Дата операции': pd.to_datetime(['30.12.2021 16:44:00'], format='%d.%m.%Y %H:%M:%S'),
            'Статус': ['OK'],
            'Сумма операции': [-3000.0],
        })),
    ]
)
def test_filter_by_period(df, date1, date2, expected_df):
    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)
    result_df = filter_by_period(date1, date2, df)
    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def test_converse_cur_by_date():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_cur_code = "USD"
    mock_date = '2020-04-30'
    mock_response.json.return_value = {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
                                       'info': {'timestamp': 1588291199, 'rate': 74.373499},
                                       'date': '2020-04-30', 'historical': True, 'result': 74.373499}
    with patch("requests.get", return_value=mock_response):
        result = converse_cur_by_date(mock_cur_code, mock_date)
        assert result == 74.37

def test_converse_cur_by_date_no_code_currency():
    mock_response = Mock()
    mock_response.status_code = 400
    mock_cur_code = ""
    mock_date = '2020-04-30'
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to get currency rate"):
            converse_cur_by_date(mock_cur_code, mock_date)

if __name__ == "__main__":
    unittest.main()