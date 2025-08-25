from typing import TypeVar, Generic, Sequence, Iterator, Union, Optional, Any, cast
from ..numbers import FuzzyNumber, TriangularFuzzyNumber, TrapezoidalFuzzyNumber
from plotnine import ggplot, aes, geom_line, labs, theme_minimal
import pandas as pd
import numpy as np
from functools import reduce

T = TypeVar("T", bound=FuzzyNumber)

class FuzzyNumberArray(Generic[T]):
    """
    Container for a fixed-size sequence of fuzzy numbers of the same (or compatible) type.

    This class wraps a list of FuzzyNumber instances and provides:
    - Sequence protocols: len, iter, indexing, slicing and fancy indexing (list of ints).
    - Element-wise arithmetic (+, *) with scalars, fuzzy numbers or another FuzzyNumberArray.
    - Vectorized access to attributes of contained fuzzy numbers via attribute lookup
      (e.g. arr.a1 returns a numpy array of a1 values).
    - Convenience plotting of membership functions using plotnine (plot method).
    - Random factory constructors for triangular and trapezoidal fuzzy numbers.

    Important behaviors and invariants
    - The constructor requires a non-empty sequence. If the provided elements are not
      all the same concrete type, the most specific common base class (by MRO) is used
      as the array's declared element type.
    - Setting items enforces that assigned elements are instances of the array's element
      type.
    - Arithmetic operations return a new FuzzyNumberArray; operations with another
      FuzzyNumberArray require equal lengths.

    Attributes
    ----------
    _data : list[FuzzyNumber]
        Underlying storage of fuzzy number instances.
    _type : type
        Declared element type (most specific common base for the provided elements).

    Examples
    --------
    >>> from fuzzpy.numbers import TriangularFuzzyNumber
    >>> a = FuzzyNumberArray([TriangularFuzzyNumber(0, 1, 2), TriangularFuzzyNumber(1, 2, 3)])
    >>> len(a)
    2
    >>> a[0] + 1.0
    <TriangularFuzzyNumber ...>
    >>> a.a2  # returns numpy array of the a2 (center) values
    array([1., 2.])
    """
    def __init__(self, data: Sequence[FuzzyNumber]):
        if not data:
            raise ValueError("FuzzyNumberArray cannot be empty")
        types = {type(fz) for fz in data}
        if len(types) == 1:
            self._type = types.pop()
        else:
            # Find the most specific common superclass among the types
            self._type = reduce(self.common_base, types)
        # store as a list[T] for precise typing; cast is safe if caller used correct element types
        self._data: list[T] = cast(list[T], list(data))

    def __getitem__(self, idx: int | slice | list[int]) -> "T | FuzzyNumberArray[T]":
        cls = type(self)
        if isinstance(idx, slice):
            return cls(self._data[idx])
        elif isinstance(idx, list):
            return cls([self._data[i] for i in idx])
        else:
            return self._data[idx]

    def __setitem__(self, idx: int, value: T):
        if not isinstance(value, self._type):
            raise TypeError(f"All elements must be of type {self._type}")
        self._data[idx] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        type_name = self._type.__name__ if hasattr(self, "_type") else "Unknown"
        return (
            f"FuzzyNumberArray(type_={type_name}, size={len(self)}, data={self._data!r})"
        )

    def __str__(self) -> str:
        type_name = self._type.__name__ if hasattr(self, "_type") else "Unknown"
        preview = ", ".join(str(fz) for fz in self._data[:5])
        if len(self) > 5:
            preview += ", ..."
        return (
            f"FuzzyNumberArray(type_={type_name}, size={len(self)}, data=[{preview}])"
        )

    def __add__(self, other: Union['FuzzyNumberArray[T]', int, float, FuzzyNumber]) -> 'FuzzyNumberArray[T]':
        if isinstance(other, FuzzyNumberArray):
            if len(self) != len(other):
                raise ValueError("Arrays must be of the same length")
            return FuzzyNumberArray([cast(T, a + b) for a, b in zip(self._data, other._data)])
        return FuzzyNumberArray([cast(T, a + other) for a in self._data])

    def __radd__(self, other: Union[int, float, FuzzyNumber]) -> 'FuzzyNumberArray[T]':
        return self.__add__(other)

    def __mul__(self, other: Union['FuzzyNumberArray[T]', int, float, FuzzyNumber]) -> 'FuzzyNumberArray[T]':
        if isinstance(other, FuzzyNumberArray):
            if len(self) != len(other):
                raise ValueError("Arrays must be of the same length")
            return FuzzyNumberArray([cast(T, a * b) for a, b in zip(self._data, other._data)])
        return FuzzyNumberArray([cast(T, a * other) for a in self._data])

    def tolist(self) -> list[T]:
        return list(self._data)

    def plot(
        self,
        n_points: int = 200,
        title: str = "Fuzzy Number Array Membership Functions",
        labels: Optional[list[str]] = None,
        show_legend: bool = False,
        **kwargs: Any
    ) -> ggplot:
        """
        Plot the membership functions of all fuzzy numbers in the array using plotnine.
        If all numbers are TriangularFuzzyNumber, only 3 points per number are used for efficiency.
        If all numbers are TrapezoidalFuzzyNumber, only 4 points per number are used for efficiency.
        Parameters
        ----------
        n_points : int
            Number of points to sample for each fuzzy number (ignored for triangular/trapezoidal).
        title : str
            Title for the plot.
        labels : list or None
            Optional list of labels for each fuzzy number. If None, indices are used.
        kwargs : dict
            Additional keyword arguments passed to plotnine's geom_line.
        Returns
        -------
        plotnine.ggplot
            The plotnine plot object.
        """
        n = len(self)
        if labels is None:
            labels = [str(i) for i in range(n)]
        if len(labels) != n:
            raise ValueError("labels must be the same length as the array")
        dfs: list[pd.DataFrame] = []
        if all(isinstance(fz, TriangularFuzzyNumber) for fz in self._data):
            for fz, label in zip(self._data, labels):
                xs = [fz.a1, fz.a2, fz.a4]
                ys = [0.0, 1.0, 0.0]
                df = pd.DataFrame({'x': xs, 'membership': ys, 'label': label})
                dfs.append(df)
        elif all(isinstance(fz, TrapezoidalFuzzyNumber) for fz in self._data):
            for fz, label in zip(self._data, labels):
                xs = [fz.a1, fz.a2, fz.a3, fz.a4]
                ys = [0.0, 1.0, 1.0, 0.0]
                df = pd.DataFrame({'x': xs, 'membership': ys, 'label': label})
                dfs.append(df)
        else:
            for fz, label in zip(self._data, labels):
                xs = np.linspace(fz.a1, fz.a4, n_points)
                ys = np.array([fz.membership(x) for x in xs])
                df = pd.DataFrame({'x': xs, 'membership': ys, 'label': label})
                dfs.append(df)
        df_all = pd.concat(dfs, ignore_index=True)
        p: ggplot = (
            ggplot(df_all, aes(x='x', y='membership', color='label'))
            + geom_line(**kwargs, show_legend=show_legend)
            + labs(title=title, x="x", y="Membership", color="Fuzzy Number")
            + theme_minimal()
        )

        return p

    def __getattr__(self, attr: str) -> Any:
        """
        Allow access to numpy arrays of attributes from contained fuzzy numbers.
        E.g., vector.left returns np.array([x.left for x in vector]) if 'left' is an attribute of the elements.
        """
        if hasattr(self._data[0], attr):
            return np.array([getattr(x, attr) for x in self._data])
        raise AttributeError(f"'{type(self).__name__}' object and its elements have no attribute '{attr}'")
    
    @staticmethod
    def common_base(t1: type, t2: type) -> type:
        return next(base for base in t1.mro() if base in t2.mro())

    @classmethod
    def random_triangular(
        cls,
        n: int,
        c_mu: float,
        c_sigma: float,
        l1: float,
        l2: float,
        r1: float,
        r2: float,
        random_state: Optional[int] = None
    ) -> "FuzzyNumberArray[TriangularFuzzyNumber]":
        """
        Generate a FuzzyNumberArray of n TriangularFuzzyNumber objects.
        c ~ N(c_mu, c_sigma), l ~ U(l1, l2), r ~ U(r1, r2).
        Ensures a1 < a2 < a4 for each number.
        """
        rng = np.random.default_rng(random_state)
        centers = rng.normal(c_mu, c_sigma, n)
        lefts = rng.uniform(l1, l2, n)
        rights = rng.uniform(r1, r2, n)
        arr: list[TriangularFuzzyNumber] = []
        for center, left, right in zip(centers, lefts, rights):
            a1 = center - abs(left)
            a2 = center
            a4 = center + abs(right)
            if a1 < a2 < a4:
                arr.append(TriangularFuzzyNumber(a1, a2, a4))
        return FuzzyNumberArray(arr)

    @classmethod
    def random_trapezoidal(
        cls,
        n: int,
        c_mu: float,
        c_sigma: float,
        l1: float,
        l2: float,
        r1: float,
        r2: float,
        w1: float,
        w2: float,
        random_state: Optional[int] = None
    ) -> "FuzzyNumberArray[TrapezoidalFuzzyNumber]":
        """
        Generate a FuzzyNumberArray of n TrapezoidalFuzzyNumber objects.
        c ~ N(c_mu, c_sigma), l ~ U(l1, l2), r ~ U(r1, r2), w ~ U(w1, w2).
        Ensures a1 < a2 <= a3 < a4 for each number.
        """
        rng = np.random.default_rng(random_state)
        centers = rng.normal(c_mu, c_sigma, n)
        lefts = rng.uniform(l1, l2, n)
        rights = rng.uniform(r1, r2, n)
        widths = rng.uniform(w1, w2, n)
        arr: list[TrapezoidalFuzzyNumber] = []
        for center, left, right, width in zip(centers, lefts, rights, widths):
            a2 = center - abs(width) / 2
            a3 = center + abs(width) / 2
            a1 = a2 - abs(left)
            a4 = a3 + abs(right)
            if a1 < a2 <= a3 < a4:
                arr.append(TrapezoidalFuzzyNumber(a1, a2, a3, a4))
        return FuzzyNumberArray(arr)
