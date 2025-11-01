"""
Helper utilities for formatting test case output.

This module provides functions and classes for formatting arrays,
matrices, and managing test file output.
"""

from collections.abc import Iterable
from pathlib import Path
from typing import Any

endl = "\n"


def list_printer(lst: Iterable[Any], sep: str = "\n", end: str = "") -> str:
    """
    Format an iterable as a string with custom separator.

    Args:
        lst: Iterable to format (list, tuple, array, etc.)
        sep: Separator between elements (default: newline)
        end: String to append at the end (default: empty)

    Returns:
        Formatted string representation of the iterable

    Examples:
        >>> list_printer([1, 2, 3], sep=" ")
        '1 2 3'
        >>> list_printer(range(3), sep=", ")
        '0, 1, 2'
    """
    return sep.join(str(x) for x in lst) + end


def list2d_printer(
    lst: Iterable[Iterable[Any]], sep: str = "\n", inner_sep: str = " ", end: str = ""
) -> str:
    """
    Format a 2D iterable (matrix) as a string.

    Args:
        lst: 2D iterable to format (list of lists, etc.)
        sep: Separator between rows (default: newline)
        inner_sep: Separator between elements in a row (default: space)
        end: String to append at the end (default: empty)

    Returns:
        Formatted string representation of the matrix

    Examples:
        >>> matrix = [[1, 2], [3, 4]]
        >>> print(list2d_printer(matrix))
        1 2
        3 4
    """
    return sep.join(list_printer(i, sep=inner_sep) for i in lst) + end


def string_printer(lst: Iterable[Any], end: str = "") -> str:
    """
    Format an iterable as a string with no separators (concatenate elements).

    Args:
        lst: Iterable to format
        end: String to append at the end (default: empty)

    Returns:
        Concatenated string of all elements

    Examples:
        >>> string_printer(['a', 'b', 'c'])
        'abc'
        >>> string_printer([1, 2, 3])
        '123'
    """
    return list_printer(lst, "", end)


class OutputHelper:
    """
    Helper class for managing test case file output.

    Organizes test cases into separate input and output files in a
    structured directory layout.

    Args:
        in_prefix: Prefix for input files (default: "input")
        out_prefix: Prefix for output files (default: "output")
        input_directory: Directory name for input files (default: "in")
        output_directory: Directory name for output files (default: "out")
        test_directory: Root directory for tests (default: "tests")
        zip_name: Name for zip archive if needed (default: "tests")
    """

    def __init__(
        self,
        in_prefix: str = "input",
        out_prefix: str = "output",
        input_directory: str = "in",
        output_directory: str = "out",
        test_directory: str = "tests",
        zip_name: str = "tests",
    ):
        self.in_prefix = in_prefix
        self.out_prefix = out_prefix
        self.test_directory = Path(test_directory)
        self.input_path = self.test_directory / input_directory
        self.output_path = self.test_directory / output_directory
        self.zip_name = zip_name

    def create_directories(self) -> None:
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_to_file(printable: str, dir_path: Path, file_name: str) -> None:
        file_path = dir_path / file_name
        file_path.write_text(printable)

    def printer(self, inp: str, outp: str, _counter: int) -> None:
        self.create_directories()
        self.write_to_file(inp, self.input_path, f"{self.in_prefix}{_counter}.txt")
        self.write_to_file(outp, self.output_path, f"{self.out_prefix}{_counter}.txt")
