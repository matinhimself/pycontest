import logging
import sys
from contextlib import redirect_stdout
from typing import Callable, Any, Optional

from pycontest.helper import OutputHelper


class NoOtpStrMethod(Exception):
    """Exception raised for NoToStringError"""

    def __init__(self):
        self.message = "Override __otp_str__ method to customize output style."
        super(NoOtpStrMethod, self).__init__(self.message)


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    """
    __case_count = 0
    batch_size = 1
    input_sequence = None
    function: Callable[..., Any] = None
    output = None
    writer = OutputHelper()
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

    def printer(self):
        if isinstance(self.writer, OutputHelper):
            self.writer.printer(self.__inp_str__(), self.__otp_str__(), Case.__case_count)
            Case.__case_count += 1
            return
        with redirect_stdout(self.writer):
            print(self.__inp_str__() + "\n" + self.__otp_str__() + "\n", end=self.separator)

    def initialize(self, batch_size):
        self.batch_size = batch_size

    def config(self):
        pass

    def __inp_str__(self) -> str:
        return f"{' '.join([str(x) for x in self.input_sequence])}\n" + \
               self.separator

    def __otp_str__(self) -> str:
        if self.output is not None:
            return f"{self.output}"
        else:
            raise NoOtpStrMethod
