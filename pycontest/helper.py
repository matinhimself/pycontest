from os import path, makedirs

endl = '\n'


def list_printer(lst, sep="\n", end=""):
    return sep.join([str(x) for x in lst]) + end


def list2d_printer(lst, sep="\n", inner_sep=" ", end=""):
    return sep.join(list_printer(i, sep=inner_sep) for i in lst) + end


def string_printer(lst, end=''):
    return list_printer(lst, "", end)


class OutputHelper:
    def __init__(self, in_prefix: str = "input", out_prefix: str = "output",
                 input_directory: str = "in", output_directory: str = "out",
                 test_directory: str = "tests", zip_name: str = "tests"):
        self.in_prefix = in_prefix
        self.out_prefix = out_prefix
        self.test_directory = test_directory
        self.input_path = path.join(self.test_directory, input_directory)
        self.output_path = path.join(self.test_directory, output_directory)
        self.zip_name = zip_name

    def create_directories(self):
        if not path.exists(self.input_path):
            makedirs(self.input_path)

        if not path.exists(self.output_path):
            makedirs(self.output_path)

    @staticmethod
    def write_to_file(printable: str, dir_path, file_name):
        relative_path = path.join(dir_path, file_name)
        with open(relative_path, "w") as f:
            f.write(printable)

    def printer(self, inp: str, outp: str, _counter: int):
        self.create_directories()
        OutputHelper.write_to_file(inp, self.input_path, f"{self.in_prefix}{str(_counter)}.txt")
        OutputHelper.write_to_file(outp, self.output_path, f"{self.out_prefix}{str(_counter)}.txt")
