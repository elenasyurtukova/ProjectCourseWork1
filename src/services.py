import re


def search_by_phone_number(data: list) -> list:
    """Функция сортировки операций с мобильными номерами в описании"""
    pattern = r"\s\d+\s\d+\-\d+\-\d+"
    filtered_list = []
    for trans in data:
        match = re.search(pattern, trans["Описание"])
        if match is not None:
            filtered_list.append(trans)
    return filtered_list
