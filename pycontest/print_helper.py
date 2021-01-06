from typing import Union

from pycontest import IntArray, FloatArray


def list_printer(lst: Union[IntArray, FloatArray, list], sep=" ", end="\n"):
    return sep.join([str(x) for x in lst]) + end
