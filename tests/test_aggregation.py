import pytest

from pylinq import Enumerable


# count
def test_count():
    assert Enumerable([1, 2, 3]).count() == 3


def test_count_empty():
    assert Enumerable([]).count() == 0


def test_count_with_predicate():
    assert Enumerable([1, 2, 3, 4]).count(lambda x: x % 2 == 0) == 2


# sum
def test_sum():
    assert Enumerable([1, 2, 3]).sum() == 6


def test_sum_empty():
    assert Enumerable([]).sum() == 0


def test_sum_with_selector():
    assert Enumerable(["a", "bb", "ccc"]).sum(len) == 6


def test_sum_floats():
    assert Enumerable([0.5, 1.5]).sum() == 2.0


# min / max
def test_min():
    assert Enumerable([3, 1, 2]).min() == 1


def test_max():
    assert Enumerable([3, 1, 2]).max() == 3


def test_min_max_with_selector():
    words = ["ccc", "a", "bb"]
    assert Enumerable(words).min(len) == 1
    assert Enumerable(words).max(len) == 3


def test_min_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).min()


def test_max_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).max()


def test_min_max_single_element():
    assert Enumerable([5]).min() == 5
    assert Enumerable([5]).max() == 5


# average
def test_average():
    assert Enumerable([1, 2, 3, 4]).average() == 2.5


def test_average_with_selector():
    assert Enumerable(["a", "bbb"]).average(len) == 2.0


def test_average_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).average()


# aggregate
def test_aggregate_no_seed():
    assert Enumerable([1, 2, 3, 4]).aggregate(lambda a, x: a + x) == 10


def test_aggregate_with_seed():
    assert Enumerable([1, 2, 3]).aggregate(lambda a, x: a + x, 100) == 106


def test_aggregate_builds_string():
    result = Enumerable(["a", "b", "c"]).aggregate(lambda a, x: a + "-" + x)
    assert result == "a-b-c"


def test_aggregate_empty_with_seed_returns_seed():
    assert Enumerable([]).aggregate(lambda a, x: a + x, 42) == 42


def test_aggregate_empty_without_seed_raises():
    with pytest.raises(ValueError):
        Enumerable([]).aggregate(lambda a, x: a + x)


def test_aggregate_seed_can_be_none():
    result = Enumerable([1, 2]).aggregate(lambda a, x: (a or 0) + x, None)
    assert result == 3


def test_chains_after_where():
    result = Enumerable(range(1, 11)).where(lambda x: x % 2 == 0).sum()
    assert result == 30
