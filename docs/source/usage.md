# Quick start

This short example shows how to create and use fuzzy numbers from `fuzzpy`.

```python
from fuzzpy.numbers.triangular import Triangular
from fuzzpy.numbers.trapezoidal import Trapezoidal

# create numbers
a = Triangular(1.0, 2.0, 3.0)
b = Trapezoidal(0.0, 1.0, 2.0, 4.0)

# basic operations (example)
print(a)
print(b)
```

For full API docs see the `API Reference <api.html>`_.
