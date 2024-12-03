import numpy as np
from advent24 import fetch


## Part 1

# Read data
cols = fetch.numpy_cols('data/01.txt')

# Sort is O(n), so this is O(n)
cols[0].sort()
cols[1].sort()

# Distances must be positive
dist = np.abs(cols[1] - cols[0])

# Return result
print('Part 1 result:', dist.sum())


## Part 2
# Calculate counts. There are ways to do this more efficiently,
# but let's just use a dictionary
counts = {}

# Counts are from the second column
for v in cols[1]:
    # Use the default trick to set empty values to 0
    counts[v] = counts.get(v, 0) + 1

# Create the counts column
count_col = np.array([counts.get(v, 0) for v in cols[0]])

# Multiply the results
similarity = cols[0]*count_col

print('The similarity score is:', similarity.sum())