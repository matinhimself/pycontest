# pycontest

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An easy-to-use test case generator for competitive programming and online judges. Generate comprehensive test cases with random data that follows your constraints.

## Features

- 🎲 Random variable generation (integers, floats, arrays, 2D arrays)
- 📝 Customizable input/output formatting
- 🔧 Support for custom generators
- 📁 Automatic test file organization
- 🐍 Python 3.10+
- 🚀 Zero dependencies

## Installation

```bash
pip install pycontest
```

## Quick Start

```python
from pycontest import Case, IntVar, IntArray
from pycontest.helper import list_printer


class TestCase(Case):
    batch_size = 10  # Generate 10 test cases

    n = IntVar(1, 100)  # Random integer between 1 and 100
    arr = IntArray(-1000, 1000, n)  # Array of n random integers

    def __inp_str__(self) -> str:
        """Define how inputs will be formatted."""
        return f"{self.n}\n{list_printer(self.arr, sep=' ')}"

    def config(self) -> None:
        """Configure the test case generator."""
        self.function = min
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
```

This will generate test files in the following structure:

```
tests/
├── in/
│   ├── input1.txt
│   ├── input2.txt
│   └── ...
└── out/
    ├── output1.txt
    ├── output2.txt
    └── ...
``` 

## Available Types

| Type | Description | Example |
|------|-------------|---------|
| `IntVar(a, b)` | Random integer N where a ≤ N ≤ b | `IntVar(1, 100)` |
| `FloatVar(a, b)` | Random float N where a ≤ N ≤ b | `FloatVar(1.5, 20.0)` |
| `IntArray(a, b, length)` | Array of random integers | `IntArray(0, 100, 10)` |
| `FloatArray(a, b, length)` | Array of random floats | `FloatArray(0.0, 10.0, 5)` |
| `ChoiceList(length, choices)` | Array of random choices | `ChoiceList(10, string.ascii_letters)` |
| `CharArray(length)` | Array of random characters | `CharArray(10)` |
| `CustomArray(length, gen, *args)` | Array using custom generator | See [Custom Generators](#custom-generators) |
| `Array2d(array, length)` | 2D array | `Array2d(IntArray(0, 10, 5), 3)` |

**Note**: Variables can be nested! Use `IntVar` as bounds for other variables:

```python
n = IntVar(1, 100)
arr = IntArray(0, 1000, n)  # Array length depends on n
```

## Advanced Usage

### Using a Python Script as Solver

Instead of a function, you can use a Python script to generate outputs:

```python
from pycontest import Case, IntArray, IntVar
from pycontest.helper import list_printer


class TestCase(Case):
    batch_size = 5

    n = IntVar(1, 10)
    arr = IntArray(0, 100, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{list_printer(self.arr, sep=' ')}"

    def config(self) -> None:
        self.app = "./solver.py"  # Your solution script


if __name__ == "__main__":
    Case.main()
```

The script will receive input via stdin and output should be printed to stdout. See [example_app.py](https://github.com/matinhimself/pycontest/blob/main/examples/example_app.py) for details.

### Custom Input/Output Formatting

Override `__inp_str__()` and `__otp_str__()` to customize formatting:

```python
class TestCase(Case):
    n = IntVar(1, 10)
    m = IntVar(1, 10)
    matrix = Array2d(IntArray(0, 100, m), n)

    def __inp_str__(self) -> str:
        """Custom input format."""
        from pycontest.helper import list2d_printer
        return f"{self.n} {self.m}\n{list2d_printer(self.matrix)}"

    def __otp_str__(self) -> str:
        """Custom output format."""
        return f"Result: {self.output}"

    def config(self) -> None:
        self.function = sum_matrix
        self.input_sequence = [self.matrix]
```

### Custom Output Writers

By default, test cases are written to separate files. You can customize this:

```python
import sys
from pycontest.helper import OutputHelper


class TestCase(Case):
    def config(self) -> None:
        # Write to stdout instead
        self.writer = sys.stdout

        # Or customize directory structure
        # self.writer = OutputHelper(
        #     in_prefix="test",
        #     out_prefix="answer",
        #     input_directory="inputs",
        #     output_directory="outputs",
        #     test_directory="testcases"
        # )
```

### Multiple Test Case Types

Generate different types of test cases by creating multiple classes:

```python
from pycontest import Case, IntVar, IntArray


class SmallTests(Case):
    batch_size = 5
    n = IntVar(1, 10)
    arr = IntArray(0, 100, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = max
        self.input_sequence = [self.arr]


class LargeTests(Case):
    batch_size = 3
    n = IntVar(1000, 10000)
    arr = IntArray(0, 10**9, n)

    def __inp_str__(self) -> str:
        return f"{self.n}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = max
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
```

### Custom Generators

Create custom generators for complex test case requirements:

```python
import random
from collections.abc import Generator
from pycontest import Case, IntVar, CustomArray


def sparse_array_generator(max_zeros: int) -> Generator[int]:
    """Generate array with at most max_zeros zero values."""
    zeros_used = 0
    while True:
        x = random.randint(0, 1000)
        if x == 0 and zeros_used < max_zeros:
            zeros_used += 1
            yield 0
        elif x != 0:
            yield x
        else:
            yield random.randint(1, 1000)


class TestCase(Case):
    batch_size = 10
    max_zeros = IntVar(0, 5)
    arr = CustomArray(100, sparse_array_generator, max_zeros)

    def __inp_str__(self) -> str:
        return f"{len(self.arr)}\n{' '.join(map(str, self.arr))}"

    def config(self) -> None:
        self.function = lambda arr: arr.count(0)
        self.input_sequence = [self.arr]


if __name__ == "__main__":
    Case.main()
```

### 2D Arrays

Generate 2D arrays (matrices) easily:

```python
from pycontest import Case, IntVar, IntArray, Array2d
from pycontest.helper import list2d_printer


class TestCase(Case):
    batch_size = 5

    n = IntVar(3, 10)  # rows
    m = IntVar(3, 10)  # columns
    matrix = Array2d(IntArray(0, 100, m), n)

    def __inp_str__(self) -> str:
        return f"{self.n} {self.m}\n{list2d_printer(self.matrix)}"

    def config(self) -> None:
        self.function = lambda mat: sum(sum(row) for row in mat)
        self.input_sequence = [self.matrix]


if __name__ == "__main__":
    Case.main()
```

## Helper Functions

The `pycontest.helper` module provides formatting utilities that work with any iterable:

```python
from pycontest.helper import list_printer, list2d_printer, string_printer

# Format any iterable with custom separator
list_printer([1, 2, 3], sep=" ")        # "1 2 3"
list_printer(range(5), sep=", ")        # "0, 1, 2, 3, 4"
list_printer((10, 20, 30), sep="-")     # "10-20-30"

# Format 2D iterables (matrices)
matrix = [[1, 2], [3, 4]]
list2d_printer(matrix, sep="\n", inner_sep=" ")
# Output:
# 1 2
# 3 4

# Concatenate elements without separator
string_printer(['a', 'b', 'c'])  # "abc"
string_printer("hello")          # "hello"
string_printer([1, 2, 3])        # "123"
```

## Examples

Check out the [examples directory](https://github.com/matinhimself/pycontest/tree/main/examples) for more:

- [complete_usage.py](https://github.com/matinhimself/pycontest/blob/main/examples/complete_usage.py) - Comprehensive example showing all features
- [example_function.py](https://github.com/matinhimself/pycontest/blob/main/examples/example_function.py) - Using functions for output generation
- [example_app.py](https://github.com/matinhimself/pycontest/blob/main/examples/example_app.py) - Using Python scripts as solvers

## Requirements

- Python 3.10 or higher
- No external dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

