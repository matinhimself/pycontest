"""
Example demonstrating multiple test case types.

This example shows how to generate different categories of test cases
(small, medium, large) in a single run.
"""

from pycontest import Case, IntArray, IntVar


class SmallTests(Case):
    """Generate small test cases (n ≤ 100)."""

    batch_size = 5

    n = IntVar(1, 100)
    arr = IntArray(0, 1000, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = sum
        self.input_sequence = [self.arr]


class MediumTests(Case):
    """Generate medium test cases (100 < n ≤ 1000)."""

    batch_size = 3

    n = IntVar(101, 1000)
    arr = IntArray(0, 10**6, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = sum
        self.input_sequence = [self.arr]


class LargeTests(Case):
    """Generate large test cases (n > 1000)."""

    batch_size = 2

    n = IntVar(1001, 10000)
    arr = IntArray(0, 10**9, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = sum
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
    print("\nGenerated 5 small + 3 medium + 2 large = 10 total test cases")
