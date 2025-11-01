"""
Example demonstrating 2D array (matrix) test case generation.

This example generates test cases for matrix sum calculation.
"""

from pycontest import Array2d, Case, IntArray, IntVar
from pycontest.helper import list2d_printer


def matrix_sum(matrix: list[list[int]]) -> int:
    """Calculate the sum of all elements in a matrix."""
    return sum(sum(row) for row in matrix)


class MatrixSumTest(Case):
    """Generate test cases for matrix sum problem."""

    batch_size = 5

    rows = IntVar(2, 10)
    cols = IntVar(2, 10)
    matrix = Array2d(IntArray(0, 100, cols), rows)

    def __inp_str__(self) -> str:
        """Format input as: rows cols on first line, then matrix rows."""
        return f"{self.rows} {self.cols}\n{list2d_printer(self.matrix)}"

    def config(self) -> None:
        """Configure to use matrix_sum function as the solution."""
        self.function = matrix_sum
        self.input_sequence = [self.matrix]


if __name__ == "__main__":
    Case.main()
