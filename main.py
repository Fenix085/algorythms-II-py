

# brute force approach
def bruteForce(pattern: str, text: str):
    results = []
    m = len(pattern)
    n = len(text)
    for i in range(n-m+1):
        j = 0
        while j < m:
            if text[i+j] != pattern[j]:
                break
            j+=1
        if j == m:
            results.append(i)
    return results

# Sunday
def sunday(pattern: str, text: str):
    pass

# KMP
def kmp(pattern: str, text: str):
    M = len(pattern)
    N = len(text)

    lps = [0] * M
    j = 0

    computeLPSArray(pattern, M, lps)

    i = 0
    results = []
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            results.append(i-j)
            j = lps[j-1]

        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return results

def computeLPSArray(pattern: str, M: int, lps: list):
    len = 0

    lps[0] = 0
    i = 1

    while i < M:
        if pattern[i] == pattern[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1

# fsm

# rabin-karp
def rabinKarp(pattern: str, text: str):
    # Number of characters in the input alphabet (ASCII)
    d = 256

    # A prime number for modulo operations to reduce collisions
    q = 101

    # Length of the pattern
    m = len(pattern)

    # Length of the text
    n = len(text)

    # Hash value for pattern
    p = 0

    # Hash value for current window of text
    t = 0

    # High-order digit multiplier
    h = 1

    ans = []

    for i in range(m-1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                ans.append(i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return ans

# gusfield z
if __name__ == "__main__":
    f = open("stuff/Lord of The Rings (JRR Tolkien).txt")
    text = f.read()
    f.close()
    patterns = ["There is nothing, Lady Galadriel", "	Gandalf looked at Frodo, and his eyes glinted. I knew much and I have learned much,' he answered. 'But I am not going to give an account of all my doings to you. The history of Elendil and Isildur and the One Ring is known to all the Wise. Your ring is shown to be that One Ring by the fire-writing alone, apart from any other evidence.' 'And when did you discover that?' asked Frodo, interrupting. 'Just now in this room, of course,' answered the wizard sharply. 'But I expected to find it. I have come back from dark journeys and long search to make that final test. It is the last proof, and all is now only too clear. Making out Gollum's part, and fitting it into the gap in the history, required some thought. I may have started with guesses about Gollum, but I am not guessing now. I know. I have seen him.'"]
    for pattern in patterns:
        print("Brute Force:", bruteForce(pattern, text))
        print("KMP:", kmp(pattern, text))
        print("Rabin-Karp:", rabinKarp(pattern, text))