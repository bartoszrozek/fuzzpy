import warnings
from abc import ABC
from typing import Any, Callable, Optional, Tuple

import numpy as np
import pandas as pd
from plotnine import aes, geom_line, ggplot, labs, theme_minimal

from fuzzpy.config import get_fuzzy_addition_method

NumericFunction = Callable[[np.ndarray[Any, Any]], np.ndarray[Any, Any]]


class FuzzyNumber(ABC):
    """
    Abstract base class representing a generalized fuzzy number with customizable membership functions.
    A fuzzy number is defined by four real parameters (a1, a2, a3, a4) that specify its support and core,
    and by optional vectorized functions that describe the shape of its membership function on the left,
    right, lower, and upper sides.

    Parameters
    ----------
    a1 : float
        The left endpoint of the support (where membership becomes nonzero).
    a2 : float
        The left endpoint of the core (where membership reaches 1).
    a3 : float
        The right endpoint of the core (where membership leaves 1).
    a4 : float
        The right endpoint of the support (where membership returns to zero).
    lower : Optional[NumericFunction], default=None
        A vectorized function mapping [0, 1] to [0, 1], describing the lower boundary of the fuzzy number.
    upper : Optional[NumericFunction], default=None
        A vectorized function mapping [0, 1] to [0, 1], describing the upper boundary of the fuzzy number.
    left : Optional[NumericFunction], default=None
        A vectorized function mapping [0, 1] to [0, 1], describing the left slope of the membership function.
    right : Optional[NumericFunction], default=None
        A vectorized function mapping [0, 1] to [0, 1], describing the right slope of the membership function.
    Methods
    -------
    membership(x: float) -> float
        Computes the membership degree of a given value x according to the fuzzy number's membership function.
    support() -> Tuple[float, float]
        Returns the support interval (a1, a4) of the fuzzy number.
    __add__(other: FuzzyNumber) -> FuzzyNumber
        Returns the fuzzy sum of this fuzzy number and another.
    __mul__(other: FuzzyNumber) -> FuzzyNumber
        Returns the fuzzy product of this fuzzy number and another.
    Abstract Methods
    ----------------
    _add_fuzzy(other: FuzzyNumber) -> FuzzyNumber
        Abstract method for fuzzy addition; must be implemented by subclasses.
    _mul_fuzzy(other: FuzzyNumber) -> FuzzyNumber
        Abstract method for fuzzy multiplication; must be implemented by subclasses.
    Notes
    -----
    - The class validates that the parameters are finite real numbers and that the order a1 <= a2 <= a3 <= a4 holds.
    - The left and right functions must be properly vectorized and monotonic (increasing for left, decreasing for right).
    - The lower and upper functions must be properly vectorized and monotonic (increasing for lower, decreasing for upper).
    - If not provided, default functions return NaN for all inputs.
    Raises
    ------
    ValueError
        If parameters are not valid, or if the provided functions do not meet the required properties.
    """

    def __init__(
        self,
        a1: int | float,
        a2: int | float,
        a3: int | float,
        a4: int | float,
        lower: Optional[NumericFunction] = None,
        upper: Optional[NumericFunction] = None,
        left_fun: Optional[NumericFunction] = None,
        right_fun: Optional[NumericFunction] = None,
    ):
        self.a1 = float(a1)
        self.a2 = float(a2)
        self.a3 = float(a3)
        self.a4 = float(a4)
        default_function: NumericFunction = lambda x: np.full_like(x, np.nan, dtype=float)
        self.lower: NumericFunction = (
            lower
            if lower is not None
            else default_function
        )
        self.upper: NumericFunction = (
            upper
            if upper is not None
            else default_function
        )
        self.left_fun: NumericFunction = (
            left_fun if left_fun is not None else default_function
        )
        self.right_fun: NumericFunction = (
            right_fun
            if right_fun is not None
            else default_function
        )
        self._validate()

    def membership(self, x: float) -> float:
        # Generalized membership function using left/right and core/support
        if x < self.a1 or x > self.a4:
            return 0.0
        elif self.a2 <= x <= self.a3:
            return 1.0
        elif self.a1 <= x < self.a2:
            # Use left_fun if available
            alpha = (x - self.a1) / (self.a2 - self.a1) if self.a2 != self.a1 else 0.0
            return float(self.left_fun(np.array([alpha]))[0])
        elif self.a3 < x <= self.a4:
            # Use right_fun if available
            alpha = (x - self.a3) / (self.a4 - self.a3) if self.a4 != self.a3 else 0.0
            return float(self.right_fun(np.array([alpha]))[0])
        return 0.0
    
    def support(self) -> Tuple[float, float]:
        return (self.a1, self.a4)

    def __add__(self, other: "FuzzyNumber | int | float") -> "FuzzyNumber":
        return self._add_fuzzy(other)

    def __mul__(self, other: "FuzzyNumber | int | float") -> "FuzzyNumber":
        return self._mul_fuzzy(other)


    def _validate(self):
        # Check a1, a2, a3, a4 are single finite real numbers
        for val in [self.a1, self.a2, self.a3, self.a4]:
            if not (isinstance(val, float) and np.isfinite(val)):
                raise ValueError(
                    "Each of a1, a2, a3, a4 should be a single finite real number"
                )
        # Check order
        if any(np.diff([self.a1, self.a2, self.a3, self.a4]) < 0):
            raise ValueError("Please provide a1 <= a2 <= a3 <= a4")
        # Check lower, upper, left, right functions
        self._check_function(self.lower, increasing=True, name="lower")
        self._check_function(self.upper, increasing=False, name="upper")
        self._check_function(self.left_fun, increasing=True, name="left_fun")
        self._check_function(self.right_fun, increasing=False, name="right_fun")
        # NA consistency
        left01 = self.left_fun(np.array([0.0, 1.0]))
        right01 = self.right_fun(np.array([0.0, 1.0]))
        lower01 = self.lower(np.array([0.0, 1.0]))
        upper01 = self.upper(np.array([0.0, 1.0]))
        if np.isnan(left01[0]) != np.isnan(right01[0]):
            raise ValueError("Either all or none of left_fun and right_fun should return NA")
        if np.isnan(lower01[0]) != np.isnan(upper01[0]):
            raise ValueError("Either all or none of lower and upper should return NA")

    def _check_function(self, func: Callable[[Any], Any], increasing: bool, name: str):
        vals = func(np.array([0.0, 1.0]))
        if not (hasattr(vals, "shape") and vals.shape == (2,)):
            raise ValueError(
                f"{name} is not properly vectorized or doesn't give numeric results"
            )
        if not np.isnan(vals[0]):
            if increasing:
                if vals[0] < 0 or vals[1] > 1 or vals[0] > vals[1]:
                    raise ValueError(
                        f"{name} should be an increasing function [0,1]->[0,1]"
                    )
            else:
                if vals[1] < 0 or vals[0] > 1 or vals[1] > vals[0]:
                    raise ValueError(
                        f"{name} should be a decreasing function [0,1]->[1,0]"
                    )

    def __repr__(self):
        return (
            f"FuzzyNumber(a1={self.a1}, a2={self.a2}, a3={self.a3}, a4={self.a4}, "
            f"lower={self.lower}, upper={self.upper}, left_fun={self.left_fun}, right_fun={self.right_fun})"
        )

    def _add_fuzzy(self, other: "FuzzyNumber | int | float") -> "FuzzyNumber":
        if isinstance(other, FuzzyNumber):
            method = get_fuzzy_addition_method()
            if method == "default":
                raise NotImplementedError("Addition with another FuzzyNumber must be implemented in a subclass.")
            elif method == "extension_principle":
                # Placeholder for extension principle method
                raise NotImplementedError("Extension principle addition not implemented yet.")
            elif method == "parametric":
                # Placeholder for parametric method
                raise NotImplementedError("Parametric addition not implemented yet.")
            else:
                raise ValueError(f"Unknown fuzzy addition method: {method}")
        elif isinstance(other, (int, float)):
            # Shift all parameters by the numeric value
            return self.__class__(
                self.a1 + other,
                self.a2 + other,
                self.a3 + other,
                self.a4 + other,
                lower=self.lower,
                upper=self.upper,
                left_fun=self.left_fun,
                right_fun=self.right_fun,
            )
        else:
            return NotImplemented

    def _mul_fuzzy(self, other: "FuzzyNumber | int | float") -> "FuzzyNumber":
        if isinstance(other, FuzzyNumber):
            raise NotImplementedError("Multiplication with another FuzzyNumber must be implemented in a subclass.")
        elif isinstance(other, (int, float)):
            # Scale all parameters by the numeric value
            return self.__class__(
                self.a1 * other,
                self.a2 * other,
                self.a3 * other,
                self.a4 * other,
                lower=self.lower,
                upper=self.upper,
                left_fun=self.left_fun,
                right_fun=self.right_fun,
            )
        else:
            return NotImplemented
        
    def __radd__(self, other:  "FuzzyNumber") -> "FuzzyNumber":
        warnings.warn("Upper casting to FuzzyNumber may lead to unexpected results.")
        return self.__add__(other)

    def __rmul__(self, other: "FuzzyNumber") -> "FuzzyNumber":
        return self.__mul__(other)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FuzzyNumber):
            return False
        return (
            np.allclose([self.a1, self.a2, self.a3, self.a4], [other.a1, other.a2, other.a3, other.a4])
            # Optionally, could compare functions as well
        )

    def __hash__(self):
        # Hash only the numeric parameters for now
        return hash((self.a1, self.a2, self.a3, self.a4))
    
    def plot(self, n_points: int = 200, title: str = "Fuzzy Number Membership Function", **kwargs) -> ggplot:
        """
        Plot the membership function of the fuzzy number using plotnine.

        Parameters
        ----------
        n_points : int
            Number of points to sample for the plot.
        title : str
            Title for the plot.
        kwargs : dict
            Additional keyword arguments passed to plotnine's geom_line.
        Returns
        -------
        plotnine.ggplot
            The plotnine plot object.
        """

        xs = np.linspace(self.a1, self.a4, n_points)
        ys = np.array([self.membership(x) for x in xs])
        df = pd.DataFrame({'x': xs, 'membership': ys})

        p: ggplot = (
            ggplot(df, aes(x='x', y='membership'))
            + geom_line(**kwargs)
            + labs(
                title=title,
                x="x",
                y="Membership"
            )
            + theme_minimal()
        )
        return p
