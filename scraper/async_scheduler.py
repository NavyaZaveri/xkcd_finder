import asyncio
import socket

import aiohttp


async def _run(request, n):
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )

    async with aiohttp.ClientSession(connector=conn) as session:
        work = [request(session, req_count=i) for i in range(0, n)]
        await asyncio.gather(*work)


def schedule_request(request, n):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run(request, n))
