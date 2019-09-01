from abc import ABC, abstractmethod
import json
import socket
import time

import aiohttp
import asyncio


class TaskHandler(ABC):

    @abstractmethod
    async def on_task_started(self, **kwargs):
        pass

    @abstractmethod
    async def on_task_finished(self, **kwargs):
        pass

    def hash_key(self, key):
        key.pop("session", None)
        key.pop("scheduler", None)
        return json.dumps(key, sort_keys=True)


class Timer(TaskHandler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = {}
        self.request_duration = {}

    async def on_task_finished(self, **kwargs):
        self.request_duration[self.hash_key(kwargs)] = time.time() - self.start_time[self.hash_key(kwargs)]

    async def on_task_started(self, **kwargs):
        self.start_time[self.hash_key(kwargs)] = time.time()

    def total_taken_for_all_requests(self):
        return max(self.request_duration.values())

    def time_for_each_request(self):
        for (req, time) in self.request_duration.items():
            yield (req, time)


class DefaultTaskHandler(TaskHandler):

    async def on_task_finished(self, **kwargs):
        pass

    async def on_task_started(self, **kwargs):
        pass


class AsyncRequestScheduler:
    def __init__(self, wait=2, task_handler=DefaultTaskHandler()):
        self.work = []
        self._completed = 0
        self.wait = wait
        self.task_handler = task_handler

    def set_initial_callback(self, callback, **kwargs):
        self.initial_callback = callback
        self.initial_callback_kwargs = kwargs

    async def add_task(self, callback, **kwargs):
        kwargs["scheduler"] = self
        kwargs["session"] = self.session
        task = asyncio.create_task(callback(**kwargs))
        await self.task_handler.on_task_started(**kwargs)
        async with asyncio.Lock():
            self.work.append((task, kwargs))

    async def _run(self):
        while self.work:
            async with asyncio.Lock():
                task, kwargs = self.work.pop()

            await task
            await self.task_handler.on_task_finished(**kwargs)

            async with asyncio.Lock():
                self._completed += 1

            if len(self.work) == 0:
                await asyncio.sleep(self.wait)

    async def _setup(self, callback, **kwargs):
        kwargs["scheduler"] = self
        kwargs["session"] = self.session
        task = asyncio.create_task(callback(**kwargs))
        await self.task_handler.on_task_started(**kwargs)
        self.work.append((task, kwargs))
        await self._run()

    async def go(self):
        await self._setup(self.initial_callback, **self.initial_callback_kwargs)

    @property
    def completed(self):
        return self._completed

    async def __aenter__(self):

        connector = aiohttp.TCPConnector(
            family=socket.AF_INET,
            ssl=False,
        )
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
