"""
pycontest - Test case generator for competitive programming.

A modern Python library for generating test cases for online judges and
competitive programming problems.
"""

from .case import Case
from .generator import (
    Array2d,
    CharArray,
    ChoiceList,
    Collections,
    CustomArray,
    FloatArray,
    FloatVar,
    IntArray,
    IntVar,
    Variables,
)
from .helper import OutputHelper

__version__ = "2.0.0"
__all__ = [
    "Case",
    "IntVar",
    "FloatVar",
    "IntArray",
    "FloatArray",
    "CharArray",
    "ChoiceList",
    "CustomArray",
    "Array2d",
    "Collections",
    "Variables",
    "OutputHelper",
]
