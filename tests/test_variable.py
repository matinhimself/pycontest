import pytest
import pycontest
from pycontest import IntVar, FloatVar


class WrongBoundingError(Exception):
    pass


class VariableBoundingTest(pycontest.Case):
    batch_size = 10000
    a = IntVar(0, 500)
    b = IntVar(a, 1000)
    c = FloatVar(a, b)

    @staticmethod
    def test_bounding(a, b, c):
        assert a <= c <= b

    def config(self):
        self.separator = ""
        self.function = VariableBoundingTest.test_bounding
        self.input_sequence = [self.a, self.b, self.c]

    def __str__(self):
        return ""

pycontest.Case.main()


