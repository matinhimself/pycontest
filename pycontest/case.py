import sys
from contextlib import redirect_stdout


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    """
    batch_size = 1
    input_sequence = None
    function = None
    _output = None
    writer = sys.stdout

    @staticmethod
    def main():
        for sc in Case.__subclasses__():
            sc = sc()
            sc.config()
            for num in range(sc.batch_size):
                if sc.function is not None and sc.input_sequence is not None:
                    sc._output = sc.function(*sc.input_sequence)
                sc.printer()

    def printer(self):
        with redirect_stdout(self.writer):
            print(self)

    def initialize(self, batch_size):
        self.batch_size = batch_size

    def config(self):
        pass
