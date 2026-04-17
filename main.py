import time
from statistics import median
import matplotlib.pyplot as plt
import numpy as np

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
def zFunction(s):
    n = len(s)
    z = [0] * n
    l, r = 0, 0

    for i in range(1, n):
        if i <= r:
            k = i - l

            z[i] = min(r - i + 1, z[k])

        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
    return z
    
def gusfieldZ(pattern: str, text: str):
    s = pattern + "$" + text
    z = zFunction(s)
    pos = []
    m = len(pattern)

    for i in range(m + 1, len(s)):
        if z[i] == m:
            pos.append(i - m - 1)

    return pos

def measure(algo, pattern, text, reps=30):
    lengths = []
    times = []
    for n in range(10, 101, 10):
        _text = text[:len(text)*n//100]
        lengths.append(len(_text))

        rep_times = []
        for _ in range(reps):
            start = time.perf_counter()
            algo(pattern, _text)
            end = time.perf_counter()
            rep_times.append(end - start)
        times.append(np.median(rep_times))
    return lengths, times

def grouped_boxplot(short_results, long_results, title, ylabel, path):
    labels = list(short_results.keys())
    n = len(labels)
    short_data = [short_results[k] for k in labels]
    long_data  = [long_results[k]  for k in labels]

    positions_short = [2*i + 1 for i in range(n)]
    positions_long  = [2*i + 1.6 for i in range(n)]

    plt.figure(figsize=(13, 6))
    b1 = plt.boxplot(short_data, positions=positions_short, widths=0.5,
                     patch_artist=True, showmeans=True)
    b2 = plt.boxplot(long_data, positions=positions_long, widths=0.5,
                     patch_artist=True, showmeans=True)

    for box in b1['boxes']: box.set_facecolor("#9ecae1")
    for box in b2['boxes']: box.set_facecolor("#fc9272")

    plt.xticks([2*i + 1.3 for i in range(n)], labels, rotation=25, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend([b1["boxes"][0], b2["boxes"][0]], ["Short pattern", "Long pattern"])
    plt.yscale("log")  # brute force will dominate otherwise
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

if __name__ == "__main__":
    f = open("stuff/Lord of The Rings (JRR Tolkien).txt")
    text = f.read()
    f.close()

    pattern = "Frodo"
    
    algos = {
        "Brute Force": bruteForce,
        "KMP": kmp,
        "Rabin-Karp": rabinKarp,
        "Gusfield Z": gusfieldZ
    }

    results_short = {name: [] for name in algos}
    results_long = {name: [] for name in algos}

    for name, algo in algos.items():
        lengths, avg_times = measure(algo, pattern, text, reps = 5)
        plt.plot(lengths, avg_times, label=name, marker="o")

    plt.xlabel("Text length (characters)")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Pattern matching algorithm comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/comparison.png", dpi=150)
    plt.show()
