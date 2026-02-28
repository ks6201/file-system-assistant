
from typing import ClassVar, Optional, ParamSpec, TypeVar, Type, Dict, Any, Callable

T = TypeVar("T")

P = ParamSpec("P")
R = TypeVar("R")

RS = TypeVar("RS")

class Container:
    has_been_initialized = False
    pending_registrations: list[Callable[[], Any]] = []
    __container: ClassVar[Optional["Container"]] = None

    def __init__(self):
        self._singleton_map: Dict[Type[Any], Any] = {}
        self._transient_map: Dict[Type[Any], Callable[[], Any]] = {}

    def register_singleton(self, key: Type[T], factory: Callable[[], T]) -> None:
        self._singleton_map[key] = factory()

    def register_transient(self, key: Type[T], factory: Callable[[], T]) -> None:
        self._transient_map[key] = factory

    def resolve_aux(self, key: Type[T]) -> T:
        if key in self._singleton_map:
            return self._singleton_map[key]

        if key in self._transient_map:
            return self._transient_map[key]()

        raise RuntimeError(f"{key} is not registered")
    

    @staticmethod
    def singleton(key: Type[T], factory: Callable[[], T]):
        if Container.__container is None:
            Container.__container = Container()
        
        Container.__container.register_singleton(key, factory)

    @staticmethod
    def transient(key: Type[T], factory: Callable[[], T]):
        if Container.__container is None:
            Container.__container = Container()
        
        Container.__container.register_transient(key, factory)

    @staticmethod
    def init():
        if Container.__container is None:
            Container.__container = Container()

        Container.has_been_initialized = True
        if len(Container.pending_registrations) > 0:
            for callback in Container.pending_registrations:
                callback()
        
        return Container.__container

    @staticmethod
    def get_instance() -> "Container":
        
        if Container.__container is None:
            Container.__container = Container()
        
        return Container.__container
    
    @staticmethod
    def resolve(key: Type[RS]) -> RS:
        if Container.__container is None:
            Container.__container = Container()
        
        return Container.__container.resolve_aux(key)