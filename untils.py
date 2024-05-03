import json
from typing import Any

import requests


def read_json_file(file_name: str) -> dict[Any, Any]:
    """
    Читает json файл и возвращает данные в виде словаря
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


file = "data/operations.json"
print(read_json_file(file))


def sum_of_transactions(transactions: dict[Any, Any], currency: dict[Any, Any]):
    """
    Возвращает сумму всех транзакций
    сли транзакция была в USD или EUR, идет обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли
    """
    sum = 0
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            sum += int(transaction["operationAmount"]["amount"])
        elif transaction["operationAmount"]["currency"]["code"] == "RUB":
            sum += int(transaction["operationAmount"]["amount"]) / int(currency)
    return sum


transactions = {
    "id": 207126257,
    "state": "EXECUTED",
    "date": "2019-07-15T11:47:40.496961",
    "operationAmount": {"amount": "92688.46", "currency": {"name": "USD", "code": "USD"}},
    "description": "Открытие вклада",
    "to": "Счет 35737585785074382265",
}, {
    "id": 667307132,
    "state": "EXECUTED",
    "date": "2019-07-13T18:51:29.313309",
    "operationAmount": {"amount": "97853.86", "currency": {"name": "руб.", "code": "RUB"}},
    "description": "Перевод с карты на счет",
    "from": "Maestro 1308795367077170",
    "to": "Счет 96527012349577388612",
}
currency = requests.get("https://www.finmarket.ru/currency/rates/")
print(sum_of_transactions(transactions, currency))
