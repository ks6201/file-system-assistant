

from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

def bootstrap(fns: list[Callable[[], Any]]) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for fn in fns: fn()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator