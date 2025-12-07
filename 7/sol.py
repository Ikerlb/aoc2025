import fileinput
from collections import deque
from itertools import product
from functools import lru_cache

def in_bounds(grid, r, c):
    if not 0 <= r < len(grid):
        return False
    if not 0 <= c < len(grid[0]):
        return False
    return True

def find_start(grid):
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "S":
            return r, c

def part1(grid, sr, sc):
    s = [(sr, sc)]
    splitters = set()
    while s:
        r, c = s.pop()
        if (r, c) in splitters:
            continue
        if grid[r][c] == "^" and in_bounds(grid, r, c  - 1):
            s.append((r, c - 1))         
            splitters.add((r, c))
        if grid[r][c] == "^" and in_bounds(grid, r, c  + 1):
            s.append((r, c + 1))         
            splitters.add((r, c))
        if grid[r][c] != "^" and in_bounds(grid, r + 1, c): 
            s.append((r + 1, c))
    return len(splitters)
    
def part2(grid, sr, sc):
    @lru_cache(None)
    def dp(r, c):
        if c < 0 or c == len(grid[0]):  
            return 0
        if r == len(grid):
            return 1
        if grid[r][c] == "^":
            return dp(r, c - 1) + dp(r, c + 1)
        return dp(r + 1, c)
    return dp(sr, sc)

raw_txt = "".join(fileinput.input())
grid = [list(row) for row in raw_txt.splitlines()]

sr, sc = find_start(grid)
print(part1(grid, sr, sc))
print(part2(grid, sr, sc))
