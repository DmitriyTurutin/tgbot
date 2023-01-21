import aiohttp
import logging
import datetime
import os
from io import BytesIO

logging.basicConfig(level=logging.INFO)


async def update_data(url, email, password):
    headers = {'Content-Type': 'application/json'}
    data = {'url': url, 'email': email, 'password': password}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as resp:
            logging.info(f'Response status: {resp.status}')
            return resp.json()


async def fetch_sales_today():
    url = os.environ.get("URL") + "/sales/today"
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            logging.info(f'Response status fetch_sales_today: {resp.status}')
            return resp.json()


async def fetch_sales_last_month():
    url = os.environ.get("URL") + "/sales/last_month"
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            logging.info(f'Response status fetch_sales_today: {resp.status}')
            return await resp.json()


async def fetch_sales_range(from_date: str, to_date: str):
    url = 'http://localhost:8000/sales'
    headers = {'Content-Type': 'application/json'}

    # parse the string date to datetime object
    from_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    to_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')
    data = {'from_date': from_date.isoformat(), 'to_date': to_date.isoformat()}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, json=data) as resp:
                logging.info(f'Response status fetch_sales_today: {resp.status}')
                return await resp.json()
    except aiohttp.ClientError as e:
        logging.error("Error making request: %s", e)


async def get_excel():
    url = 'http://localhost:8000/download/sales.xlsx'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            file = BytesIO(resp)
            file.name = 'sales.xlsx'
            return file


async def get_plot():
    url = 'http://localhost:8000/download/sales.png'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            file = BytesIO(resp)
            return file
