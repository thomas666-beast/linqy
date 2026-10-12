from __future__ import annotations

from typing import Any, Callable, Generic, Iterable, Iterator, Optional, TypeVar

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

    def order_by(self, key_selector: Callable[[T], Any]) -> OrderedEnumerable[T]:
        """Sort ascending by the key returned from key_selector."""
        return OrderedEnumerable(self, [(key_selector, False)])

    def order_by_descending(
        self, key_selector: Callable[[T], Any]
    ) -> OrderedEnumerable[T]:
        """Sort descending by the key returned from key_selector."""
        return OrderedEnumerable(self, [(key_selector, True)])

    def __repr__(self) -> str:
        return f"Enumerable({self._source!r})"

class OrderedEnumerable(Enumerable[T]):
    """An Enumerable with a sort order. Supports then_by chaining.

    Sorting happens when the sequence is iterated, not when it is built.
    """

    def __init__(
        self,
        source: Iterable[T],
        keys: list[tuple[Callable[[T], Any], bool]],
    ) -> None:
        super().__init__(source)
        self._keys = keys  # list of (key_selector, descending)

    def __iter__(self) -> Iterator[T]:
        items = list(self._source)
        # sort() is stable, so sorting by the last key first and the
        # first key last gives the correct multi-key ordering.
        for key, descending in reversed(self._keys):
            items.sort(key=key, reverse=descending)
        return iter(items)

    def then_by(self, key_selector: Callable[[T], Any]) -> OrderedEnumerable[T]:
        """Add a secondary ascending sort key."""
        return OrderedEnumerable(self._source, self._keys + [(key_selector, False)])

    def then_by_descending(
        self, key_selector: Callable[[T], Any]
    ) -> OrderedEnumerable[T]:
        """Add a secondary descending sort key."""
        return OrderedEnumerable(self._source, self._keys + [(key_selector, True)])
