import time
from statistics import median
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle, randint

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

LITERAL, ANY_ONE, ANY_MANY = 0, 1, 2

def tokenize(pattern: str):
    tokens = []
    i = 0
    while i < len(pattern):
        pat = pattern[i]
        if pat == "\\":
            if i + 1 >= len(pattern):
                raise ValueError("pattern ends with a dangling backslash")
            tokens.append((LITERAL, pattern[i+1]))
            i += 2
        elif pat == "?":
            tokens.append((ANY_ONE, None))
            i += 1
        elif pat == "*":
            if tokens and tokens[-1][0] == ANY_MANY:
                i += 1
                continue
            tokens.append((ANY_MANY, None))
            i += 1
        else:
            tokens.append((LITERAL, pat))
            i += 1
    return tokens

def bruteMode(pattern: str, text: str) -> bool:
    pattern_tokens = tokenize(pattern)
    text_length = len(text)
    token_count = len(pattern_tokens)
    match_table = [[False] * (token_count + 1) for _ in range(text_length + 1)]

    match_table[0][0] = True
    for token_index in range(1, token_count + 1):
        if pattern_tokens[token_index - 1][0] == ANY_MANY:
            match_table[0][token_index] = match_table[0][token_index - 1]

    for text_index in range(1, text_length + 1):
        match_table[text_index][0] = True
        for token_index in range(1, token_count + 1):
            kind, ch = pattern_tokens[token_index - 1]
            if kind == ANY_MANY:
                match_table[text_index][token_index] = match_table[text_index - 1][token_index] or match_table[text_index][token_index - 1]
            elif kind == ANY_ONE:
                match_table[text_index][token_index] = match_table[text_index - 1][token_index - 1]
            else:
                match_table[text_index][token_index] = match_table[text_index - 1][token_index - 1] and text[text_index - 1] == ch

    return any(match_table[text_index][token_count] for text_index in range(text_length + 1))

# Sunday
def sunday(pattern: str, text: str):
    len_pat, len_text = len(pattern), len(text)

    occ = {}
    for j in range(len_pat):
        occ[pattern[j]] = j

    matches = []
    i = 0
    while i <= len_text - len_pat:
        if text.startswith(pattern, i):
            matches.append(i)
        i+=len_pat
        if i < len_text:
            i -= occ.get(text[i], -1)

    return matches

def split_on_star(tokens: list):
    chunks = []
    current = []

    starts_with_star = bool(tokens) and tokens[0][0] == ANY_MANY
    ends_with_star = bool(tokens) and tokens[-1][0] == ANY_MANY

    for kind, ch in tokens:
        if kind == ANY_MANY:
            if current:
                chunks.append(current)
                current = []
            continue
        current.append((kind, ch))

    if current:
        chunks.append(current)

    prefix = bool(chunks) and not starts_with_star
    suffix = bool(chunks) and not ends_with_star
    return chunks, prefix, suffix

            

def verify(tokens: list, text: str, pos: int):
    for j, (kind, ch) in enumerate(tokens):
        if kind == ANY_ONE:
            continue
        if pos + j >= len(text) or text[pos + j] != ch:
            return False
    return True


def sundayMode(pattern: str, text: str) -> bool:
    pattern_tokens = tokenize(pattern)
    if not pattern_tokens:
        return len(text) == 0

    chunks, _, _ = split_on_star(pattern_tokens)
    if not chunks:
        return True

    text_length = len(text)
    search_start = 0

    for chunk in chunks:
        chunk_length = len(chunk)

        shift_table = {}
        wildcard_shift = chunk_length + 1
        for token_index, (kind, ch) in enumerate(chunk):
            if kind == ANY_ONE:
                wildcard_shift = min(wildcard_shift, chunk_length - token_index)
            else:
                shift_table[ch] = chunk_length - token_index

        candidate_start = search_start
        match_start = -1
        while candidate_start + chunk_length <= text_length:
            if verify(chunk, text, candidate_start):
                match_start = candidate_start
                break
            if candidate_start + chunk_length >= text_length:
                break
            next_char = text[candidate_start + chunk_length]
            candidate_start += min(shift_table.get(next_char, chunk_length + 1), wildcard_shift)

        if match_start < 0:
            return False
        search_start = match_start + chunk_length

    return True

# KMP
def kmp(pattern: str, text: str):
    len_pat = len(pattern)
    len_text = len(text)

    lps = [0] * len_pat
    j = 0

    computeLPSArray(pattern, len_pat, lps)

    i = 0
    results = []
    while i < len_text:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len_pat:
            results.append(i-j)
            j = lps[j-1]

        elif i < len_text and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return results

def computeLPSArray(pattern: str, len_pat: int, lps: list):
    len = 0

    lps[0] = 0
    i = 1

    while i < len_pat:
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
def fsm(pattern: str, text: str):
    TF = build_transition_table(pattern)
    len_pat, len_text = len(pattern), len(text)
    state = 0
    results = []
    for i in range(len_text):
        state = TF[state].get(text[i], 0)
        if state == len_pat:
            results.append(i - len_pat + 1)
    return results

def build_transition_table(pattern: str):
    TF = [{} for _ in range(len(pattern)+1)]
    X = 0
    alphabet = set(pattern)

    for state in range(len(pattern)+1):
        if state > 1:
            X = TF[X].get(pattern[state-1], 0)
        for char in alphabet:
            if state < len(pattern) and char == pattern[state]:
                TF[state][char] = state + 1
            else:
                TF[state][char] = TF[X].get(char, 0)
    return TF


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

    # Precompute h = pow(d, m-1) % q
    for i in range(m-1):
        h = (h * d) % q

    # Compute initial hash values for pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # If hash values match, check characters one by one
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                ans.append(i)

        # Calculate hash value for the next window
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

def trumpMatch(pattern: str, text: str):
    ans = []
    for _ in range(randint(3, 20)):
        a = randint(0, len(text)-1)
        if text[a] == pattern[0]:
            ans.append(a)
    return print(f"""Folks, I just invented this algorithm — right now, on the spot, nobody's ever seen anything like it. The smartest people, Ivy League, tremendous pattern matchers, they came up with some answers: {ans}. Good answers? Sure. The best? Not even close to mine.
People didn't even know what a pattern WAS before me. They were matching — I don't even want to tell you what they were matching. Sad!
And KMP? Knuth, Morris, Pratt — THREE guys. Took three guys to do what I do alone, by the way, alone, with one hand. One hand! And Gusfield Z, total disaster, I've been saying it for years. Z. What does the Z even stand for? Nobody knows. Probably "zero," as in zero matches, believe me.
99% accuracy. Maybe 100. The scientists at MIT — great school, great school, they love me there — they're still checking, but between you and me, it's 100. Rabin-Karp? Please. Obama used Rabin-Karp. That's all you need to know.
Joe Biden couldn't find this pattern if you spotted him the first character. Which, by the way, is exactly what I do, and I still find it. Incredible.""")

def measure_samples(algo, pattern, text, reps=30):

    times = []
    for _ in range(reps):
        t0 = time.perf_counter()
        algo(pattern, text)
        times.append(time.perf_counter() - t0)
    return times

def measure_scaling(algo, pattern, text, reps=30):

    lengths, times = [], []
    for n in range(10, 101, 10):
        _text = text[: len(text) * n // 100]
        lengths.append(len(_text))

        rep_times: list[float] = []
        for _ in range(reps):
            t0 = time.perf_counter()
            algo(pattern, _text)
            rep_times.append(time.perf_counter() - t0)

        times.append(float(np.median(rep_times)))
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
    plt.yscale("linear")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

def compare(pattern, text, isLong = False):
    for name, algo in ALGOS.items():
        lengths, avg_times = measure_scaling(algo, pattern, text, reps = 10)
        plt.plot(lengths, avg_times, label=name, marker="o")

    expected_short = bruteForce(pattern_short, text)
    expected_long  = bruteForce(pattern_long,  text)
    for name, algo in ALGOS.items():
        if algo != trumpMatch:
            assert algo(pattern_short, text) == expected_short, f"{name} wrong on short"
            assert algo(pattern_long,  text) == expected_long,  f"{name} wrong on long"
    print("All algorithms agree ✓")

    plt.xlabel("Text length (characters)")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Pattern matching algorithm comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if isLong:
        plt.savefig("results/comparison_long.png", dpi=150)
    else:
        plt.savefig("results/comparison.png", dpi=150)
    plt.show()

ALGOS = {
    "Brute Force": bruteForce,
    "Sunday": sunday,
    "KMP": kmp,
    "FSM": fsm,
    "Rabin-Karp": rabinKarp,
    "Gusfield Z": gusfieldZ,
    "TrumpMatch": trumpMatch
}

if __name__ == "__main__":
    f = open("stuff/Lord of The Rings (JRR Tolkien).txt")
    text = f.read()
    f.close()

    pattern_short = "Frodo"
    pattern_long = """Sam looked at his master with approval, but also with surprise: there was a look in his face and a tone in his voice that he had not known before. It had always been a notion of his that the kindness of dear Mr. Frodo was of such a high degree that it must imply a fair measure of blindness. Of course, he also firmly held the incompatible belief that Mr. Frodo was the wisest person in the world (with the possible exception of Old Mr. Bilbo and of Gandalf). Gollum in his own way, and with much more excuse as his acquaintance was much briefer, may have _made a similar mistake, confusing kindness and blindness. At any rate this speech abashed and terrified him. He grovelled on the ground and could speak no clear words but nice master.
	Frodo waited patiently for a while, then he spoke again less sternly. `Come now, Gollum or Sm�agol if you wish, tell me of this other way, and show me, if you can, what hope there is in it, enough to justify me in turning aside from my plain path. I am in haste.'
	But Gollum was in a pitiable state, and Frodo's threat had quite unnerved him. It was not easy to get any clear account out of him, amid his mumblings and squeakings, and the frequent interruptions in which he crawled on the floor and begged them both to be kind to `poor little Sm�agol'. After a while he grew a little calmer, and Frodo gathered bit by bit that, if a traveller followed the road that turned west of Ephel D�ath, he would come in time to a crossing in a circle of dark trees. On the right a road went down to Osgiliath and the bridges of the Anduin; in the middle the road went on southwards."""

    # short_results = {name: measure_samples(algo, pattern_short, text) for name, algo in ALGOS.items()}
    # long_results  = {name: measure_samples(algo, pattern_long,  text) for name, algo in ALGOS.items()}
    
    # grouped_boxplot(short_results, long_results, "Pattern matching algorithm comparison", "Runtime (seconds)", "results/boxplots.png")

    # compare(pattern_short, text)
    # compare(pattern_long, text, isLong=True)

    # s = "a"*100000
    # p = "c"*50
    # l = list(s)
    # shuffle(l)
    # wacky_karp = ''.join(l)

    short_results = {name: measure_samples(algo, pattern_short, text) for name, algo in ALGOS.items()}
    long_results  = {name: measure_samples(algo, pattern_long, text) for name, algo in ALGOS.items()}

    grouped_boxplot(
        short_results, long_results,
        "running such a pattern so that Sunday has to be faster than Gusfield Z",
        "Runtime (seconds)",
        "results/wacky_sund.png"
    )

    # print(bruteMode("b\\\\ a\?*", "aaabaaab\ a?aba"))

    text_rk = ''.join("a"*100000)

    # pattern that won't appear — random 30-char string + a rare suffix
    pattern_rk = ''.join("c"*28) + "##"