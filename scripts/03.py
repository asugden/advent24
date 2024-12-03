import re
import numpy as np
from advent24 import fetch

## Part 1

re_mul = r'mul\((\d+),(\d+)\)'
data = fetch.txt('data/03.txt')

matches = re.findall(re_mul, data)
muls = [int(v[0])*int(v[1]) for v in matches]

print('Mul sum is:', np.array(muls).sum())


## Part 2
def doordont_mask(txt: str, re_mul: str) -> list[int]:
    """Iterate through the text accounting for do or don't"""
    re_dont = r'(do\(\)|don\'t\(\))'
    mask = np.array([True]*len(txt))
    for m in re.finditer(re_dont, txt):
        mask[m.span()[0]:] = True if m.group() == 'do()' else False

    out = []
    for m in re.finditer(re_mul, txt):
        if mask[m.span()[0]]:
            out.append(int(m.group(1))*int(m.group(2)))
    
    return out

print('Do/dont mul sum is:', np.array(doordont_mask(data, re_mul)).sum())