from typing import Protocol, runtime_checkable


@runtime_checkable
class OutputWriter(Protocol):
    """
    The testcase writer interface
    you should Implement these methods to make your own writer.
    """

    def printer(self, inp: str, otp: str, counter: int):
        pass
