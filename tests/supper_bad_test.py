from pycontest import Case, IntVar, CustomArray, Collections, FloatVar
import random
import logging


def q(n: int):
    while True:
        x = random.uniform(0, 3000)
        if n > 0 and x > 1000 or x == 0:
            yield 0
            n -= 1
        else:
            yield x


class VariableBoundingTest(Case):
    batch_size = 10000
    a = IntVar(0, 500)
    b = IntVar(a, 1000)
    c = FloatVar(a, b)

    @staticmethod
    def test_bounding(a, b, c):
        if not a <= c <= b:
            logging.error(f"Bounding Test failed.{a} {b} {c} ")

    def config(self):
        self.separator = ""
        self.function = VariableBoundingTest.test_bounding
        self.input_sequence = [self.a, self.b, self.c]

    def __str__(self):
        return ""


Case.main()
