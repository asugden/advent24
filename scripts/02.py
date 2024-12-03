import numpy as np
from advent24 import fetch

def safe(row: np.array) -> bool:
    """Determine whether a row is safe"""
    diffs = row[1:] - row[:-1]
    
    # All descending or all ascending
    if (diffs > 0).sum() < len(diffs) and (diffs < 0).sum() < len(diffs):
        return False
    
    # Differs by at most 3    
    if np.max(np.abs(diffs)) > 3:
        return False

    # Differs by at least one 
    if np.min(np.abs(diffs)) < 1:
        return False

    # All criteria are met
    return True

## Part 1

# Read data
data = fetch.numpy_rows('data/02.txt')
safe_rows = np.array([safe(row) for row in data])

print('Number of safe rows:', safe_rows.sum())

## Part 2

def damp(row: np.array) -> bool:
    """Inefficient, but tests dropping every entry"""
    if safe(row):
        # Check for the full row being safe
        return True
    elif len(row) > 2:
        # Only check for subrows if they are long enough
        for i in range(len(row)):
            # Create a subrow, dropping every position
            subrow = np.array(row.tolist()[:i] + row.tolist()[i+1:])
            if safe(subrow):
                return True

    return False


dampened_safe_rows = np.array([damp(row) for row in data])

print('Number of dampened safe rows:', dampened_safe_rows.sum())