import asyncio
import logging
import time


logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)


def fibn(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibn(n-2) + fibn(n-1)


def run_fibonacci_sync():
    start_time = time.monotonic()
    fibn(20)
    log.info('Sync Fibonacci in %d ms', (time.monotonic() - start_time) * 1000)


async def fibn_async(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    tasks = []
    tasks.append(asyncio.create_task(fibn_async(n-2)))
    tasks.append(asyncio.create_task(fibn_async(n-1)))
    return sum(await asyncio.gather(*tasks))


async def run_fibonacci_async():
    start_time = time.monotonic()
    await fibn_async(20)
    log.info('Async Fibonacci in %d ms', (time.monotonic() - start_time) * 1000)


if __name__ == '__main__':
    run_fibonacci_sync()
    asyncio.run(run_fibonacci_async())
