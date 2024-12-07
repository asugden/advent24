import numpy as np
from advent24 import fetch

data = fetch.txt('data/06.txt')
data = np.array([np.fromiter(row.replace('.', '9')
                                .replace('#', '8')
                                .replace('^', '0'), dtype=int) 
                                for row in data.split('\n')])

def trace(data: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    """Trace path from 2, moving upwards"""
    angle = 0  # 0 = up, 1 = right, 2 = down, 3 = left
    nrows, ncols = data.shape

    while (not (pos[0] == 0 and angle == 0) 
           and not (pos[0] == nrows - 1 and angle == 2)
           and not (pos[1] == 0 and angle == 3)
           and not (pos[1] == ncols and angle == 1)):
        nxt = (pos[0] - 1 if angle == 0 else pos[0] + 1 if angle == 2 else pos[0], 
               pos[1] + 1 if angle == 1 else pos[1] - 1 if angle == 3 else pos[1])
        if data[nxt[0], nxt[1]] == 8:
            angle = (angle + 1)%4
        else:
            pos = nxt
            data[nxt[0], nxt[1]] = angle

    return data

# Part 1
pos = np.where(data == 0)
traced_data = trace(data.copy(), (int(pos[0]), int(pos[1])))
print('Steps:', (traced_data < 8).sum())

# Part 2
def is_loop(data: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    """Trace path from 2, moving upwards"""
    angle = 0  # 0 = up, 1 = right, 2 = down, 3 = left
    nrows, ncols = data.shape
    first_pos = pos

    steps = 0
    while (not (pos[0] == 0 and angle == 0) 
           and not (pos[0] == nrows - 1 and angle == 2)
           and not (pos[1] == 0 and angle == 3)
           and not (pos[1] == ncols - 1 and angle == 1)):
        nxt = (pos[0] - 1 if angle == 0 else pos[0] + 1 if angle == 2 else pos[0], 
               pos[1] + 1 if angle == 1 else pos[1] - 1 if angle == 3 else pos[1])
        if data[nxt[0], nxt[1]] == 8:
            angle = (angle + 1)%4
        else:
            pos = nxt

            if data[nxt[0], nxt[1]] == angle:
                return True
            elif pos == first_pos and angle == 0 and steps > 0:
                return True

            data[nxt[0], nxt[1]] = angle
            steps += 1
    
    return False

def test_for_loops(data: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    """Test every location for loops"""
    loop_count = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (pos[0] != i or pos[1] != j) and data[i, j] != 8:
                new_block = data.copy()
                new_block[i, j] = 8
                if is_loop(new_block, pos):
                    loop_count += 1
    return loop_count

print('Loops:', test_for_loops(data, pos))