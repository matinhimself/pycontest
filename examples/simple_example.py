"""
Simple example demonstrating basic test case generation.

This example generates test cases for finding the maximum value in an array.
"""

from pycontest import Case, IntArray, IntVar
from pycontest.helper import list_printer


class MaxValueTest(Case):
    """Generate test cases for maximum value problem."""

    batch_size = 10  # Generate 10 test cases

    n = IntVar(1, 100)  # Array length between 1 and 100
    arr = IntArray(-1000, 1000, n)  # Array with values between -1000 and 1000

    def __inp_str__(self) -> str:
        """Format the input as: n on first line, array elements on second line."""
        return f"{self.n}\n{list_printer(self.arr, sep=' ')}"

    def config(self) -> None:
        """Configure to use max function as the solution."""
        self.function = max
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
