from dataclasses import asdict, dataclass
import dataclasses
from functools import wraps
from typing import Any, Callable, Generic, ParamSpec, TypeVar

ERROR_TYPE = TypeVar("ERROR_TYPE")
SUCCESS_TYPE = TypeVar("SUCCESS_TYPE")

@dataclass
class SuccessResponse(Generic[SUCCESS_TYPE]):
    response: SUCCESS_TYPE
    is_error: bool = False


@dataclass
class ErrorResponse(Generic[ERROR_TYPE]):
    error: ERROR_TYPE
    is_error: bool = True

type ToolResponse = dict[str, Any] | None

P = ParamSpec("P")
R = TypeVar("R")

def tool_response(func: Callable[P, R]) -> Callable[P, dict[str, Any]]:
    """
    Decorator that converts a dataclass return value into a dictionary.

    This decorator wraps a function and enforces that its return value is
    an instance of a dataclass. The returned dataclass instance is then
    converted to a dictionary using ``dataclasses.asdict`` before being
    returned to the caller.

    The decorated function retains its original signature via ``functools.wraps``.

    Type Parameters:
        P: Parameter specification for the wrapped function.
        R: Return type of the wrapped function (expected to be a dataclass instance).

    Args:
        func (Callable[P, R]): The function to wrap. It must return
            a dataclass instance (not a dataclass type).

    Returns:
        Callable[P, dict[str, Any]]: A wrapped function that returns
        the dictionary representation of the dataclass instance.

    Raises:
        Exception: If the wrapped function does not return a dataclass instance,
            or if it returns a dataclass type instead of an instance.

    Example:
        >>> from dataclasses import dataclass
        >>>
        >>> @dataclass
        ... class User:
        ...     id: int
        ...     name: str
        >>>
        >>> @transform_response
        ... def get_user() -> User:
        ...     return User(id=1, name="Alice")
        >>>
        >>> get_user()
        {'id': 1, 'name': 'Alice'}
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> dict[str, Any]:
        result = func(*args, **kwargs)

        if not dataclasses.is_dataclass(result) or isinstance(result, type):
            raise RuntimeError(f"{func.__name__} should return dataclass instance")

        return asdict(result)

    return wrapper