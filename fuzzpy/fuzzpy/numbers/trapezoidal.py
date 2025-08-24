from .fuzzy_number import FuzzyNumber
import numpy as np

class TrapezoidalFuzzyNumber(FuzzyNumber):
    """
    Trapezoidal fuzzy number.

    Represents a trapezoidal fuzzy number with a piecewise-linear membership
    function defined by four real parameters.

    Parameters
    ----------
    a1, a2, a3, a4 : float
        Parameters defining the trapezoid:
        a1 : left endpoint of support (membership > 0)
        a2 : left endpoint of core (membership = 1)
        a3 : right endpoint of core (membership = 1)
        a4 : right endpoint of support (membership > 0)

    Notes
    -----
    The membership function μ(x) is defined as:
      - μ(x) = 0 for x <= a1 or x >= a4
      - μ(x) increases linearly from 0 to 1 on [a1, a2]
      - μ(x) = 1 on [a2, a3]
      - μ(x) decreases linearly from 1 to 0 on [a3, a4]

    The left and right slopes are linear and the core [a2, a3] is flat (membership = 1).
    """
    def __init__(self, a1: float, a2: float, a3: float, a4: float):
        # Define left and right as linear functions
        def left_fun(alpha: np.ndarray) -> np.ndarray:
            # Linear increasing from 0 to 1
            return alpha
        def right_fun(alpha: np.ndarray) -> np.ndarray:
            # Linear decreasing from 1 to 0
            return 1 - alpha
        super().__init__(a1, a2, a3, a4, left_fun=left_fun, right_fun=right_fun)

    def _add_fuzzy(self, other: "FuzzyNumber | int | float") -> "TrapezoidalFuzzyNumber":
        # if isinstance(other, TrapezoidalFuzzyNumber):
        #     # Add corresponding parameters
        #     return TrapezoidalFuzzyNumber(
        #         self.a1 + other.a1,
        #         self.a2 + other.a2,
        #         self.a3 + other.a3,
        #         self.a4 + other.a4,
        #     )
        if isinstance(other, (int, float)):
            # Add other to each parameter
            return TrapezoidalFuzzyNumber(
                self.a1 + other,
                self.a2 + other,
                self.a3 + other,
                self.a4 + other,
            )
        else:
            return NotImplemented

    def _mul_fuzzy(self, other: "FuzzyNumber | int | float") -> "TrapezoidalFuzzyNumber":
        if isinstance(other, TrapezoidalFuzzyNumber):
            # Multiply corresponding parameters (not always mathematically correct, but common for positive fuzzy numbers)
            return TrapezoidalFuzzyNumber(
                self.a1 * other.a1,
                self.a2 * other.a2,
                self.a3 * other.a3,
                self.a4 * other.a4,
            )
        elif isinstance(other, (int, float)):
            # Multiply each parameter by other
            return TrapezoidalFuzzyNumber(
                self.a1 * other,
                self.a2 * other,
                self.a3 * other,
                self.a4 * other,
            )
        else:
            return NotImplemented

    def __repr__(self):
        return (
            f"TrapezoidalFuzzyNumber(a1={self.a1}, a2={self.a2}, a3={self.a3}, a4={self.a4})"
        )
