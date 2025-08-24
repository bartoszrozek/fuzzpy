from .trapezoidal import TrapezoidalFuzzyNumber
from .fuzzy_number import FuzzyNumber

class TriangularFuzzyNumber(TrapezoidalFuzzyNumber):
    """
    Triangular fuzzy number.

    A triangular fuzzy number is defined by three real parameters (a1, a2, a3)
    that determine a piecewise-linear membership function with a peak of 1 at a2.
    The membership function increases linearly from a1 to a2 and decreases
    linearly from a2 to a3.

    Parameters
    ----------
    a1 : float
        Left endpoint of the support (membership > 0).
    a2 : float
        Peak location where membership equals 1.
    a3 : float
        Right endpoint of the support (membership > 0).

    Attributes
    ----------
    a1, a2, a3 : float
        Parameters provided at construction. Internally a triangular number is
        represented as a trapezoidal fuzzy number with a collapsed plateau
        (i.e., the trapezoid core is the single point a2).

    Raises
    ------
    ValueError
        If not a1 <= a2 <= a3.
    """
    def __init__(self, a1: float, a2: float, a3: float):
        if not (a1 <= a2 <= a3):
            raise ValueError("Require a1 <= a2 <= a3 for TriangularFuzzyNumber")
        # For triangular, a2 == a3 for the core, a4 == a3 for support
        super().__init__(a1, a2, a2, a3)
    
    @property
    def left(self) -> float:
        """Return the left (lower) endpoint of the triangular fuzzy number.
        This is the smallest point in the support of the triangular membership function
        (where membership may become non-zero), corresponding to the internal attribute
        ``a1``.
        Returns:
            float: The left/support endpoint a1.
        """

        return self.a1

    @property
    def mid(self) -> float:
        """Return the peak (modal) point of the triangular fuzzy number.
        This is the point where the membership function reaches its maximum value of 1,
        corresponding to the internal attribute ``a2``.
        Returns:
            float: The peak/modal point a2."""
        return self.a2

    @property
    def right(self) -> float:
        """Return the right (upper) endpoint of the triangular fuzzy number.
        This is the largest point in the support of the triangular membership function
        (where membership may become non-zero), corresponding to the internal attribute
        ``a4`` (which equals ``a3`` in triangular numbers).
        Returns:
            float: The right/support endpoint a3."""
        return self.a4

    def _add_fuzzy(self, other: "FuzzyNumber | int | float") -> "TriangularFuzzyNumber":
        # if isinstance(other, TriangularFuzzyNumber):
        #     return TriangularFuzzyNumber(
        #         self.a1 + other.a1,
        #         self.a2 + other.a2,
        #         self.a4 + other.a4,
        #     )
        if isinstance(other, (int, float)):
            return TriangularFuzzyNumber(
                self.a1 + other,
                self.a2 + other,
                self.a4 + other,
            )
        else:
            return NotImplemented

    def _mul_fuzzy(self, other: "FuzzyNumber | int | float") -> "TriangularFuzzyNumber":
        if isinstance(other, TriangularFuzzyNumber):
            return TriangularFuzzyNumber(
                self.a1 * other.a1,
                self.a2 * other.a2,
                self.a4 * other.a4,
            )
        elif isinstance(other, (int, float)):
            return TriangularFuzzyNumber(
                self.a1 * other,
                self.a2 * other,
                self.a4 * other,
            )
        else:
            return NotImplemented

    def __repr__(self):
        return (
            f"TriangularFuzzyNumber(left={self.left}, mid={self.mid}, right={self.right})"
        )
