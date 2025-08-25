# Quick start

This page shows short, practical examples to get you started with creating and working with fuzzy numbers and arrays.

## Imports

```python
import numpy as np
from fuzzpy.fuzzpy.numbers import (
	TriangularFuzzyNumber,
	TrapezoidalFuzzyNumber,
	FuzzyNumber,
)
from fuzzpy.fuzzpy.structs import FuzzyNumberArray
from fuzzpy.fuzzpy.config import set_fuzzy_addition_method, get_fuzzy_addition_method
```

## Create basic fuzzy numbers

```python
# Triangular: (left, mid, right)
a = TriangularFuzzyNumber(0, 1, 2)

# Trapezoidal: (a1, a2, a3, a4)
b = TrapezoidalFuzzyNumber(0, 1, 2, 3)

# FuzzyNumber with custom membership helpers
import numpy as np
d = FuzzyNumber(0, 1, 2, 3, left_fun=np.sin, right_fun=np.cos)
```

## Arithmetic and scalar operations

```python
# scalar multiplication
a2 = a * 2
a3 = a * 3

# scalar addition (using configured addition method)
c = TriangularFuzzyNumber(1, 2, 3) + 5.0
```

## FuzzyNumberArray — fixed-size containers

```python
v = FuzzyNumberArray([a, b, c])
len(v)          # sequence behaviour
v[0]            # indexing
v[:2]           # slicing -> FuzzyNumberArray
v[ [0,2] ]      # fancy indexing -> FuzzyNumberArray
```

Vectorized access to components is supported via attribute lookup:

```python
v.mid           # numpy array of center (a2) values for each element
v.left          # same for left bound
v.right         # same for right bound
```

## Plotting membership functions

FuzzyNumberArray includes a convenience `plot()` method (uses plotnine). It will automatically
choose a compact sampling for triangular/trapezoidal numbers and a denser sampling for arbitrary
fuzzy numbers.

```python
n = 10
cm = np.linspace(0, 10, n)
array = FuzzyNumberArray.random_triangular(
	n=n, c_mu=cm, c_sigma=0.5, l1=0.2, l2=0.5, r1=0.2, r2=0.5
)

array.plot()        # show membership functions for the generated sample
(array + 2).plot()  # plot after adding a scalar to each element
```

## Example: computing the ICr (interval central region) for a triangular array

The notebook shows a small helper that computes the ICr-alpha value for a vector of triangular fuzzy numbers.
When given a `FuzzyNumberArray[TriangularFuzzyNumber]` (or a list of TFNs), the function returns a numpy array
of ICr values for the provided alpha.

```python
def ICr_alpha(vector: FuzzyNumberArray[TriangularFuzzyNumber], alpha: float = 0.5) -> np.ndarray:
	if alpha < 0.5:
		res = 2 * (vector.mid - vector.left) * alpha + vector.left
	else:
		res = 2 * (vector.right - vector.mid) * alpha + 2 * vector.mid - vector.right
	return res
```

This helper demonstrates how to combine the array's vectorized attributes (`left`, `mid`, `right`) with
numpy operations to get fast, element-wise results.

---

For the complete API and additional examples, see the API Reference and the `examples/` folder in the repository.
