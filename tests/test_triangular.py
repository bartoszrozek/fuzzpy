import pytest

from fuzzpy.numbers.triangular import TriangularFuzzyNumber


def test_left_mid_right_properties():
    tri = TriangularFuzzyNumber(0.0, 1.0, 2.0)
    assert tri.left == 0.0
    assert tri.mid == 1.0
    assert tri.right == 2.0


def test_repr_contains_classname():
    tri = TriangularFuzzyNumber(0.0, 1.0, 2.0)
    assert 'TriangularFuzzyNumber' in repr(tri)


def test_add_two_triangulars():
    a = TriangularFuzzyNumber(0.0, 1.0, 2.0)
    b = TriangularFuzzyNumber(1.0, 2.0, 3.0)
    c = a + b
    assert isinstance(c, TriangularFuzzyNumber)
    assert (c.left, c.mid, c.right) == (1.0, 3.0, 5.0)


def test_add_scalar_to_triangular():
    a = TriangularFuzzyNumber(0.0, 1.0, 2.0)
    d = a + 2.0
    assert (d.left, d.mid, d.right) == (2.0, 3.0, 4.0)


def test_mul_scalar_with_triangular():
    a = TriangularFuzzyNumber(0.0, 1.0, 2.0)
    e = a * 4.0
    assert (e.left, e.mid, e.right) == (0.0, 4.0, 8.0)


def test_triangular_invalid_order():
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(2.0, 1.0, 0.0)
