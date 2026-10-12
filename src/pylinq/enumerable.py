from __future__ import annotations

from typing import Callable, Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Enumerable(Generic[T]):
    """Wraps any iterable and provides LINQ-style query operators.

    Operators return new Enumerable objects built on generators, so
    nothing runs until the result is iterated.
    """

    def __init__(self, source: Iterable[T]) -> None:
        self._source = source

    def __iter__(self) -> Iterator[T]:
        return iter(self._source)

    def to_list(self) -> list[T]:
        return list(self)

    def where(self, predicate: Callable[[T], bool]) -> Enumerable[T]:
        """Keep only the elements for which predicate returns True."""
        return Enumerable(x for x in self if predicate(x))

    def select(self, selector: Callable[[T], R]) -> Enumerable[R]:
        """Transform each element using selector."""
        return Enumerable(selector(x) for x in self)

    def __repr__(self) -> str:
        return f"Enumerable({self._source!r})"
