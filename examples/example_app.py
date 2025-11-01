from pycontest import Case, FloatArray, IntArray, IntVar
from pycontest.helper import list_printer


class TestCase(Case):
    list1 = IntArray(0, 10**2, IntVar(1, 5))
    list2 = FloatArray(0, 10**2, IntVar(1, 5))

    def __inp_str__(self) -> str:
        return f"{list_printer(self.list1, sep=' ')}\n{list_printer(self.list2, sep=' ')}"

    def config(self) -> None:
        self.app = "./my_min.py"


if __name__ == "__main__":
    Case.main()
