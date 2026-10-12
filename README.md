# pylinq

LINQ-style query operators for Python. Chain `where`, `select`,
`order_by`, `group_by`, `join` and more over any iterable, with lazy
evaluation.

## Install

```bash
pip install -e .
```

## Example

```python
from pylinq import Enumerable

people = [
    {"name": "Ann", "age": 25, "city": "Munich"},
    {"name": "Bob", "age": 30, "city": "Berlin"},
    {"name": "Cy",  "age": 35, "city": "Munich"},
]

names = (
    Enumerable(people)
    .where(lambda p: p["age"] >= 30)
    .order_by(lambda p: p["name"])
    .select(lambda p: p["name"])
    .to_list()
)  # ['Bob', 'Cy']

by_city = (
    Enumerable(people)
    .group_by(lambda p: p["city"], result_selector=lambda k, g: (k, g.count()))
    .to_list()
)  # [('Munich', 2), ('Berlin', 1)]
```

## Operators

| Category | Operators |
|---|---|
| Filter / project | `where`, `select`, `select_many` |
| Ordering | `order_by`, `order_by_descending`, `then_by`, `then_by_descending`, `reverse` |
| Paging | `take`, `skip`, `take_while`, `skip_while`, `chunk` |
| Elements | `first`, `single`, `last`, `element_at` (+ `_or_default`), `any`, `all`, `contains` |
| Aggregation | `count`, `sum`, `min`, `max`, `average`, `aggregate` |
| Sets | `distinct`, `union`, `intersect`, `except_` |
| Grouping / joins | `group_by`, `join`, `group_join` |
| Other | `zip`, `concat`, `to_list`, `to_dict`, `to_set` |

## Behavior notes

- **Deferred execution:** operators that return an `Enumerable` do no work
  until you iterate. Operators that return a value (`first`, `count`, `sum`,
  `to_list`, ...) run immediately.
- **Re-enumerable:** a query can be enumerated more than once, and each
  enumeration re-runs it. The exception is a query built on a one-shot
  source such as a generator.
- **Errors:** where C# throws `InvalidOperationException`, pylinq raises
  `ValueError`. `element_at` raises `IndexError`.
- **Hashing:** set operations, `group_by`, `join`, and `to_dict` need
  hashable keys.

## Tests

```bash
pip install pytest
pytest
```
