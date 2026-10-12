from __future__ import annotations

from itertools import islice
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

    def take(self, count: int) -> Enumerable[T]:
        """Return the first `count` elements. Non-positive counts give an empty sequence."""
        return Enumerable(islice(self, max(count, 0)))

    def skip(self, count: int) -> Enumerable[T]:
        """Skip the first `count` elements and return the rest."""
        return Enumerable(islice(self, max(count, 0), None))

    def take_while(self, predicate: Callable[[T], bool]) -> Enumerable[T]:
        """Return elements while predicate is True, stopping at the first failure."""
        def generate():
            for x in self:
                if not predicate(x):
                    return
                yield x

        return Enumerable(generate())

    def skip_while(self, predicate: Callable[[T], bool]) -> Enumerable[T]:
        """Skip elements while predicate is True, then return everything after."""
        def generate():
            skipping = True
            for x in self:
                if skipping and predicate(x):
                    continue
                skipping = False
                yield x

        return Enumerable(generate())

    def chunk(self, size: int) -> Enumerable[list[T]]:
        """Split the sequence into lists of at most `size` elements."""
        if size < 1:
            raise ValueError("size must be greater than 0")

        def generate():
            it = iter(self)
            while True:
                batch = list(islice(it, size))
                if not batch:
                    return
                yield batch

        return Enumerable(generate())

    def first(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        """Return the first element (matching predicate, if given). Raises ValueError if none."""
        for x in self:
            if predicate is None or predicate(x):
                return x
        raise ValueError("Sequence contains no matching element")

    def first_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Any = None,
    ) -> Any:
        """Like first, but returns `default` instead of raising."""
        for x in self:
            if predicate is None or predicate(x):
                return x
        return default

    def single(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        """Return the only matching element. Raises ValueError if there are none or several."""
        found = False
        result = None
        for x in self:
            if predicate is None or predicate(x):
                if found:
                    raise ValueError("Sequence contains more than one matching element")
                found = True
                result = x
        if not found:
            raise ValueError("Sequence contains no matching element")
        return result

    def single_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Any = None,
    ) -> Any:
        """Return the only matching element, or `default` if none. Raises if several."""
        found = False
        result = default
        for x in self:
            if predicate is None or predicate(x):
                if found:
                    raise ValueError("Sequence contains more than one matching element")
                found = True
                result = x
        return result

    def last(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        """Return the last element (matching predicate, if given). Raises ValueError if none."""
        found = False
        result = None
        for x in self:
            if predicate is None or predicate(x):
                found = True
                result = x
        if not found:
            raise ValueError("Sequence contains no matching element")
        return result

    def last_or_default(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Any = None,
    ) -> Any:
        """Like last, but returns `default` instead of raising."""
        result = default
        for x in self:
            if predicate is None or predicate(x):
                result = x
        return result

    def element_at(self, index: int) -> T:
        """Return the element at a zero-based index. Raises IndexError if out of range."""
        if index < 0:
            raise IndexError("index must be non-negative")
        for i, x in enumerate(self):
            if i == index:
                return x
        raise IndexError("index out of range")

    def element_at_or_default(self, index: int, default: Any = None) -> Any:
        """Like element_at, but returns `default` instead of raising."""
        if index < 0:
            return default
        for i, x in enumerate(self):
            if i == index:
                return x
        return default

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """True if the sequence has any element (matching predicate, if given)."""
        for x in self:
            if predicate is None or predicate(x):
                return True
        return False

    def all(self, predicate: Callable[[T], bool]) -> bool:
        """True if every element satisfies predicate (vacuously True when empty)."""
        for x in self:
            if not predicate(x):
                return False
        return True

    def contains(self, value: T) -> bool:
        """True if the sequence contains `value` (compared with ==)."""
        for x in self:
            if x == value:
                return True
        return False

    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        """Count elements, or only those matching predicate."""
        total = 0
        for x in self:
            if predicate is None or predicate(x):
                total += 1
        return total

    def sum(self, selector: Optional[Callable[[T], Any]] = None) -> Any:
        """Sum the elements (or the selected values). Empty gives 0."""
        total = 0
        for x in self:
            total += x if selector is None else selector(x)
        return total

    def min(self, selector: Optional[Callable[[T], Any]] = None) -> Any:
        """Smallest element (or selected value). Raises ValueError if empty."""
        it = iter(self)
        try:
            first = next(it)
        except StopIteration:
            raise ValueError("Sequence contains no elements") from None
        result = first if selector is None else selector(first)
        for x in it:
            value = x if selector is None else selector(x)
            if value < result:
                result = value
        return result

    def max(self, selector: Optional[Callable[[T], Any]] = None) -> Any:
        """Largest element (or selected value). Raises ValueError if empty."""
        it = iter(self)
        try:
            first = next(it)
        except StopIteration:
            raise ValueError("Sequence contains no elements") from None
        result = first if selector is None else selector(first)
        for x in it:
            value = x if selector is None else selector(x)
            if value > result:
                result = value
        return result

    def average(self, selector: Optional[Callable[[T], Any]] = None) -> float:
        """Mean of the elements (or selected values). Raises ValueError if empty."""
        total = 0
        n = 0
        for x in self:
            total += x if selector is None else selector(x)
            n += 1
        if n == 0:
            raise ValueError("Sequence contains no elements")
        return total / n

    _NO_SEED = object()

    def aggregate(
        self,
        func: Callable[[Any, T], Any],
        seed: Any = _NO_SEED,
    ) -> Any:
        """Fold the sequence with func(accumulator, element).

        Without a seed, the first element is the starting accumulator
        (ValueError if empty). With a seed, an empty sequence returns it.
        """
        it = iter(self)
        if seed is Enumerable._NO_SEED:
            try:
                acc = next(it)
            except StopIteration:
                raise ValueError("Sequence contains no elements") from None
        else:
            acc = seed
        for x in it:
            acc = func(acc, x)
        return acc

    def distinct(
        self, key_selector: Optional[Callable[[T], Any]] = None
    ) -> Enumerable[T]:
        """Remove duplicates, keeping the first occurrence of each.

        If key_selector is given, uniqueness is decided by the selected key.
        """
        def generate():
            seen = set()
            for x in self:
                key = x if key_selector is None else key_selector(x)
                if key not in seen:
                    seen.add(key)
                    yield x

        return Enumerable(generate())

    def union(self, second: Iterable[T]) -> Enumerable[T]:
        """Distinct elements from this sequence followed by those from `second`."""
        def generate():
            seen = set()
            for source in (self, second):
                for x in source:
                    if x not in seen:
                        seen.add(x)
                        yield x

        return Enumerable(generate())

    def intersect(self, second: Iterable[T]) -> Enumerable[T]:
        """Distinct elements that appear in both sequences, in this sequence's order."""
        def generate():
            allowed = set(second)
            seen = set()
            for x in self:
                if x in allowed and x not in seen:
                    seen.add(x)
                    yield x

        return Enumerable(generate())

    def except_(self, second: Iterable[T]) -> Enumerable[T]:
        """Distinct elements of this sequence that do not appear in `second`."""
        def generate():
            seen = set(second)
            for x in self:
                if x not in seen:
                    seen.add(x)
                    yield x

        return Enumerable(generate())

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
