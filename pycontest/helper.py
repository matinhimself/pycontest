from typing import Union

from pycontest import IntArray, FloatArray


class printHelper:
    endl = "\n"

    @staticmethod
    def list_printer(lst: Union[IntArray, FloatArray, list], sep="\n", end=""):
        return sep.join([str(x) for x in lst]) + end
