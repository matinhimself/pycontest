from __future__ import annotations

import random
import string
from typing import Union, Generator, Callable, SupportsRound, Any


class IterationNotCompleted(BaseException):
    """Generator stopped iteration. Make sure it iterates over all arrays length"""
    pass


class UndefinedVariable(Exception):
    """Exception raised for UndefinedVariable"""

    def __init__(self, variable):
        self.message = f"Variable {variable} not defined."


class BoundingError(Exception):
    """Exception raised for BoundingError"""

    def __init__(self, lower_bound, upper_bound):
        self.message = f"Lower bound less than upper bound." + \
                       f" lower bound: {lower_bound}, upper bound: {upper_bound}"
        super(BoundingError, self).__init__(self.message)


class Variables:
    """Simple Base class for all variables

    :kwargs
    -------
        * **generator**: ``Callable[..., Generator]``
        A Callable function that returns a Generator used to generate variable.

        * **decimal_places**: ``int``
        Rounds generated variables, **default**: ``no rounding``
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.generator = kwargs.get('generator')
        self.decimal_places = kwargs.get('decimal_places')

        # last will used to access last generated variable
        # in case of use Variable in other generators as parameters
        self.last = None

        # Initialize
        self.next()

    def rounder(self, val):
        if self.decimal_places and isinstance(val, SupportsRound):
            self.last = round(val, self.decimal_places)
        else:
            self.last = val
        return self.last

    def next(self):
        tmp_args = [x if not isinstance(x, (IntVar, FloatVar)) else x.last for x in self.args]
        self.last = self.rounder(self.generator(*tmp_args))
        return self.last


class BoundedVar(Variables):
    """A simple wrapper for variables that has bounding option.

    :raise *BoundingError* if bounding is wrong.
    """

    def __init__(self, lower_bound, upper_bound, *args, **kwargs):
        tmp_upper = upper_bound if not isinstance(upper_bound, Variables) else upper_bound.last
        tmp_lower = lower_bound if not isinstance(lower_bound, Variables) else lower_bound.last
        if tmp_upper < tmp_lower:
            raise BoundingError(lower_bound, upper_bound)
        super().__init__(lower_bound, upper_bound, *args, **kwargs)


class IntVar(BoundedVar):
    """Generates random random integer between lower and upper bound
    using random.randint callable.
    """

    def __init__(self, lower_bound: Union[IntVar, int], upper_bound: Union[IntVar, int], **kwargs):
        super().__init__(lower_bound, upper_bound, generator=random.randint, **kwargs)


class FloatVar(BoundedVar):
    """Generates random random float between lower and upper bound
    using random.uniform callable.
    """

    def __init__(self, lower_bound: Union[float, int, IntVar, FloatVar],
                 upper_bound: Union[float, int, IntVar, FloatVar], **kwargs):
        super().__init__(lower_bound, upper_bound, generator=random.uniform, **kwargs)


class Collections(Variables):
    """A base class for all collection type variables.
    use this CustomArray() instead if you want to make cus
    """

    def __init__(self, *args, **kwargs):
        self.length = kwargs.get('length') if kwargs.get('length') else 1
        super(Collections, self).__init__(*args, **kwargs)

    def next(self):
        # Using temp args to get current args Variable if they are
        # [:Variable:] for current generation,

        tmp_args = [x if not isinstance(x, (IntVar, FloatVar)) else x.last for x in self.args]
        tmp_length = self.length if not isinstance(self.length, IntVar) else self.length.last

        # not using temp args/length will cause to set arguments as a not
        # changeable integer for next generations.

        return [self.rounder(self.generator(*tmp_args)) for _ in range(tmp_length)]


class CustomArray(Collections):
    """A class to build custom arrays using a Generator."""

    # The difference with :Collections: class is :CustomArray: gets a Callable[..., Generator]
    # that yields each member for a generation, But Collection uses a generator
    # that returns each member of array(e.g random.randint).
    def __init__(self, length: Union[int, IntVar], generator: Callable[..., Generator[Any, Any, Any]], *args, **kwargs):
        super().__init__(*args, generator=generator, length=length, **kwargs)

    def next(self):
        tmp_args = [x if not isinstance(x, (IntVar, FloatVar)) else x.last for x in self.args]
        tmp_length = self.length if not isinstance(self.length, IntVar) else self.length.last

        # Making a generator from Callable[..., Generator] function for each generation
        gen = self.generator(*tmp_args)
        try:
            self.last = [self.rounder(next(gen)) for _ in range(tmp_length)]
        except StopIteration:
            raise IterationNotCompleted("\nGenerator stopped iteration. Make sure it iterates over all arrays length.")
        return self.last


class IntArray(Collections):
    """"Generates random integer for each member of array using random.randint generator"""

    def __init__(self, lower_bound: Union[IntVar, int], upper_bound: Union[IntVar, int],
                 length: Union[IntVar, int]):
        super().__init__(lower_bound, upper_bound, length=length, generator=random.randint, decimal_places=0)


class Array2d(Collections):
    """"Generates random integer for each member of array using random.randint generator"""

    def __init__(self, array: Union[IntArray, FloatArray], length: Union[IntVar, int]):
        self.array = array
        super().__init__(length=length)

    def next(self):
        tmp_args = [x if not isinstance(x, (IntVar, FloatVar)) else x.last for x in self.args]
        tmp_length = self.length if not isinstance(self.length, IntVar) else self.length.last

        self.last = [self.array.next() for _ in range(tmp_length)]
        return self.last


class FloatArray(Collections):
    """"Generates random float for each member of array using random.uniform generator"""

    def __init__(self, lower_bound: Union[int, float, IntVar, FloatVar],
                 upper_bound: Union[int, float, IntVar, FloatVar],
                 length: Union[int, IntVar], decimal_places: int = 1):
        super().__init__(lower_bound, upper_bound, length=length, generator=random.uniform,
                         decimal_places=decimal_places)


class ChoiceList(Collections):
    """Generates random choice from given list with random.choice generator"""

    def __init__(self, length: Union[int, IntVar], choice_list: list, *args, **kwargs):
        super().__init__(choice_list, *args, generator=random.choice, length=length, **kwargs)


class CharArray(ChoiceList):
    """"Generates random choice from all available english characters"""

    def __init__(self, length: Union[int, IntVar]):
        super().__init__(length, string.ascii_letters)
