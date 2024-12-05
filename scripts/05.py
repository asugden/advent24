from advent24 import fetch

def load() -> tuple[list[tuple[int, int]], list[list[int]]]:
    """Load the data returning the tuples of ordering and the updates"""
    data = fetch.txt('data/05.txt')
    data = data.split('\n\n')
    orders = [tuple([int(n) for n in v.split('|')]) for v in data[0].split('\n')]
    updates = [[int(n) for n in v.split(',')] for v in data[1].split('\n')]
    return orders, updates

def following_numbers(orders: list[tuple[int, int]]) -> dict[int, set[int]]:
    """Create a dict of numbers that must follow other numbers"""
    out = {}
    for pair in orders:
        out[pair[0]] = out.get(pair[0], []) + [pair[1]]
    
    # Convert to sets
    for key in out.keys():
        out[key] = set(out[key])
    return out

def is_correct(update: list[int], follows: dict[int, set[int]]) -> bool:
    """Check if a single entry is correct"""
    for i in range(1, len(update)):
        prev_nums = set(update[:i])
        required_later_nums = follows.get(update[i], None)
        if (required_later_nums is not None and 
            len(required_later_nums.intersection(prev_nums)) > 0):
            return False
    return True

def screen(updates: list[list[int]], 
           follows: dict[int, set[int]], 
           keep_correct: bool = True) -> list[list[int]]:
    """Return only the correct updates"""
    out = []
    for update in updates:
        # Skip the first entry because no numbers precede
        fail = not is_correct(update, follows)
        
        if not fail and keep_correct:
            out.append(update)
        elif fail and not keep_correct:
            out.append(update)
    return out

def sum_mids(updates: list[list[int]]) -> int:
    """Sum the middle numbers"""
    out = 0
    for update in updates:
        out += update[(len(update) - 1)//2]
    return out

## Part 1
# start by identifying which updates are already in the right order
# the middle page number of each update (correctly-ordered)
# sum
orders, updates = load()
follows = following_numbers(orders)
correct_updates = screen(updates, follows)
print('Sum of correct update midpoints is:', sum_mids(correct_updates))

# Part 2
# Find the updates which are not in the correct order. 
# What do you get if you add up the middle page numbers after 
# correctly ordering just those updates?

def swap(updates: list[list[int]], follows: dict[int, set[int]]):
    """Swap orders based on the rules"""
    out = []
    for update in updates:
        while not is_correct(update, follows):
            i = 1
            while i < len(update):
                prev_nums = set(update[:i])
                required_later_nums = follows.get(update[i], set([]))
                mis_nums = required_later_nums.intersection(prev_nums)
                if len(mis_nums) > 0:
                    mis_num = mis_nums.pop()
                    switch_pos = update.index(mis_num)
                    update[switch_pos], update[i] = update[i], update[switch_pos]
                else:
                    i += 1
        out.append(update)
    return out

incorrect_updates = screen(updates, follows, False)
corrected_updates = swap(incorrect_updates, follows)
print('Sum of corrected update midpoints is:', sum_mids(corrected_updates))
