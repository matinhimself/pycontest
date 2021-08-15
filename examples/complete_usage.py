import string
import random
from typing import Generator

from pycontest import Case, IntArray, \
    IntVar, FloatVar, FloatArray, ChoiceList, CustomArray

from pycontest.helper import list_printer, string_printer


# skip this for now.
# Gamma distribution random generator as a custom generator.
def custom_generator(f1: float, f2: float, n: int) -> Generator[float, float, None]:
    for i in range(n):
        yield random.gammavariate(f1, f2) * 100 // 1 / 100


# just like pythons unittest module,
# define your testcase classes inheriting `pycontest.Case`
# and call Case.main() to start generating testcases.
class TestCase(Case):
    # defines how many test cases will be generated
    batch_size = 11

    # variables:

    # single Integer Variable
    n = IntVar(1, 10)

    # Array of Integer with given size and bounds
    # you can use Variables in arguments of variables constructors too!
    arr = IntArray(lower_bound=0, upper_bound=100, length=n)

    # single float Variable
    f1 = FloatVar(1, 10, decimal_places=2)
    f2 = FloatVar(f1, 10, decimal_places=2)

    # Array of Integer with given size and bounds
    float_arr = FloatArray(f1, f2, n, decimal_places=3)

    # An array from Choice List with given size
    letters = ChoiceList(n, string.ascii_uppercase)

    # An array from your custom generator function.
    gamma_gen = CustomArray(n, custom_generator, f1, f2, n)

    # defines how inputs will be printed to the writer
    def __inp_str__(self):
        return f"input: \n{self.n}\n" + \
               f"{list_printer(self.arr, sep=', ')}\n" + \
               f"{self.f1}\n" + \
               f"{self.f2}\n" + \
               f"{list_printer(self.float_arr, sep=', ')}\n" + \
               f"{string_printer(self.letters)}\n" + \
               f"{self.gamma_gen}\n"

    # defines how outputs will be printed to the writer
    def __otp_str__(self) -> str:
        return f"output: \n{self.output}"

    def config(self):
        # if u want generate output, you have 2 options
        #
        # 1: using a function; just set self.function
        # here we will use builtin min function
        # that return minimum value of a list
        self.function = min
        # then set your functions input arguments
        # here we will pass both arr and float_arr to the min function
        self.input_sequence = [[*self.arr, *self.float_arr]]

        # or
        # 2: using a python application.
        # you can generate output with your python program.
        # just set your application path like
        # self.app = r'my_min.py'
        # and pycontest will use __inp_str__
        # to generate the input for your program
        # and mock it as std.in to your program.
        # see https://github.com/matinhimself/pycontest/blob/main/examples/example_app.py

        # Default writer, writes each testcase
        # into separate files like below:
        # └───tests
        #     ├────in
        #     │     ├───input0.txt
        #     │     ├───input1.txt
        #     │     │  . . .
        #     │     └───input10.txt
        #     └────out
        #           ├───output0.txt
        #           ├───output1.txt
        #           │  . . .
        #           └───output10.txt
        #
        # + You can customize directory names
        #   , input/output and ... of default writer helper.OutputHelper.
        #       self.writer = OutputHelper(kwargs)
        #
        # - Make your own writer class implementing
        #     writer.OutputWriter Protocol
        #
        # - If you want to print all testCases
        #   in terminal:
        #       self.writer = sys.stdout
        #
        # - If you want all test cases in a file:
        #       self.writer = open("file.txt","a")

        # sys.redirect_stdout will close
        # io automatically after printing
        self.writer = open("./tests.txt", "a")


if __name__ == '__main__':
    Case.main()
