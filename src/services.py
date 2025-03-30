import json
import re

from src.utils import func_read_file_excel


def search_by_phone_number(data: list) -> list:
    pattern = r'\s\d+\s\d+\-\d+\-\d+'
    filtered_list = []
    for trans in data:
        match = re.search(pattern, trans['Описание'])
        if match is not None:
            filtered_list.append(trans)
    return filtered_list

df = func_read_file_excel('../data/operations.xlsx')
list_of_transactions = df.to_dict(orient="records")
print(list_of_transactions)
filtered_list = search_by_phone_number(list_of_transactions)
json_filtered_list = json.dumps(filtered_list, indent=4, ensure_ascii=False)
print(json_filtered_list)
list1 = search_by_phone_number([])
print(list1)