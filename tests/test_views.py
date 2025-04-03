import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.views import main_func


class TestMainFunc(unittest.TestCase):
    @patch('src.utils.func_read_file_json')
    @patch('src.utils.converse_cur_by_date')
    @patch('src.utils.get_price_stock_promotion')
    def test_main_func(self, mock_get_price, mock_converse_cur, mock_read_json):
        # Настройка заглушек
        mock_read_json.return_value = {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "GOOGL"]
        }
        mock_converse_cur.return_value = 75.45
        mock_get_price.return_value = 150.25

        # Создание тестового DataFrame
        data = {
            "Сумма операции": [-100.0, 200.0, -50.0, 300.0, -3000.0, 200.0, -10000.0],
            "Дата операции": [
                "30.12.2021 16:44:00",
                "29.12.2021 12:22:00",
                "28.12.2021 10:02:00",
                "01.11.2020 01:05:00",
                "12.10.2021 15:13:00",
                "19.08.2021 19:15:00",
                "09.12.2020 06:15:00"
            ],
            "Категория": ["Еда", "Наличные", "Транспорт", "Переводы", "Одежда",
                          "Переводы", "Супермаркеты"],
            "Сумма операции с округлением": [100.0, 200.0, 50.0, 300.0, 3000.0, 200.0, 10000.0]
        }
        df = pd.DataFrame(data)

        # Вызов тестируемой функции
        result = main_func(df, "31.12.2021")

        # Проверка результата
        self.assertIn("expenses", result)
        self.assertIn("income", result)
        self.assertIn("currency_rates", result)
        self.assertIn("stock_prices", result)
        # Добавь больше проверок в зависимости от ожидаемого результата

if __name__ == '__main__':
    unittest.main()