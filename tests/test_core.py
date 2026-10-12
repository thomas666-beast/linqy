from linqy import Enumerable


def test_wraps_list():
    assert Enumerable([1, 2, 3]).to_list() == [1, 2, 3]


def test_wraps_generator():
    gen = (x for x in range(3))
    assert Enumerable(gen).to_list() == [0, 1, 2]


def test_wraps_range_and_string():
    assert Enumerable(range(3)).to_list() == [0, 1, 2]
    assert Enumerable("abc").to_list() == ["a", "b", "c"]


def test_is_iterable():
    assert [x for x in Enumerable([1, 2])] == [1, 2]


def test_empty():
    assert Enumerable([]).to_list() == []
