import fileinput
from itertools import product

def neighbors(grid, r, c):
    g = product([0, -1, 1], repeat = 2)
    next(g) # burn (0, 0)
    for dr, dc in g:
        if not 0 <= (nr := r + dr) < len(grid):
            continue
        if not 0 <= (nc := c + dc) < len(grid[0]):
            continue
        yield nr, nc

# mutates grid
def step(grid):
    n, m = len(grid), len(grid[0])
    res = 0
    rem = set()
    for r, c in product(range(n), range(m)):
        if grid[r][c] != "@":
            continue
        count = 0
        for nr, nc in neighbors(grid, r, c):
            if grid[nr][nc] == "@":
                count += 1
        if count < 4:
            rem.add((r, c))
    num_rem = len(rem)
    for r, c in rem:
        grid[r][c] = "X"
    return num_rem

def part1(grid):
    grid = [row[:] for row in grid]
    return step(grid)

def part2(grid):
    grid = [row[:] for row in grid]
    res = 0
    while (num_rem := step(grid)): 
        res += num_rem
    return res

raw_txt = "".join(fileinput.input())
grid = [list(line) for line in raw_txt.splitlines()]

print(part1(grid))
print(part2(grid))
