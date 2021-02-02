from pycontest import Case, IntArray, \
    IntVar, FloatVar

from pycontest import OutputHelper
from pycontest.helper import list_printer


class TestCase(Case):
    batch_size = 100
    # Times a testcase will be generated

    # Simply define variables
    m = FloatVar(0.5, 1.2, decimal_places=2)
    n = IntVar(1, 5)
    arr = IntArray(0, 100, n)

    # Override __str__ to customize
    # to customize output style.
    def __inp_str__(self):
        # We can not use \n in fstrings
        # you can use `endl` const from printHelper
        return f"input:\n{self.m} {self.n}\n" + \
               f"{list_printer(self.arr)}"

    def __otp_str__(self):
        return f"output:\n{self.output}"

    # Config method is required if you
    # want to specify the output writer
    # or define output method
    def config(self):
        # Function that generates output
        self.function = sum

        # A list of variables that will
        # passed to the `function`
        self.input_sequence = [self.arr]

        # Default writer, writes testcases
        # in this style:
        # └───tests
        #     ├────in
        #     │     ├───test0.txt
        #     │     ├───test1.txt
        #     │     │  . . .
        #     │     └───test<n>.txt
        #     └────out
        #           ├───test0.txt
        #           ├───test1.txt
        #           │  . . .
        #           └───test<n>.txt
        # You can customize directory names
        # and input/output prefix using
        # self.writer = OutputHelper(kwargs)

        # If you want to print all testCases
        # in terminal:
        # self.writer = sys.stdout

        # If you want all test cases in a file:
        # self.writer = open("file.txt","a")

        # sys.redirect_stdout will close
        # io automatically after printing


# Case.main() will start generating
# for all Case's subclasses,
# just like unittest package.
Case.main()
