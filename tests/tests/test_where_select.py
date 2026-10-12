from pylinq import Enumerable


def test_where_filters():
    result = Enumerable([1, 2, 3, 4, 5]).where(lambda x: x % 2 == 0).to_list()
    assert result == [2, 4]


def test_where_no_matches():
    assert Enumerable([1, 2, 3]).where(lambda x: x > 10).to_list() == []


def test_select_transforms():
    result = Enumerable([1, 2, 3]).select(lambda x: x * 10).to_list()
    assert result == [10, 20, 30]


def test_select_changes_type():
    result = Enumerable([1, 2, 3]).select(str).to_list()
    assert result == ["1", "2", "3"]


def test_chaining():
    result = (
        Enumerable(range(10))
        .where(lambda x: x % 2 == 0)
        .select(lambda x: x * x)
        .to_list()
    )
    assert result == [0, 4, 16, 36, 64]


def test_deferred_execution():
    calls = []

    def track(x):
        calls.append(x)
        return x

    query = Enumerable([1, 2, 3]).select(track)
    assert calls == []          # nothing has run yet
    query.to_list()
    assert calls == [1, 2, 3]   # runs only on enumeration
