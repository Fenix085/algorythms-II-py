import pytest

from main import bruteForce, kmp, rabinKarp

def test_bruteForce():
    assert bruteForce("b", "aabaa") == [2]
    assert bruteForce("abc", "abccbaabccba") == [0, 6]
    assert bruteForce("b", "aaaaa") == []
    assert bruteForce("aa", "aaaaa") == [0, 1, 2, 3]
    assert bruteForce("a b", "a aa a b aa b") == [5, 10]

def test_kmp():
    assert kmp("b", "aabaa") == [2]
    assert kmp("abc", "abccbaabccba") == [0, 6]
    assert kmp("b", "aaaaa") == []
    assert kmp("aa", "aaaaa") == [0, 1, 2, 3]
    assert kmp("a b", "a aa a b aa b") == [5, 10]

def test_rabinKarp():
    assert rabinKarp("b", "aabaa") == [2]
    assert rabinKarp("abc", "abccbaabccba") == [0, 6]
    assert rabinKarp("b", "aaaaa") == []
    assert rabinKarp("aa", "aaaaa") == [0, 1, 2, 3]
    assert rabinKarp("a b", "a aa a b aa b") == [5, 10]




