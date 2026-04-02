

# brute force approach
def bruteForce(pattern: str, text: str):
    m = len(pattern)
    n = len(text)
    for i in range(n-m):
        j = 0
        while j < m:
            if text[i+j] != pattern[j]:
                break
            j+=1
        if j == m:
            print(f"Pattern found. Index: {i}")

if __name__ == "__main__":
    f = open("stuff/Lord of The Rings (JRR Tolkien).txt")
    text = f.read()
    f.close()
    pattern = "Prologue"
    bruteForce(pattern, text)