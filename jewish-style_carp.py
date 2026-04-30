import random
import time

HASH_BASE = 11
HASH_BITS = 64
MASK = (1 << HASH_BITS) - 1


def rabin_karp_2d(picture, window_size):
    num_rows, num_cols = len(picture), len(picture[0])

    if window_size > num_rows or window_size > num_cols:
        return []

    base_power = 1
    for _ in range(window_size - 1):
        base_power = (base_power * HASH_BASE) & MASK

    num_window_rows = num_rows - window_size + 1
    reference_col = num_cols - window_size

    column_hashes = [[0] * num_cols for _ in range(num_window_rows)]

    for col_index in range(num_cols):
        rolling_hash = 0
        for row_index in range(window_size):
            rolling_hash = (rolling_hash * HASH_BASE + picture[row_index][col_index]) & MASK
        column_hashes[0][col_index] = rolling_hash

        for row_start in range(1, num_window_rows):
            rolling_hash = (
                (rolling_hash - picture[row_start - 1][col_index] * base_power)
                * HASH_BASE
                + picture[row_start + window_size - 1][col_index]
            ) & MASK
            column_hashes[row_start][col_index] = rolling_hash

    reference_hash = 0
    for col_index in range(reference_col, num_cols):
        reference_hash = (reference_hash * HASH_BASE + column_hashes[0][col_index]) & MASK

    duplicate_positions = []

    for row_start in range(num_window_rows):
        rolling_hash = 0
        for col_index in range(window_size):
            rolling_hash = (rolling_hash * HASH_BASE + column_hashes[row_start][col_index]) & MASK

        if rolling_hash == reference_hash:
            if not (row_start == 0 and 0 == reference_col):
                if _verify(picture, row_start, 0, window_size, num_cols):
                    duplicate_positions.append((row_start, 0))

        for col_start in range(1, num_cols - window_size + 1):
            rolling_hash = (
                (rolling_hash - column_hashes[row_start][col_start - 1] * base_power)
                * HASH_BASE
                + column_hashes[row_start][col_start + window_size - 1]
            ) & MASK

            if rolling_hash == reference_hash:
                if not (row_start == 0 and col_start == reference_col):
                    if _verify(picture, row_start, col_start, window_size, num_cols):
                        duplicate_positions.append((row_start, col_start))

    return duplicate_positions

def _verify(picture, row_start, col_start, window_size, num_cols):
    reference_row, reference_col = 0, num_cols - window_size
    for row_offset in range(window_size):
        for col_offset in range(window_size):
            if picture[row_start + row_offset][col_start + col_offset] != picture[reference_row + row_offset][reference_col + col_offset]:
                return False
    return True


def demo_small():
    """The 4×4 example from the walkthrough."""
    picture = [
        [1, 2, 7, 3],
        [4, 5, 8, 9],
        [7, 3, 6, 0],
        [8, 9, 1, 2],
    ]
    window_size = 2
    print("=== Small demo (4×4, K=2) ===")
    print("Picture:")
    for row in picture:
        print("  ", row)
    print(f"Top-right {window_size}×{window_size} corner:")
    num_cols = len(picture[0])
    for row_index in range(window_size):
        print("  ", [picture[row_index][col_index] for col_index in range(num_cols - window_size, num_cols)])
 
    duplicate_positions = rabin_karp_2d(picture, window_size)
    print(f"Duplicates found at: {duplicate_positions}")
    print()
 
 
def demo_large():
    """Random 500×500 picture with a planted duplicate."""
    num_rows, num_cols, window_size = 500, 500, 10
    random.seed(42)
    picture = [[random.randint(0, 255) for _ in range(num_cols)] for _ in range(num_rows)]
 
    # plant the top-right 10×10 corner at position (250, 100)
    for row_offset in range(window_size):
        for col_offset in range(window_size):
            picture[250 + row_offset][100 + col_offset] = picture[row_offset][num_cols - window_size + col_offset]
 
    print(f"=== Large demo ({num_rows}×{num_cols}, K={window_size}) ===")
    t0 = time.perf_counter()
    duplicate_positions = rabin_karp_2d(picture, window_size)
    elapsed = time.perf_counter() - t0
    print(f"Duplicates found at: {duplicate_positions}")
    print(f"Time: {elapsed:.4f} s")
    print()
 
 
def demo_no_match():
    """Confirm no false positives on a random picture with no planted duplicate."""
    num_rows, num_cols, window_size = 200, 200, 5
    random.seed(99)
    picture = [[random.randint(0, 255) for _ in range(num_cols)] for _ in range(num_rows)]
 
    print(f"=== No-match demo ({num_rows}×{num_cols}, K={window_size}) ===")
    duplicate_positions = rabin_karp_2d(picture, window_size)
    print(f"Duplicates found at: {duplicate_positions}  (expected: none)")
    print()

if __name__ == "__main__":
    demo_small()
    demo_large()
    demo_no_match()