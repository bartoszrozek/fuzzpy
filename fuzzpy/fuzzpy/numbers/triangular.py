from .trapezoidal import TrapezoidalFuzzyNumber
from .fuzzy_number import FuzzyNumber

class TriangularFuzzyNumber(TrapezoidalFuzzyNumber):
    """
    Represents a standard triangular fuzzy number with a piecewise linear membership function.
    The membership function is defined by three real parameters (a1, a2, a3):
        - a1: left endpoint of support (membership > 0)
        - a2: peak (membership = 1)
        - a3: right endpoint of support (membership > 0)
    The left and right slopes are linear, and the peak is at a2.
    """
    def __init__(self, a1: float, a2: float, a3: float):
        if not (a1 <= a2 <= a3):
            raise ValueError("Require a1 <= a2 <= a3 for TriangularFuzzyNumber")
        # For triangular, a2 == a3 for the core, a4 == a3 for support
        super().__init__(a1, a2, a2, a3)
    
    @property
    def left(self) -> float:
        return self.a1

    @property
    def mid(self) -> float:
        return self.a2

    @property
    def right(self) -> float:
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
