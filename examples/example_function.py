from pycontest import Case, CharArray, IntVar
from pycontest.helper import string_printer


def lcs(str1: list[str], str2: list[str], m: int, n: int) -> int:
    """Return length of longest common substring.

    Source: https://www.geeksforgeeks.org/longest-common-substring-dp-29/
    """
    matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    result = 0

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                matrix[i][j] = 0
            elif str1[i - 1] == str2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
                result = max(result, matrix[i][j])
            else:
                matrix[i][j] = 0
    return result


class TestCase(Case):
    len_str_1 = IntVar(0, 50)
    len_str_2 = IntVar(0, 50)
    str_1 = CharArray(len_str_1)
    str_2 = CharArray(len_str_2)

    def __inp_str__(self) -> str:
        return f"{string_printer(self.str_1)}\n{string_printer(self.str_2)}"

    def config(self) -> None:
        self.function = lcs
        self.input_sequence = [self.str_1, self.str_2, self.len_str_1, self.len_str_2]


if __name__ == "__main__":
    Case.main()
