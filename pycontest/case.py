import sys
from contextlib import redirect_stdout
from typing import Callable, Any


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    """
    batch_size = 1
    input_sequence = None
    function: Callable[..., Any] = None
    _output = None
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
                if tm.function is not None and tm.input_sequence is not None:
                    tm._output = tm.function(*tm.input_sequence)
                tm.printer()

    def printer(self):
        with redirect_stdout(self.writer):
            print(self.__str__(), end=self.separator)

    def initialize(self, batch_size):
        self.batch_size = batch_size

    def config(self):
        pass
