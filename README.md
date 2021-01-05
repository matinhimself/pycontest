# pycontest

An easy to use testcase generator for generating testcases for online judges.

## Installation
`$ pip install git+https://github.com/matinhimself/pycontest`

## Basic Usage
```python
from pycontest import Case, IntArray, IntVar, FloatVar

# Every test case will be a subclass of Case class
class TestCase(Case):
    # batch_size is how many times testCase will be generated 
    batch_size = 10
    
    # You can define every variable simply
    m = FloatVar(0.5, 1.2, decimal_places=2)
    n = IntVar(0, 5)
    arr = IntArray(0, 100, n)

    def __str__(self):
        # The __str__ method is required.
        # It will specify the style of generated test case
        return f"input:\n{self.m} {self.n}\n" + \
               f"{self.arr}\n"

    def config(self):
        # Config method is required if you want to specify the output writer
        # Default writer is sys.stdout so it will output to terminal by default
        self.writer = open("tests.txt", "w")
        # sys.redirect_stdout will close io automatically after printing

Case.main()
# Case.main() will start generating for all Case's subclasses, just like unittest package.
```
the code above will generate
```
./tests.txt

input:
0.94 1
[93]

input:
0.76 0
[]

...

input:
0.62 3
[62, 40, 89]
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

