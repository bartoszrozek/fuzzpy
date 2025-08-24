# FuzzyPy

A Python package for fuzzy numbers. This project uses [UV](https://github.com/astral-sh/uv) for dependency management and benchmarking.

## Project Structure
- `src/` — Package source code
- `tests/` — Unit and integration tests
- `benchmarks/` — Benchmark scripts
- `docs/` — Documentation
- `examples/` — Usage examples

## Setup
1. Install [UV](https://github.com/astral-sh/uv):
   ```bash
   pip install uv
   ```
2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running Tests
```bash
uv pip install -r requirements-dev.txt
uv pytest
```

## Running Benchmarks
```bash
uv pip install -r requirements-bench.txt
python benchmarks/bench_*.py
```
