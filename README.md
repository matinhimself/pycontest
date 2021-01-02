# pycontest

A simple testcase generator for generating testcases for online judges.

## Installation
`$ pip install git+https://github.com/matinhimself/pycontest`

## Basic Usage
```python
# ~main.py
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

Case.main()
# Case.main() will start generating for all Case's subclasses
```
the code above will generate
```
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


Process finished with exit code 0

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

