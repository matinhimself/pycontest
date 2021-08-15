from unittest.mock import Mock
from pycontest import IntVar, FloatVar, Case, IntArray, FloatArray, CustomArray
import unittest

mock_writer = Mock()
mock_writer.printer = Mock()


class ArraySizeTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    n = IntVar(1, 1000)
    arr = IntArray(0, 5, n)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.n, self.arr]
        self.function = lambda n, arr: self.tc.assertEqual(len(arr), n)
        self.writer = mock_writer


class IntArrayBoundingTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    a = IntVar(1, 100)
    b = IntVar(a, 500)
    arr = IntArray(a, b, 20)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.a, self.b, self.arr]
        self.function = lambda a, b, arr: self.tc.assertTrue(min(arr) >= a and max(arr) <= b)
        self.writer = mock_writer


class FloatArrayBoundingTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    a = FloatVar(1, 100.42)
    b = FloatVar(a, 500.1)
    arr = FloatArray(a, b, 20, decimal_places=14)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.a, self.b, self.arr]
        self.function = lambda a, b, arr: self.tc.assertTrue(min(arr) >= a and max(arr) <= b, f"{a}, {b}, {arr}")
        self.writer = mock_writer


class CustomArraySizeTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    a = FloatVar(1, 100.42)
    b = FloatVar(a, 500.1)

    @staticmethod
    def gen(f1, f2):
        while True:
            yield f1 + f2

    n = IntVar(1, 100)
    arr = CustomArray(n, gen.__get__(object, object), a, b)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.arr, self.n]
        self.function = lambda arr, n: self.tc.assertEqual(len(arr), n)
        self.writer = mock_writer


class CustomArrayGenTest(Case, ):
    tc = unittest.TestCase()

    batch_size = 1000
    a = FloatVar(1, 100.42)
    b = FloatVar(a, 500.1)

    @staticmethod
    def gen(f1, f2):
        while True:
            yield f1 + f2

    n = IntVar(1, 100)
    arr = CustomArray(n, gen.__get__(object, object), a, b)

    def __otp_str__(self) -> str:
        return ""

    def config(self):
        self.input_sequence = [self.arr, self.a, self.b]
        self.function = lambda arr, f1, f2: self.tc.assertEqual(min(arr), max(arr), f1 + f2)
        self.writer = mock_writer


if __name__ == '__main__':
    Case.main(dev_mode=True)
