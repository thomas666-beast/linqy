from __future__ import annotations

from typing import Callable, Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")
U = TypeVar("U")

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

    def select_many(
        self,
        selector: Callable[[T], Iterable[U]],
        result_selector: Optional[Callable[[T, U], R]] = None,
    ) -> Enumerable:
        """Project each element to a sequence and flatten the results.

        If result_selector is given, it is called with the original
        element and each inner item, and its return value is yielded.
        """
        def generate():
            for outer in self:
                for inner in selector(outer):
                    if result_selector is None:
                        yield inner
                    else:
                        yield result_selector(outer, inner)

        return Enumerable(generate())

    def __repr__(self) -> str:
        return f"Enumerable({self._source!r})"
