# pycontest

An easy to use testcase generator for generating testcases for online judges.

## Installation
`$ pip install git+https://github.com/matinhimself/pycontest`

## Basic Usage
```python
from pycontest import Case, IntArray, \
    IntVar

from pycontest import PrintHelper


class TestCase(Case):
    batch_size = 10

    n = IntVar(1, 10**2)
    arr = IntArray(-1000, 1000, n)

    def __inp_str__(self):
        return f"{self.n}\n" +\
                f"{PrintHelper.list_printer(self.arr)}"

    def config(self):
        self.function = min
        self.input_sequence = [self.arr]


Case.main()
```
the code above will generate something like this:
```txt
        # └───tests
        #     ├────in
        #     │     ├───test0.txt
        #     │     ├───test1.txt
        #     │     │  . . .
        #     │     └───test10.txt
        #     └────out
        #           ├───test0.txt
        #           ├───test1.txt
        #           │  . . .
        #           └───test10.txt
```
each `tests/in/test<n>.txt` file contains the output of `__inp_str__`function.

each `tests/out/test<n>.txt` file contains the the output of `function` with `*input_sequence` as parameters.

For more examples see [examples](https://github.com/matinhimself/pycontest/tree/main/examples).

### Using more than one TestCase
you can simply generate different test cases with making more classes inheriting from Case class.
```python
...
    class TestCase1(Case):
        # ...
        pass

    class TestCase2(Case):
        # ...
        pass
Case.main()
```

### Using custom generator
To using your own generator for generating variables you can use `CustomArray`.
```python
from pycontest import Case, IntVar, CustomArray
import random


def q(n: int):
    while True:
        x = random.randint(0, 3000)
        if n > 0 and x > 1000 or x == 0:
            yield 0
            n -= 1
        else:
            yield x


class TestCase(Case):
    m = IntVar(0, 5)
    arr = CustomArray(100, q, m)

    def __str__(self):
        return f"input:\n{self.m}\n" + \
               f"\n{self.arr}\n"


Case.main()

```
Here with `CustomArray` via our `q` generator we were able to generate an array that has maximum `m` 0s in and chance of a member being 0 is 1/3.

