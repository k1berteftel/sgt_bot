from aiohttp import ClientSession


async def get_usdt_eur() -> float:
    url = 'https://open.er-api.com/v6/latest/USD'
    async with ClientSession() as session:
        async with session.get(url) as res:
            data = await res.json()
            print(data['rates'])
            eur = data['rates']['EUR']
    return float(eur)
