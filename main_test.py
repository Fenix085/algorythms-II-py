import pytest

from main import bruteForce

def test_bruteForce():
    assert bruteForce("b", "aabaa") == [2]
    assert bruteForce("abc", "abccbaabccba") == [0, 6]
    assert bruteForce("b", "aaaaa") == []
    assert bruteForce("aa", "aaaaa") == [0, 1, 2, 3]
    assert bruteForce("a b", "a aa a b aa b") == [5, 10]
