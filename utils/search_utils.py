import re


def parse_entities(text):
    worker_match = re.search(r'Воркер:\s*@(\w+)', text)
    username = worker_match.group(1) if worker_match else None
    match = re.match(r'^(\d+(?:[.,]\d+)?)\s*([^\d\s]+)?$', text.strip())
    if match:
        amount = int(match.group(1).replace(',', '.'))
        currency_symbol = match.group(2) or 'USD'  # если нет символа — считаем USD
        return username, amount, currency_symbol
    return None, None, None