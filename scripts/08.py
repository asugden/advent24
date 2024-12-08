import numpy as np
import re
from advent24 import fetch


def create_matrices(data: str) -> list[np.ndarray]:
    """Convert input data into a set of matrices."""
    nrows = len(data.split('\n'))
    ncols = len(data.split('\n')[0])
    vals = set(re.findall('[A-Za-z0-9]', data))
    
    data = data.replace('\n', '')
    out = []
    for v in vals:
        fmap = np.zeros((nrows, ncols))
        for pos in [i for i, c in enumerate(data) if c == v]:
            col = pos % ncols
            row = pos // ncols
            fmap[row, col] = 1
        out.append(fmap)
    return out

def antinodes(fmap: np.ndarray, cr: int, cc: int, multi: bool = False) -> np.ndarray:
    """Find all antinodes for a map and a position."""
    out = np.zeros(fmap.shape) > 1
    rows, cols = np.where(fmap == 1)

    for r, c in zip(rows, cols):
        if cr != r or cc != c:
            if multi:
                # A distance multiple of 0 also counts. This is the
                # fastest way to add that
                out[cr, cc] = True

            dr = cr - r  # Distance in rows
            dc = cc - c  # Distance in cols

            multiple = 1
            new_r = cr + dr 
            new_c = cc + dc
            while ((multiple < 2 or multi)
                   and new_r >= 0
                   and new_c >= 0
                   and new_r < fmap.shape[0]
                   and new_c < fmap.shape[1]):
                out[new_r, new_c] = True
                new_r += dr
                new_c += dc
                multiple += 1 

    return out

def map_antinodes(fmap: np.ndarray, multi: bool = False) -> np.ndarray:
    """Get the combined map of all antinodes for a single map"""
    out = np.zeros(fmap.shape) > 1
    rows, cols = np.where(fmap == 1)
    for r, c in zip(rows, cols):
        out = out | antinodes(fmap, r, c, multi)
    return out

def all_maps_antinodes(fmaps: list[np.ndarray], multi: bool = False) -> np.ndarray:
    """Get the antinodes for all maps"""
    out = np.zeros(fmaps[0].shape) > 1
    for fmap in fmaps:
        out = out | map_antinodes(fmap, multi)
    return out

data = create_matrices(fetch.txt('data/08.txt'))

all_antinodes = all_maps_antinodes(data)
print((all_antinodes > 0).sum())

all_multi_antinodes = all_maps_antinodes(data, multi=True)
print((all_multi_antinodes > 0).sum())