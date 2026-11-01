"""Unit tests for arithmetic results, errors, and operation logging.

Each ``pytest.mark.parametrize`` block runs the same test function with multiple
input combinations, keeping common arithmetic cases concise while checking
integers, decimal values, negative values, and zero where relevant.
"""

import logging

import pytest

from operations import add, divide, multiply, subtract


@pytest.mark.parametrize(
    # Each row supplies the two operands and the expected sum.
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (-2, 3, 1),
        (2.5, 3.5, 6.0),
        (0, 0, 0),
    ],
)
def test_add(a, b, expected):
    """Return the expected sum for integer, decimal, negative, and zero inputs."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    # Each row supplies the minuend, subtrahend, and expected difference.
    ("a", "b", "expected"),
    [
        (5, 3, 2),
        (-2, 3, -5),
        (2.5, 1.5, 1.0),
        (0, 7, -7),
    ],
)
def test_subtract(a, b, expected):
    """Return the expected difference for representative numeric inputs."""
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    # Each row supplies two factors and their expected product.
    ("a", "b", "expected"),
    [
        (4, 3, 12),
        (-2, 3, -6),
        (2.5, 4, 10.0),
        (0, 9, 0),
    ],
)
def test_multiply(a, b, expected):
    """Return the expected product, including negative and zero cases."""
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    # Each row supplies the dividend, non-zero divisor, and expected quotient.
    ("a", "b", "expected"),
    [
        (6, 3, 2.0),
        (7, 2, 3.5),
        (2.5, 2, 1.25),
        (-8, 4, -2.0),
    ],
)
def test_divide(a, b, expected):
    """Return the expected quotient for integer and decimal operands."""
    assert divide(a, b) == expected


def test_divide_by_zero_raises_value_error():
    """Reject a zero divisor with the documented exception and message."""
    with pytest.raises(ValueError, match="Cannot divide by zero!"):
        divide(5, 0)


@pytest.mark.parametrize(
    # Pair each operation with sample arguments and the expected log text.
    ("operation", "arguments", "log_message"),
    [
        (add, (2, 3), "Addition: 2 + 3 = 5"),
        (subtract, (5, 3), "Subtraction: 5 - 3 = 2"),
        (multiply, (2, 3), "Multiplication: 2 * 3 = 6"),
        (divide, (6, 3), "Division: 6 / 3 = 2.0"),
    ],
)
def test_successful_operations_are_logged(caplog, operation, arguments, log_message):
    """Capture INFO logs and verify each successful operation is recorded."""
    with caplog.at_level(logging.INFO, logger="operations"):
        operation(*arguments)

    assert log_message in caplog.text


def test_division_by_zero_is_logged(caplog):
    """Capture the WARNING emitted when division by zero is rejected."""
    with caplog.at_level(logging.WARNING, logger="operations"):
        with pytest.raises(ValueError, match="Cannot divide by zero!"):
            divide(5, 0)

    assert "Division rejected because the divisor is zero" in caplog.text
