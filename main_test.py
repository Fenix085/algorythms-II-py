import pytest

from main import bruteForce, kmp, rabinKarp, gusfieldZ, sunday, fsm, bruteMode, sundayMode

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

def test_gusfieldZ():
    assert gusfieldZ("b", "aabaa") == [2]
    assert gusfieldZ("abc", "abccbaabccba") == [0, 6]
    assert gusfieldZ("b", "aaaaa") == []
    assert gusfieldZ("aa", "aaaaa") == [0, 1, 2, 3]
    assert gusfieldZ("a b", "a aa a b aa b") == [5, 10]

def test_sunday():
    assert sunday("b", "aabaa") == [2]
    assert sunday("abc", "abccbaabccba") == [0, 6]
    assert sunday("b", "aaaaa") == []
    assert sunday("aa", "aaaaa") == [0, 1, 2, 3]
    assert sunday("a b", "a aa a b aa b") == [5, 10]

def test_fsm():
    assert fsm("b", "aabaa") == [2]
    assert fsm("abc", "abccbaabccba") == [0, 6]
    assert fsm("b", "aaaaa") == []
    assert fsm("aa", "aaaaa") == [0, 1, 2, 3]
    assert fsm("a b", "a aa a b aa b") == [5, 10]

def test_bruteMode():
    assert bruteMode("aba", "aaabaaaba") == True
    assert bruteMode("*ba", "aaabaaaba") == True
    assert bruteMode("a?a", "aaabaaaba") == True
    assert bruteMode("a?b", "aaabaaaba") == True
    assert bruteMode("a?*", "aaabaaaba") == True
    assert bruteMode("b*b", "aaabaaaba") == True
    assert bruteMode("ac", "aaabaaaba") == False
    assert bruteMode("a?c", "aaabaaaba") == False
    assert bruteMode("a?*c", "aaabaaaba") == False

def test_sundayMode():
    assert bruteMode("aba", "aaabaaaba") == True
    assert bruteMode("*ba", "aaabaaaba") == True
    assert bruteMode("a?a", "aaabaaaba") == True
    assert bruteMode("a?b", "aaabaaaba") == True
    assert bruteMode("a?*", "aaabaaaba") == True
    assert bruteMode("b*b", "aaabaaaba") == True
    assert bruteMode("ac", "aaabaaaba") == False
    assert bruteMode("a?c", "aaabaaaba") == False
    assert bruteMode("a?*c", "aaabaaaba") == False