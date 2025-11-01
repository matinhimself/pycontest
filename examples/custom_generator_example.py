"""
Example demonstrating custom generator usage.

This example shows how to create a custom generator for specific requirements,
such as generating a sorted array with controlled duplicates.
"""

import random
from collections.abc import Generator

from pycontest import Case, CustomArray, IntVar


def sorted_array_generator(length: int, max_value: int) -> Generator[int]:
    """
    Generate a sorted array with some duplicate values.

    Args:
        length: Length of array to generate
        max_value: Maximum value in array
    """
    # Generate array
    arr = [random.randint(1, max_value) for _ in range(length)]
    arr.sort()

    # Yield each element
    for num in arr:
        yield num


class SortedArrayTest(Case):
    """Generate test cases with sorted arrays."""

    batch_size = 5

    n = IntVar(5, 20)
    max_val = IntVar(10, 100)
    arr = CustomArray(n, sorted_array_generator, n, max_val)

    def __inp_str__(self) -> str:
        """Format input as: n on first line, sorted array on second line."""
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def __otp_str__(self) -> str:
        """Format output to show if array is sorted."""
        return f"{'YES' if self.output else 'NO'}"

    def config(self) -> None:
        """Configure to check if array is sorted."""
        self.function = lambda arr: arr == sorted(arr)
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
