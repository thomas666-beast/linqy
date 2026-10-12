import pytest

from linqy import Enumerable


# zip
def test_zip():
    result = Enumerable([1, 2, 3]).zip(["a", "b", "c"]).to_list()
    assert result == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_stops_at_shortest():
    assert Enumerable([1, 2, 3]).zip(["a"]).to_list() == [(1, "a")]
    assert Enumerable([1]).zip(["a", "b"]).to_list() == [(1, "a")]


def test_zip_result_selector():
    result = Enumerable([1, 2]).zip([10, 20], lambda a, b: a + b).to_list()
    assert result == [11, 22]


def test_zip_empty():
    assert Enumerable([]).zip([1, 2]).to_list() == []


# concat
def test_concat():
    assert Enumerable([1, 2]).concat([3, 4]).to_list() == [1, 2, 3, 4]


def test_concat_keeps_duplicates():
    assert Enumerable([1, 2]).concat([2, 3]).to_list() == [1, 2, 2, 3]


def test_concat_with_enumerable_and_generator():
    assert Enumerable([1]).concat(Enumerable([2])).to_list() == [1, 2]
    assert Enumerable([1]).concat(x for x in [2, 3]).to_list() == [1, 2, 3]


# reverse
def test_reverse():
    assert Enumerable([1, 2, 3]).reverse().to_list() == [3, 2, 1]


def test_reverse_empty():
    assert Enumerable([]).reverse().to_list() == []


def test_reverse_after_order_by():
    result = Enumerable([2, 3, 1]).order_by(lambda x: x).reverse().to_list()
    assert result == [3, 2, 1]


def test_reverse_deferred_execution():
    calls = []

    def track(x):
        calls.append(x)
        return x

    query = Enumerable([1, 2, 3]).select(track).reverse()
    assert calls == []
    assert query.to_list() == [3, 2, 1]
    assert calls == [1, 2, 3]


# to_dict
def test_to_dict():
    result = Enumerable(["a", "bb", "ccc"]).to_dict(len)
    assert result == {1: "a", 2: "bb", 3: "ccc"}


def test_to_dict_element_selector():
    result = Enumerable(["a", "bb"]).to_dict(lambda s: s, len)
    assert result == {"a": 1, "bb": 2}


def test_to_dict_duplicate_key_raises():
    with pytest.raises(ValueError):
        Enumerable(["a", "b"]).to_dict(len)


def test_to_dict_empty():
    assert Enumerable([]).to_dict(lambda x: x) == {}


# to_set
def test_to_set():
    assert Enumerable([1, 2, 2, 3]).to_set() == {1, 2, 3}


def test_to_set_empty():
    assert Enumerable([]).to_set() == set()
