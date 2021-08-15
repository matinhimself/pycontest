from unittest.mock import mock_open, Mock
from pycontest import IntVar, FloatVar, Case, IntArray, FloatArray
import unittest

mock_writer = Mock()
mock_writer.printer = Mock()


class VariableBoundingTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    a = IntVar(0, 100)
    b = IntVar(a, 200)
    c = FloatVar(a, b)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.a, self.b, self.c]
        self.function = lambda a, b, c: self.tc.assertTrue(a <= c <= b, f"{a}, {b}, {c}")
        self.writer = mock_writer


if __name__ == '__main__':
    Case.main(dev_mode=True)
