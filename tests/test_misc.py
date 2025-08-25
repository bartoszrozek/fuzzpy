import pytest

from fuzzpy.numbers.trapezoidal import TrapezoidalFuzzyNumber


def test_equality_with_non_fuzzy_is_false():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    assert not (t == 123)


def test_membership_outside_and_at_support_endpoints():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    assert t.membership(-1.0) == 0.0
    # at a4 expect 0 (right_fun at alpha==1 is 0 for trapezoid)
    assert t.membership(3.0) == 0.0


def test_scalar_mul_commutes_with_rmul():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    assert (t * 2.0) == (2.0 * t)
