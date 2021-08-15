from unittest import mock
from io import StringIO
from contextlib import redirect_stdout
from typing import Callable, Any,  TextIO, Union

from pycontest.helper import OutputHelper
from pycontest.writer import OutputWriter


class NoOtpStrMethod(Exception):
    """Exception raised for NoToStringError"""

    def __init__(self):
        self.message = "Override __otp_str__ method to customize output style."
        super(NoOtpStrMethod, self).__init__(self.message)


class Case:
    """A base class that TestCases will inherit that, by default it will generate a testCase only once
    you can change that by changing the batch_size.
    @param 
    """
    __case_count = 0
    batch_size = 1

    function: Callable[..., Any] = None
    app = None

    input_sequence = None
    output = None

    writer: Union[TextIO, OutputWriter] = OutputHelper()

    separator: str = "\n"

    @staticmethod
    def main(dev_mode=False):

        for sc in Case.__subclasses__():
            tmp = type('tmp', sc.__bases__, dict(sc.__dict__))
            for num in range(sc.batch_size):
                for k, v in vars(sc).items():
                    from pycontest import Variables
                    if isinstance(v, Variables):
                        setattr(tmp, k, v.next())
                tm = tmp()
                tm.config()
                if tm.function and tm.input_sequence is not None:
                    tm.output = tm.function(*tm.input_sequence)
                if tm.app is not None:
                    print(tm.__inp_str__().split('\n'))
                    with mock.patch('builtins.input', side_effect=tm.__inp_str__().split('\n')):
                        with mock.patch('sys.stdout', new=StringIO()) as capturedOutput:
                            exec(tm.app)
                    tm.output = capturedOutput.getvalue()

                tm.printer()
            if dev_mode:
                print(f"{sc.batch_size} tests passed.")
            else:
                print(f"{sc.batch_size} testcase generated.")

    def printer(self):
        if isinstance(self.writer, OutputWriter):
            self.writer.printer(self.__inp_str__(), self.__otp_str__(), Case.__case_count)
            Case.__case_count += 1
            return
        with redirect_stdout(self.writer):
            print(self.__inp_str__() + "\n" + self.__otp_str__() + "\n", end=self.separator)

    def initialize(self, batch_size):
        self.batch_size = batch_size

    def config(self):
        pass

    def __inp_str__(self) -> str:
        return f"{' '.join([str(x) for x in self.input_sequence])}\n" + \
               self.separator

    def __otp_str__(self) -> str:
        if self.output is not None:
            return f"{self.output}"
        else:
            raise NoOtpStrMethod
