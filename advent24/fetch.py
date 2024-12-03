import urllib.request
import re

import numpy as np


def numpy_cols(filename: str, skip_n: int = 0) -> list[np.array]:
    """Return data from a file by numpy columns"""
    with open(filename, 'r') as f:
        data = re.sub(r'[^\S\r\n]+', ' ', f.read())
        
        out = []
        for i, row in enumerate(data.split('\n')):
            if i >= skip_n:
                row = row.strip().split(' ')
                if len(out) == 0:
                    for col in row:
                        out.append([])
                for j, col in enumerate(row):
                    out[j].append(float(col))
        return [np.array(v) for v in out]

def numpy_rows(filename: str, skip_n: int = 0) -> list[np.array]:
    """Return data from a file by numpy rows"""
    with open(filename, 'r') as f:
        data = re.sub(r'[^\S\r\n]+', ' ', f.read())
        
        out = []
        for i, row in enumerate(data.split('\n')):
            if i >= skip_n:
                out.append(np.array([float(v) for v in row.strip().split(' ')]))
        return out

def txt(filename: str) -> str:
    """Return data from a file as raw text"""
    with open(filename, 'r') as f:
        return f.read()