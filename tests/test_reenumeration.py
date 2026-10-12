from pylinq import Enumerable


def test_query_can_be_enumerated_twice():
    query = Enumerable([1, 2, 3, 4]).where(lambda x: x % 2 == 0).select(lambda x: x * 10)
    assert query.to_list() == [20, 40]
    assert query.to_list() == [20, 40]


def test_other_operators_are_reusable():
    queries = [
        Enumerable([1, 2, 3]).take(2),
        Enumerable([1, 2, 3]).skip(1),
        Enumerable([[1], [2]]).select_many(lambda x: x),
        Enumerable([1, 1, 2]).distinct(),
        Enumerable([1, 2, 3]).chunk(2),
        Enumerable([1, 2]).reverse(),
        Enumerable([2, 1]).order_by(lambda x: x),
        Enumerable([1, 2, 3]).group_by(lambda x: x % 2),
    ]
    for q in queries:
        assert [list(x) if hasattr(x, "key") else x for x in q] == \
               [list(x) if hasattr(x, "key") else x for x in q]


def test_query_reflects_changes_to_source():
    data = [1, 2, 3]
    query = Enumerable(data).where(lambda x: x > 1)
    assert query.to_list() == [2, 3]
    data.append(4)
    assert query.to_list() == [2, 3, 4]


def test_each_enumeration_reruns_the_selector():
    calls = []
    query = Enumerable([1, 2]).select(lambda x: calls.append(x) or x)
    query.to_list()
    query.to_list()
    assert calls == [1, 2, 1, 2]


def test_wrapped_generator_is_still_one_shot():
    query = Enumerable(x for x in [1, 2, 3]).where(lambda x: x > 1)
    assert query.to_list() == [2, 3]
    assert query.to_list() == []
