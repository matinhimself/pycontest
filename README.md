# pycontest(0.1.4)

An easy to use testcase generator for generating testcases for online judges.

## Installation

`$ pip install git+https://github.com/matinhimself/pycontest`

## Basic Usage

### Types

| Type |  Description | Example |
| - | - | - |
| IntVar(a, b)| Generates a random integer N such that `a` <= N <= `b`.| `IntVar(1, IntVar(10, 20))` |
| FloatVar(a, b) |  Generates a random float N such that `a` <= N <= `b`.| `FloatVar(1.5, FloatVar(1.6, 20))`  | 
| CustomArray(l, g, *args) | Generates an array with length `l` and `g` as generator of each element | [Here]( #using-custom-generator) |
|IntArray(a, b, l)|Generates a random integer array with length `l` and `IntVar(a, b)` as generator.|`IntArray(0, 100, IntVar(0, 10**9))`|
|FloatArray(a, b, l)|Generates a random float array with length `l` and `FloatVar(a, b)` as generator.|`FloatArray(2.2, 80.3, IntVar(0, 10**9))`|
|ChoiceList(l, c_l: list or string)|Generates a random array with length `l` and a random choice of c_l |`ChoiceList(100, string.hexdigits)`|

### Usage
```python
from pycontest import Case, IntArray, \
    IntVar

from pycontest.helper import list_printer


class TestCase(Case):
    batch_size = 10

    n = IntVar(1, 10**2)
    arr = IntArray(-1000, 1000, n)

    def __inp_str__(self):
        return f"{self.n}\n" +\
                f"{list_printer(self.arr)}"

    def config(self):
        self.function = min
        self.input_sequence = [self.arr]


Case.main()
```

Instead of function you can use a python file, set `self.app` to the python file path.

```python
    def config(self):
        self.path = 'my_app.py'
```

in this method your app will run with `__inp_str__` function as input, and all the stdout prints will captured as output.
see [example_app](https://github.com/matinhimself/pycontest/blob/main/examples/example_app.py).

### writer

Default writer, writes each testcase into separate files:

```txt
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
```

each `tests/in/input<n>.txt` file contains the output of `__inp_str__`function.

each `tests/out/output<n>.txt` file contains the the output of `function` with `*input_sequence` as parameters.

For more examples and explanation see [examples](https://github.com/matinhimself/pycontest/tree/main/examples).

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
