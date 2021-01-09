import logging
import sys
from contextlib import redirect_stdout
from typing import Callable, Any


class NoToStringError(Exception):
    """Exception raised for NoToStringError"""

    def __init__(self):
        self.message = "Override __str__ method to customize output style."
        super(NoToStringError, self).__init__(self.message)


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    """
    batch_size = 1
    input_sequence = None
    function: Callable[..., Any] = None
    output = None
    writer = sys.stdout
    separator: str = "\n"

    @staticmethod
    def main():
        for sc in Case.__subclasses__():
            tmp = type('tmp', sc.__bases__, dict(sc.__dict__))
            for num in range(sc.batch_size):
                for k, v in vars(sc).items():
                    from pycontest import Variables
                    if isinstance(v, Variables):
                        setattr(tmp, k, v.next())
                tm = tmp()
                tm.config()
                if tm.function and tm.input_sequence:
                    tm.output = tm.function(*tm.input_sequence)
                tm.printer()

    def __str__(self):
        if self.output:
            return f"{' '.join([str(x) for x in self.input_sequence])}\n" + \
                   f"{self.output}" + self.separator
        else:
            raise NoToStringError()

    def printer(self):
        with redirect_stdout(self.writer):
            print(self.__str__(), end=self.separator)

    def initialize(self, batch_size):
        self.batch_size = batch_size

    def config(self):
        pass
