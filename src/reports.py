from datetime import datetime
from typing import Optional
import pandas as pd
from src.utils import filter_by_period, func_read_file_excel


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date is not None:
        date1 = datetime.strptime(date, "%d.%m.%Y")
    else:
        date1 = datetime.now()
    if date1.month > 3:
        month_2 = date1.month - 3
        date2 = datetime(year=date1.year, month=month_2, day=date1.day)
    else:
        year_2 = date1.year - 1
        month_2 = date1.month + 12 - 3
        date2 = datetime(year=year_2, month=month_2, day=date1.day)
    filtered_df = filter_by_period(date1, date2, transactions)
    category_df = filtered_df[filtered_df['Категория'] == category]
    sum_category = round(category_df['Сумма платежа'].sum())
    return sum_category
df = func_read_file_excel('../data/operations.xlsx')
sum_category = spending_by_category(df, 'Супермаркеты', '01.06.2019')
print(sum_category)
