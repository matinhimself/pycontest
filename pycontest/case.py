"""
Core test case generation functionality.

This module provides the base Case class that test case generators inherit from.
"""

from collections.abc import Callable
from contextlib import redirect_stdout
from io import StringIO
from typing import Any, TextIO
from unittest import mock

from pycontest.helper import OutputHelper
from pycontest.writer import OutputWriter


class NoOtpStrMethod(Exception):
    """Exception raised when __otp_str__ method needs to be overridden."""

    def __init__(self):
        self.message = "Override __otp_str__ method to customize output style."
        super().__init__(self.message)


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    """

    __case_count = 0
    batch_size = 1

    function: Callable[..., Any] | None = None
    app: str | None = None

    input_sequence: tuple | list | None = None
    output: Any = None

    writer: TextIO | OutputWriter = OutputHelper()

    separator: str = "\n"

    @staticmethod
    def main(dev_mode: bool = False) -> None:

        from pycontest import Variables

        for sc in Case.__subclasses__():
            tmp = type("tmp", sc.__bases__, dict(sc.__dict__))
            for num in range(sc.batch_size):
                for k, v in vars(sc).items():
                    if isinstance(v, Variables):
                        setattr(tmp, k, v.next())
                tm = tmp()
                tm.config()
                if tm.function and tm.input_sequence is not None:
                    tm.output = tm.function(*tm.input_sequence)
                if tm.app is not None:
                    with mock.patch("builtins.input", side_effect=tm.__inp_str__().split("\n")):
                        with mock.patch("sys.stdout", new=StringIO()) as captured_output:
                            with open(tm.app) as app_file:
                                exec(app_file.read())
                    tm.output = captured_output.getvalue()

                tm.printer()
            status = "tests passed" if dev_mode else "testcase generated"
            print(f"{sc.batch_size} {status}.")

    def printer(self) -> None:
        if isinstance(self.writer, OutputWriter):
            self.writer.printer(self.__inp_str__(), self.__otp_str__(), Case.__case_count + 1)
            Case.__case_count += 1
            return
        with redirect_stdout(self.writer):
            print(f"{self.__inp_str__()}\n{self.__otp_str__()}\n", end=self.separator)

    def initialize(self, batch_size: int) -> None:
        self.batch_size = batch_size

    def config(self) -> None:
        pass

    def __inp_str__(self) -> str:
        return f"{' '.join(str(x) for x in self.input_sequence)}\n{self.separator}"

    def __otp_str__(self) -> str:
        if self.output is not None:
            return f"{self.output}"
        raise NoOtpStrMethod
