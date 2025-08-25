import math
import pytest

from fuzzpy.numbers.trapezoidal import TrapezoidalFuzzyNumber


def test_support():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 3.0, 4.0)
    assert t.support() == (0.0, 4.0)


def test_left_endpoint_zero():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 3.0, 4.0)
    assert math.isclose(t.membership(0.0), 0.0)


def test_left_slope_midpoint():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 3.0, 4.0)
    assert math.isclose(t.membership(0.5), 0.5)


def test_core_membership_one():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 3.0, 4.0)
    assert math.isclose(t.membership(1.5), 1.0)


def test_right_slope_midpoint():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 3.0, 4.0)
    assert math.isclose(t.membership(3.5), 0.5)


def test_add_scalar_returns_shifted_support():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    t_add = t + 2.0
    assert isinstance(t_add, TrapezoidalFuzzyNumber)
    assert t_add.support() == (2.0, 5.0)


def test_mul_scalar_scales_support():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    t_mul = t * 3.0
    assert isinstance(t_mul, TrapezoidalFuzzyNumber)
    assert t_mul.support() == (0.0, 9.0)


def test_invalid_order_raises():
    with pytest.raises(ValueError):
        TrapezoidalFuzzyNumber(2.0, 1.0, 3.0, 4.0)
