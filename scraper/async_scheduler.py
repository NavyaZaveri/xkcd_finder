from abc import ABC, abstractmethod
import asyncio


class TaskHandler(ABC):

    @abstractmethod
    def on_task_started(self, **kwargs):
        pass

    @abstractmethod
    def on_task_finished(self, **kwargs):
        pass


class DefaultTaskHandler(TaskHandler):

    def on_task_finished(self, **kwargs):
        pass

    def on_task_started(self, **kwargs):
        pass


class AsyncScheduler:
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
        task = asyncio.create_task(callback(**kwargs))
        self.task_handler.on_task_started(**kwargs)
        async with asyncio.Lock():
            self.work.append((task, kwargs))

    async def _run(self):
        while self.work:
            async with asyncio.Lock():
                task, kwargs = self.work.pop()

            await task
            self.task_handler.on_task_finished(**kwargs)

            async with asyncio.Lock():
                self._completed += 1

            if len(self.work) == 0:
                await asyncio.sleep(self.wait)

    async def _setup(self, callback, **kwargs):
        kwargs["scheduler"] = self
        task = asyncio.create_task(callback(**kwargs))
        self.work.append((task, kwargs))
        await self._run()

    def go(self):
        asyncio.run(self._setup(self.initial_callback, **self.initial_callback_kwargs))

    @property
    def completed(self):
        return self._completed
