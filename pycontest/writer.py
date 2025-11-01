"""
Protocol for custom output writers.

This module defines the interface for custom test case output writers.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class OutputWriter(Protocol):
    """
    Protocol for custom test case output writers.

    Implement this protocol to create custom writers for test case output.

    Example:
        class CustomWriter:
            def printer(self, inp: str, otp: str, counter: int):
                # Custom output logic
                pass
    """

    def printer(self, inp: str, otp: str, counter: int) -> None:
        """
        Write a single test case.

        Args:
            inp: Input string for the test case
            otp: Output string for the test case
            counter: Test case number (1-indexed)
        """
        ...
