

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


if __name__ == "__main__":
    f = open("stuff/Lord of The Rings (JRR Tolkien).txt")
    text = f.read()
    f.close()
    pattern = "Prologue"
    print(bruteForce(pattern, text))