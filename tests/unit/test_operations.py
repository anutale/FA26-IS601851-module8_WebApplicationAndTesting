import pytest

from operations import add, divide, multiply, subtract


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (-2, 3, 1),
        (2.5, 3.5, 6.0),
        (0, 0, 0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (5, 3, 2),
        (-2, 3, -5),
        (2.5, 1.5, 1.0),
        (0, 7, -7),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (4, 3, 12),
        (-2, 3, -6),
        (2.5, 4, 10.0),
        (0, 9, 0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (6, 3, 2.0),
        (7, 2, 3.5),
        (2.5, 2, 1.25),
        (-8, 4, -2.0),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero!"):
        divide(5, 0)
