"""
Global configuration for fuzzpy package.
"""

# Available addition methods (extend as needed)
fuzzy_addition_method = "default"  # e.g., "default", "extension_principle", "parametric", etc.


def set_fuzzy_addition_method(method: str):
    """Set the global fuzzy addition method."""
    global fuzzy_addition_method
    fuzzy_addition_method = method


def get_fuzzy_addition_method() -> str:
    """Get the current global fuzzy addition method."""
    return fuzzy_addition_method
