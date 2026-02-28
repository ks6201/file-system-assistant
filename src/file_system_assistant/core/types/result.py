

from abc import abstractmethod
from typing import Any, Callable, Generic, TypeVar

OK_VALUE_TYPE = TypeVar("OK_VALUE_TYPE")
ERR_VALUE_TYPE = TypeVar("ERR_VALUE_TYPE")

OR_ELSE_RETURN_TYPE = TypeVar("OR_ELSE_RETURN_TYPE")

MAP_ERROR_RETURN_TYPE = TypeVar("MAP_ERROR_RETURN_TYPE")

OK_FACTORY_RETURN_TYPE = TypeVar("OK_FACTORY_RETURN_TYPE")
ERR_FACTORY_RETURN_TYPE = TypeVar("ERR_FACTORY_RETURN_TYPE")

class Result(Generic[OK_VALUE_TYPE, ERR_VALUE_TYPE]):

    def __init__(self, value: OK_VALUE_TYPE | None, error: ERR_VALUE_TYPE | None):
        self._value = value
        self._error = error

    @abstractmethod
    def unwrap(self) -> OK_VALUE_TYPE:
        ...

    @abstractmethod
    def unwrap_or_else(self, else_value: OR_ELSE_RETURN_TYPE) -> OK_VALUE_TYPE | OR_ELSE_RETURN_TYPE:
        ...
    
    @abstractmethod
    def unwrap_err(self) -> ERR_VALUE_TYPE:
        ...

    @abstractmethod
    def map_err(self, err_handler: Callable[[ERR_VALUE_TYPE], MAP_ERROR_RETURN_TYPE]) -> MAP_ERROR_RETURN_TYPE:
        ...

    def is_ok(self) -> bool:
        return self._value is not None

    @abstractmethod
    def is_err(self) -> bool:
        return self._error is not None

    @staticmethod
    def ok(value: OK_FACTORY_RETURN_TYPE) -> "Ok[OK_FACTORY_RETURN_TYPE]":
        return Ok(value)
    
    @staticmethod
    def err(error: ERR_FACTORY_RETURN_TYPE) -> "Err[ERR_FACTORY_RETURN_TYPE]":
        return Err(error)    


class Ok(Generic[OK_VALUE_TYPE], Result[OK_VALUE_TYPE, Any]):

    def __init__(self, value: OK_VALUE_TYPE) -> None:
        super().__init__(value, None)

    def unwrap(self) -> OK_VALUE_TYPE:
        if self._value is None:
            raise RuntimeError("Failed to unwrap.")
        
        return self._value
    
    def unwrap_or_else(self, else_value: OR_ELSE_RETURN_TYPE) -> OK_VALUE_TYPE | OR_ELSE_RETURN_TYPE:
        if self._value is None:
            return else_value
        
        return self._value
    
    def unwrap_err(self) -> None:
        if self._value is not None:
            raise RuntimeError("Value is present")
        
    def map_err(self, err_handler: Callable[[None], MAP_ERROR_RETURN_TYPE]) -> MAP_ERROR_RETURN_TYPE:
        raise RuntimeError("Cannot map error with Ok type")
    
    def is_ok(self) -> bool:
        return self._value is not None
    
    def is_err(self) -> bool:
        return self._value is None


class Err(Generic[ERR_VALUE_TYPE], Result[Any, ERR_VALUE_TYPE]):
    _error: ERR_VALUE_TYPE | None = None
    
    def __init__(self, err: ERR_VALUE_TYPE) -> None:
        super().__init__(None, err)

    def unwrap(self) -> None:
        raise RuntimeError("Nothing to unwrap, it's an error")

    def unwrap_or_else(self, else_value: OR_ELSE_RETURN_TYPE) -> OR_ELSE_RETURN_TYPE:
        return else_value
    
    def unwrap_err(self) -> ERR_VALUE_TYPE:
        if self._error is None:
            raise RuntimeError("No error found")
        return self._error
    
    def map_err(self, err_handler: Callable[[ERR_VALUE_TYPE], MAP_ERROR_RETURN_TYPE]) -> MAP_ERROR_RETURN_TYPE:
        if self._error is None:
            raise RuntimeError("No error found")
        
        return err_handler(self._error)
    
    def is_err(self) -> bool:
        return self._error is not None
    
    def is_ok(self) -> bool:
        return self._error is None