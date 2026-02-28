from __future__ import annotations
from typing import Generic, TypeVar

OptionalT = TypeVar("OptionalT") 

T = TypeVar("T")

class Optional(Generic[OptionalT]):

    @staticmethod
    def of(value: T) -> "Optional[T]":
        return Optional(value, True)

    @staticmethod
    def empty() -> "Optional[T]": # type: ignore
        return Optional(None, False)

    @staticmethod
    def of_nullable(value: OptionalT | None) -> Optional[OptionalT]:
        return Optional(None, value is not None)

    def __init__(self, value: OptionalT | None, is_present: bool) -> None:
        self.__value = value
        self.__is_present = is_present

    def get(self) -> OptionalT:
        if self.__value is None:
            raise ValueError("No value present")
        return self.__value
    
    def get_or_else_throw(self, exception: Exception) -> OptionalT:
        if self.__value is None:
            raise exception
        
        return self.__value
    
    def get_or_else(self, other: OptionalT) -> OptionalT:
        if self.__value is None:
            return other
        
        return self.__value
    
    def is_present(self) -> bool:
        return self.__is_present

    def is_empty(self) -> bool:
        return not self.__is_present