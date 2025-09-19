import re


def parse_entities(text):
    worker_match = re.search(r'Воркер:\s*@(\w+)', text)
    username = worker_match.group(1) if worker_match else None
    profit_match = re.search(r'Доля воркера:\s*(\d+(?:[.,]\d+)?)\s*([€$£₽]|[A-Z]{3})?', text)
    if profit_match:
        amount_str = profit_match.group(1).replace(',', '.')
        amount = int(float(amount_str))  # или float(amount_str), если нужны дробные
        currency = profit_match.group(2) or 'USD'  # если валюта не указана — USD по умолчанию
        return username, amount, currency

    return None, None, None