# pycontest

An easy to use testcase generator for generating testcases for online judges.

## Installation
`$ pip install git+https://github.com/matinhimself/pycontest`

## Basic Usage
```python
from pycontest import Case, IntArray, \
    IntVar, FloatVar

from pycontest import printHelper

# A test case
class TestCase(Case):
    batch_size = 10
    # Times a testcase will be generated

    # Simply define variables
    m = FloatVar(0.5, 1.2, decimal_places=2)
    n = IntVar(1, 5)
    arr = IntArray(0, 100, n)

    # Override __str__ to customize
    # to customize output style.
    def __str__(self):
        # We can not use \n in fstrings
        # you can use `endl` const from printHelper
        return f"input:\n{self.m} {self.n}\n" + \
         f"{printHelper.list_printer(self.arr)}\n" + \
         f"output:\n{self.output}\n"

    # Config method is required if you
    # want to specify the output writer
    # or define output method
    def config(self):
        # Function that generates output
        self.function = sum
        # A list of variables that will
        # passed to the `function`
        self.input_sequence = [self.arr]

        # Default `writer` is sys.stdout
        self.writer = open("tests.txt", "a")
        # sys.redirect_stdout will close
        # io automatically after printing


# Case.main() will start generating
# for all Case's subclasses,
# just like unittest package.
Case.main()
```

the code above will generate something like this:
```
./tests.txt
input:
0.92 2
64
41
output:
105

.
.
.

input:
1.1 5
8
47
33
69
6
output:
163
```

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

