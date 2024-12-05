from advent24 import fetch

## Part 1

def xmas_fw(rows: list[str]) -> int:
    """Count the forward numbers of xmases"""
    count = 0
    for row in rows:
        count += row.count('xmas')
    return count

def diag_to_nwse(rows: list[str]) -> tuple[list[str], list[str]]:
    """Convert diagonals into two flat string sets"""
    ncols = len(rows[0])
    nrows = len(rows)
    out = ['']*(ncols + nrows - 1)
    for rown, row in enumerate(rows):  # i is row number
        for coln, let in enumerate(row):  # j is col number
            # Imagine 10 rows by 8 cols, consider i - j and j - i and ncols + i - j and ncols + j
            #          rown, coln  ; r-c, c-r, nc+r, nc+c
            # Position of 0, 0 is 0; 0, 0, 8, 8
            # Position of 0, 1 is 1; -1, 1, 8, 9
            # Position of 0, 5 is 5; -5, 5, 8, 12
            # Position of 1, 0 is 9; 1, -1, 9, 8
            # Position of 1, 1 is 0; 0, 0, 9, 9
            # Position of 1, 2 is 1; -1, 1, 9, 10
            # Position of 1, 5 is 4; -4, 4, 9, 13
            # Position of 2, 0 is 10; 2, -2, 10, 8
            # Position of 2, 1 is 9; 1, -1, 10, 9
            # Position of 4, 1 is 11; 3, -3, 12, 9
            # Position of 2, 2 is 0; 0, 0, 10, 10
            # Position of 3, 5 is 2; -2, 2, 13, 11
            pos = coln - rown if coln >= rown else ncols + rown - coln - 1
            out[pos] += let
    return out

def rev(rows: list[str]) -> list[str]:
    """Reverse strings"""
    return [row[::-1] for row in rows]

def rev_col(rows: list[str]) -> list[str]:
    """Reverse rows"""
    return rows[::-1]

def switch_row_col(rows: list[str]) -> list[str]:
    """Switch rows and columns"""
    out = ['']*len(rows[0])
    for row in rows:
        for i, let in enumerate(row):
            out[i] += let
    return out

def all_directions(rows: list[str]) -> int:
    """Count in all directions"""
    # Forward, Backward, Up, Down
    count = xmas_fw(rows)
    count += xmas_fw(rev(rows))
    count += xmas_fw(switch_row_col(rows))
    count += xmas_fw(rev(switch_row_col(rows)))

    # Diagonal NWSE, NESW, SENW, SWNE
    count += xmas_fw(diag_to_nwse(rows))
    count += xmas_fw(diag_to_nwse(rev(rows)))
    count += xmas_fw(diag_to_nwse(rev_col(rev(rows))))
    count += xmas_fw(diag_to_nwse(rev_col(rows)))

    return count


data = fetch.txt('data/04.txt')
rows = [v.lower().strip() for v in data.strip().split('\n')]
print('Count is:', all_directions(rows))


# Part 2
def cross_mas_match(rows: list[str], search: list[str]) -> bool:
    """Check whether it is a match of X-MASes"""
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if search[i][j] != '.' and search[i][j] != rows[i][j]:
                return False
    return True

def sub_list(rows: list[str], row: int, col: int, nrows: int, ncols: int) -> list[str]:
    """Extract a sub matrix from list of strings"""
    out = []
    for n in range(row, row+nrows):
        out.append(rows[n][col:col+ncols])
    return out

def cross_mas_fw(rows: list[str]) -> int:
    """Count all x-wise MASes"""
    # There are four rotational variants of 90 degrees
    search = ['m.m',
              '.a.',
              's.s']
    variants = [search, switch_row_col(search), rev_col(search), rev(switch_row_col(search))]
    nrows = len(search)
    ncols = len(search[0])
    
    count = 0
    for srch in variants:
        # I initially made an error here, forgetting to add 1 and missing the last row
        for i in range(len(rows) - nrows + 1):
            for j in range(len(rows[i]) - ncols + 1):
                if cross_mas_match(sub_list(rows, i, j, nrows, ncols), srch):
                    count += 1
    return count

print('Count 2 is:', cross_mas_fw(rows))
