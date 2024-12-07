import numpy as np
import itertools
from advent24 import fetch

data = fetch.txt('data/07.txt')
data = [(int(row.split(':')[0]), 
         [int(v) for v in row.split(':')[1].strip().split(' ')]) 
         for row in data.split('\n')]

def math_it_step(state: int, val: int, op: int):
    """Compute the value of a step, updating the state."""
    if op == 0:
        return state + val
    elif op == 1:
        return state*val
    else:
        return eval(f'{state}{val}')

def math_it(vals: list[int], operators: list[int]) -> int:
    """Convert operators into math and combine values"""
    state = vals[0]
    for v, op in zip(vals[1:], operators):
        state = math_it_step(state, v, op)

    # This elegant solution doesn't work with the strict left to right
    # because the output has to be computed before the concatenation.
    # fun = ('('*len(vals) + 
    #        ''.join([str(num) + ')' + ('+' if op == 0 else '*' if op == 1 else '')
    #                for num, op in zip(vals, list(operators) + [-1])]))
    # return eval(fun)

    return state


def test_row(expected: int, vals: list[int], allow_concat: bool = False) -> bool:
    """Test all permutations of a single row."""
    # Create permutations of 0s and 1s which represent + and * respectively
    permutations = list(itertools.product([0, 1, 2] if allow_concat else [0, 1], 
                                          repeat=len(vals) - 1))
    
    for perm in permutations:
        if math_it(vals, perm) == expected:
            return True
    
    return False

def screen_rows(rows, allow_concat: bool = False) -> int:
    """Evaluate which rows work and sum their expected values."""
    out = 0
    for row in rows:
        if test_row(row[0], row[1], allow_concat):
            out += row[0]
    return out

print('The sum of screened rows is:', screen_rows(data))

# Part 2
print('The sum with three operators is:', screen_rows(data, True))