import asyncio
import datetime as dt
import logging
import os
import time

import httpx


logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)


API_HISTORICAL = 'https://openexchangerates.org/api/historical/{}.json'
APP_ID = os.environ.get('APP_ID', '')
PERIOD_DAYS = int(os.environ.get('PERIOD', 2))


async def get_rates_for(client, date):
    log.info('Starting API request for %s', date)
    content = None

    response = await client.get(
        API_HISTORICAL.format(date.strftime('%Y-%m-%d')),
        params=dict(app_id=APP_ID)
    )

    if response.status_code == 200:
        log.info('Response received from %s', response.url)
        content = response.text
    else:
        log.error('Bad %s, status %d', response.url, response.status_code)

    return content


async def get_rates():
    rates = []
    tasks = []
    start_time = time.monotonic()
    today = dt.datetime.today()
    async with httpx.AsyncClient() as client:
        for days in range(PERIOD_DAYS):
            date = today - dt.timedelta(days=days)
            tasks.append(asyncio.create_task(get_rates_for(client, date)))
        rates = await asyncio.gather(*tasks)

    log.info('Downloaded in %d ms', (time.monotonic() - start_time) * 1000)
    return rates


if __name__ == '__main__':
    asyncio.run(get_rates())
