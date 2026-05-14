from collections import Counter


def check_equal(input1: str, input2: str) -> bool:
    counter1 = Counter(input1)
    counter2 = Counter(input2)
    for char, count in counter1.items():
        if counter2[char] != count:
            return False
    for char, count in counter2.items():
        if counter1[char] != count:
            return False
    return True
