import asyncio
import time

import pytest
import requests

from scraper.async_scheduler import AsyncRequestScheduler


async def sleep(completed, n, scheduler, **kwargs):
    if completed >= n:
        return None
    await scheduler.add_task(sleep, completed=completed + 1, n=n)
    await asyncio.sleep(0.0001)


async def dummy_request_with_scheduler(req_number, n, scheduler, session):
    if req_number >= n:
        return None
    await scheduler.add_task(dummy_request_with_scheduler, req_number=req_number + 1, n=n)
    await session.get("https://www.google.com")


@pytest.mark.asyncio
async def test_async_scraper_with_dummy_async_activity():
    async with AsyncRequestScheduler(wait=5) as a:
        a.set_initial_callback(sleep, completed=1, n=5)
        await a.go()
    assert a.completed == 5


def time_it(fn):
    async def inner(**kwargs):
        t = time.time()
        if asyncio.iscoroutinefunction(fn):
            await fn(**kwargs)
        else:
            fn(**kwargs)

        return time.time() - t

    return inner


@time_it
async def async_request(n):
    async with AsyncRequestScheduler(wait=1) as a:
        a.set_initial_callback(dummy_request_with_scheduler, req_number=0, n=n)
        await a.go()


@time_it
def sync_request(n):
    for i in range(n):
        requests.get("https://www.google.com")


@pytest.mark.asyncio
@pytest.mark.parametrize("n", range(20, 100, 25))
@pytest.mark.slow
async def test_async_scraper_faster_than_synchronous_scraper(n):
    async_time = await async_request(n=n)
    sync_time = await sync_request(n=n)
    assert sync_time > async_time
