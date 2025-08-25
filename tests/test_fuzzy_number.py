import numpy as np
import pytest

from fuzzpy.numbers.trapezoidal import TrapezoidalFuzzyNumber
from fuzzpy.numbers.fuzzy_number import FuzzyNumber


def test_equality_and_hash():
    t1 = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    t2 = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    assert t1 == t2
    assert hash(t1) == hash(t2)


def test_radd_emits_warning_and_returns_shifted():
    t = TrapezoidalFuzzyNumber(0.0, 1.0, 2.0, 3.0)
    with pytest.warns(Warning):
        res = 2 + t
    assert isinstance(res, TrapezoidalFuzzyNumber)
    assert res.support() == (2.0, 5.0)


def test_bad_vectorized_function_shape_raises():
    # function returning wrong-shaped array should trigger validation error
    def bad_fun(x: np.ndarray) -> np.ndarray:
        # returns shape (1,) even when passed 2 elements
        return np.array([0.0])

    with pytest.raises(ValueError):
        FuzzyNumber(0.0, 1.0, 2.0, 3.0, left_fun=bad_fun, right_fun=bad_fun, lower=bad_fun, upper=bad_fun)
