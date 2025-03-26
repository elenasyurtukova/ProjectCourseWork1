import unittest
from unittest.mock import patch

import pandas as pd

from src.views import func_read_file_excel


class TestReadExcelFile(unittest.TestCase):
    def test_valid_data(self):
        mock_data = pd.DataFrame(
            {'Дата операции': ['01.01.2018 12:49:53'],
             'Номер карты': [None], 'Статус': ['OK'],
             'Сумма операции': [-3000.0], 'Валюта операции': ['RUB'],
             'Кэшбэк': [None], 'Категория': ['Переводы'],
             'Описание': ['Линзомат ТЦ Юность'],
             'Бонусы (включая кэшбэк)': [0],
             'Округление на инвесткопилку': [0],
             'Сумма операции с округлением': [3000.0]}
        )
        with patch("pandas.read_excel", return_value=mock_data):
            result = func_read_file_excel("operations.xlsx")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["Статус"], "OK")

    def test_file_not_found(self):
        with patch("pandas.read_excel", side_effect=FileNotFoundError):
            result = func_read_file_excel("operations.xlsx")
            self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()