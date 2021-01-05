import pycontest


class TestCases(pycontest.Case):
    n = pycontest.IntVar(0, 10)
    arr = pycontest.FloatArray(0, 10 ** 2, n)

    def __str__(self):
        return f"input:\n{self.n}\n" + \
               f"{self.arr}" + \
               f"\noutput:\n{self._output}"

    def config(self):
        self.function = min
        self.input_sequence = self.arr


pycontest.Case.main()
