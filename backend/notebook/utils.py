import asyncio
import functools
from typing import Any, Callable


def task(f: Callable) -> Callable:
    """wraps an async function to be execute as a Task in the background of the event loop"""

    def inner(*args: Any, **kwargs: Any) -> asyncio.Task:
        return asyncio.create_task(f(*args, **kwargs))

    functools.update_wrapper(inner, f)
    return inner
