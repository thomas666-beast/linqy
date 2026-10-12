from pylinq import Enumerable

PEOPLE = [("Bob", 30), ("Ann", 25), ("Cy", 30), ("Dee", 25)]


def test_order_by_ascending():
    assert Enumerable([3, 1, 2]).order_by(lambda x: x).to_list() == [1, 2, 3]


def test_order_by_descending():
    result = Enumerable([3, 1, 2]).order_by_descending(lambda x: x).to_list()
    assert result == [3, 2, 1]


def test_order_by_key_selector():
    result = Enumerable(["ccc", "a", "bb"]).order_by(len).to_list()
    assert result == ["a", "bb", "ccc"]


def test_order_by_is_stable():
    result = Enumerable(["bb", "aa", "c", "dd"]).order_by(len).to_list()
    assert result == ["c", "bb", "aa", "dd"]


def test_then_by():
    result = (
        Enumerable(PEOPLE)
        .order_by(lambda p: p[1])
        .then_by(lambda p: p[0])
        .to_list()
    )
    assert result == [("Ann", 25), ("Dee", 25), ("Bob", 30), ("Cy", 30)]


def test_then_by_descending():
    result = (
        Enumerable(PEOPLE)
        .order_by(lambda p: p[1])
        .then_by_descending(lambda p: p[0])
        .to_list()
    )
    assert result == [("Dee", 25), ("Ann", 25), ("Cy", 30), ("Bob", 30)]


def test_order_by_descending_then_by():
    result = (
        Enumerable(PEOPLE)
        .order_by_descending(lambda p: p[1])
        .then_by(lambda p: p[0])
        .to_list()
    )
    assert result == [("Bob", 30), ("Cy", 30), ("Ann", 25), ("Dee", 25)]


def test_chains_after_ordering():
    result = (
        Enumerable([5, 3, 8, 1])
        .order_by(lambda x: x)
        .where(lambda x: x > 1)
        .select(lambda x: x * 2)
        .to_list()
    )
    assert result == [6, 10, 16]


def test_deferred_execution():
    calls = []

    def key(x):
        calls.append(x)
        return x

    query = Enumerable([3, 1, 2]).order_by(key)
    assert calls == []
    assert query.to_list() == [1, 2, 3]
    assert sorted(calls) == [1, 2, 3]


def test_then_by_only_after_ordering():
    assert not hasattr(Enumerable([1, 2]), "then_by")
