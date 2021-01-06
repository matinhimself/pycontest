import pycontest
from pycontest import print_helper


class TestCases(pycontest.Case):
    batch_size = 10000
    n = pycontest.IntVar(2, 10)
    arr = pycontest.FloatArray(0, 10 ** 2, n)

    def __str__(self):
        return f"input:\n{self.n}" + \
               f"{print_helper.list_printer(self.arr)}" + \
               f"output:\n{self._output}"

    def config(self):
        self.writer = open("tests.txt", "a")
        self.function = min
        self.input_sequence = self.arr


pycontest.Case.main()
