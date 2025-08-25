# FuzzyPy

FuzzyPy is a Python library for creating, manipulating and visualizing fuzzy numbers
(triangular, trapezoidal and general fuzzy numbers). It provides convenience types and
vectorized operations to make numerical and statistical workflows with fuzzy data ergonomic.

Documentation is available at [github pages](https://bartoszrozek.github.io/fuzzpy/).

This repository includes:
- `fuzzpy/` — package source (numbers, container structs and config)
- `docs/` — Sphinx documentation source and built output
- `examples/` — short runnable examples and notebooks (see `test.ipynb` for an interactive demo)
- `tests/` — unit tests

Highlights
- `fuzzpy.numbers` — core fuzzy number classes:
   - `TriangularFuzzyNumber` — left/center/right triangular TFNs
   - `TrapezoidalFuzzyNumber` — four-parameter trapezoidal numbers
   - `FuzzyNumber` — more general base with customizable membership helpers
- `fuzzpy.structs.FuzzyNumberArray` — fixed-size, typed container for arrays of fuzzy numbers with
   vectorized attributes (e.g. `.left`, `.mid`, `.right`), sequence semantics and plotting support
- `fuzzpy.config` — runtime configuration for e.g. fuzzy addition semantics

Quick install (developer workflow)

1. Install UV (recommended for reproducible envs used in this project):

```bash
pip install uv
```

2. Install project dependencies (dev/test/bench as needed):

```bash
uv pip install -r requirements.txt          # runtime deps
uv pip install -r requirements-dev.txt      # developer/test deps
uv pip install -r requirements-bench.txt    # benchmark deps
```

Running tests

```bash
uv pip install -r requirements-dev.txt
uv pytest
```

Running benchmarks

```bash
uv pip install -r requirements-bench.txt
python benchmarks/bench_*.py
```

Quick examples

```python
import numpy as np
from fuzzpy.numbers import TriangularFuzzyNumber, TrapezoidalFuzzyNumber
from fuzzpy.structs import FuzzyNumberArray

# create numbers
a = TriangularFuzzyNumber(0, 1, 2)
b = TrapezoidalFuzzyNumber(0, 1, 2, 3)

# arrays
arr = FuzzyNumberArray([a, b])
print(arr.mid)   # numpy array of centers

# plotting (uses plotnine)
arr.plot()
```

License

This repository includes a package copyright and license (check `PKG-INFO` or `LICENSE`).

---
