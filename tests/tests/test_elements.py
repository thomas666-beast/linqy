import pytest

from pylinq import Enumerable


# first / first_or_default
def test_first():
    assert Enumerable([1, 2, 3]).first() == 1


def test_first_with_predicate():
    assert Enumerable([1, 2, 3, 4]).first(lambda x: x > 2) == 3


def test_first_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).first()


def test_first_no_match_raises():
    with pytest.raises(ValueError):
        Enumerable([1, 2]).first(lambda x: x > 10)


def test_first_or_default():
    assert Enumerable([1, 2, 3]).first_or_default() == 1


def test_first_or_default_returns_default():
    assert Enumerable([]).first_or_default() is None
    assert Enumerable([]).first_or_default(default=-1) == -1


def test_first_or_default_with_predicate():
    assert Enumerable([1, 2, 3]).first_or_default(lambda x: x > 10, default=0) == 0


def test_first_stops_early():
    pulled = []

    def source():
        for i in range(100):
            pulled.append(i)
            yield i

    assert Enumerable(source()).first() == 0
    assert pulled == [0]


# single / single_or_default
def test_single():
    assert Enumerable([7]).single() == 7


def test_single_with_predicate():
    assert Enumerable([1, 2, 3]).single(lambda x: x > 2) == 3


def test_single_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).single()


def test_single_multiple_raises():
    with pytest.raises(ValueError):
        Enumerable([1, 2]).single()


def test_single_or_default_empty():
    assert Enumerable([]).single_or_default() is None
    assert Enumerable([]).single_or_default(default=5) == 5


def test_single_or_default_multiple_raises():
    with pytest.raises(ValueError):
        Enumerable([1, 2]).single_or_default()


# last / last_or_default
def test_last():
    assert Enumerable([1, 2, 3]).last() == 3


def test_last_with_predicate():
    assert Enumerable([1, 2, 3, 4]).last(lambda x: x < 3) == 2


def test_last_empty_raises():
    with pytest.raises(ValueError):
        Enumerable([]).last()


def test_last_or_default():
    assert Enumerable([1, 2, 3]).last_or_default() == 3
    assert Enumerable([]).last_or_default(default=9) == 9


# element_at / element_at_or_default
def test_element_at():
    assert Enumerable(["a", "b", "c"]).element_at(1) == "b"


def test_element_at_out_of_range():
    with pytest.raises(IndexError):
        Enumerable([1, 2]).element_at(5)


def test_element_at_negative():
    with pytest.raises(IndexError):
        Enumerable([1, 2]).element_at(-1)


def test_element_at_or_default():
    assert Enumerable([1, 2]).element_at_or_default(1) == 2
    assert Enumerable([1, 2]).element_at_or_default(5, default=0) == 0
    assert Enumerable([1, 2]).element_at_or_default(-1, default=0) == 0


# any / all / contains
def test_any_non_empty():
    assert Enumerable([1]).any() is True


def test_any_empty():
    assert Enumerable([]).any() is False


def test_any_with_predicate():
    assert Enumerable([1, 2, 3]).any(lambda x: x > 2) is True
    assert Enumerable([1, 2, 3]).any(lambda x: x > 5) is False


def test_any_short_circuits():
    pulled = []

    def source():
        for i in range(100):
            pulled.append(i)
            yield i

    assert Enumerable(source()).any(lambda x: x == 2) is True
    assert pulled == [0, 1, 2]


def test_all():
    assert Enumerable([2, 4, 6]).all(lambda x: x % 2 == 0) is True
    assert Enumerable([2, 3, 6]).all(lambda x: x % 2 == 0) is False


def test_all_empty_is_true():
    assert Enumerable([]).all(lambda x: False) is True


def test_contains():
    assert Enumerable([1, 2, 3]).contains(2) is True


def test_contains_missing():
    assert Enumerable([1, 2, 3]).contains(9) is False
