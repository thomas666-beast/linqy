from pylinq import Enumerable

CUSTOMERS = [
    {"id": 1, "name": "Ann"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Cy"},
]
ORDERS = [
    {"customer_id": 1, "item": "book"},
    {"customer_id": 2, "item": "pen"},
    {"customer_id": 1, "item": "lamp"},
    {"customer_id": 9, "item": "ghost"},
]


# group_by
def test_group_by_key():
    groups = Enumerable([1, 2, 3, 4, 5, 6]).group_by(lambda x: x % 2).to_list()
    assert [(g.key, g.to_list()) for g in groups] == [(1, [1, 3, 5]), (0, [2, 4, 6])]


def test_group_by_first_appearance_order():
    groups = Enumerable(["b1", "a1", "b2", "a2"]).group_by(lambda s: s[0]).to_list()
    assert [g.key for g in groups] == ["b", "a"]


def test_group_by_element_selector():
    groups = Enumerable(["apple", "avocado", "banana"]).group_by(
        lambda w: w[0], lambda w: len(w)
    )
    assert [(g.key, g.to_list()) for g in groups] == [("a", [5, 7]), ("b", [6])]


def test_group_by_result_selector():
    result = (
        Enumerable([1, 2, 3, 4, 5])
        .group_by(lambda x: x % 2, result_selector=lambda k, g: (k, g.sum()))
        .to_list()
    )
    assert result == [(1, 9), (0, 6)]


def test_group_by_empty():
    assert Enumerable([]).group_by(lambda x: x).to_list() == []


def test_group_is_enumerable():
    group = Enumerable([1, 2, 3, 4]).group_by(lambda x: x % 2).first()
    assert group.where(lambda x: x > 1).to_list() == [3]
    assert group.count() == 2


def test_group_by_deferred_execution():
    calls = []

    def key(x):
        calls.append(x)
        return x % 2

    query = Enumerable([1, 2, 3]).group_by(key)
    assert calls == []
    query.to_list()
    assert calls == [1, 2, 3]


# join
def test_join():
    result = (
        Enumerable(CUSTOMERS)
        .join(
            ORDERS,
            lambda c: c["id"],
            lambda o: o["customer_id"],
            lambda c, o: (c["name"], o["item"]),
        )
        .to_list()
    )
    assert result == [("Ann", "book"), ("Ann", "lamp"), ("Bob", "pen")]


def test_join_excludes_unmatched():
    result = Enumerable([1, 2, 3]).join(
        [2, 3, 4], lambda x: x, lambda y: y, lambda x, y: (x, y)
    ).to_list()
    assert result == [(2, 2), (3, 3)]


def test_join_multiple_matches_on_both_sides():
    result = Enumerable([1, 1]).join(
        ["a", "b"], lambda x: x, lambda s: 1, lambda x, s: s
    ).to_list()
    assert result == ["a", "b", "a", "b"]


def test_join_deferred_execution():
    calls = []

    def inner_key(y):
        calls.append(y)
        return y

    query = Enumerable([1]).join([1, 2], lambda x: x, inner_key, lambda x, y: y)
    assert calls == []
    assert query.to_list() == [1]
    assert calls == [1, 2]


# group_join
def test_group_join():
    result = (
        Enumerable(CUSTOMERS)
        .group_join(
            ORDERS,
            lambda c: c["id"],
            lambda o: o["customer_id"],
            lambda c, orders: (c["name"], orders.select(lambda o: o["item"]).to_list()),
        )
        .to_list()
    )
    assert result == [("Ann", ["book", "lamp"]), ("Bob", ["pen"]), ("Cy", [])]


def test_group_join_includes_outer_without_matches():
    result = Enumerable([1, 2]).group_join(
        [], lambda x: x, lambda y: y, lambda x, ys: (x, ys.count())
    ).to_list()
    assert result == [(1, 0), (2, 0)]


def test_group_join_inner_can_be_generator():
    result = Enumerable([1, 2]).group_join(
        (y for y in [2, 2, 3]),
        lambda x: x,
        lambda y: y,
        lambda x, ys: (x, ys.count()),
    ).to_list()
    assert result == [(1, 0), (2, 2)]
