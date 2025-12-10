import fileinput
import math
from functools import lru_cache
from itertools import combinations

def parse(line):
    lights = joltage = None
    buttons = []
    for part in line.split(" "):
        if part[0] == "[":
            lights = [0 if c == "." else 1 for c in part[1:-1]]
        elif part[0] == "(":
            inside = part[1:-1].split(",")
            buttons.append(list(map(int, inside)))
        else:
            inside = part[1:-1].split(",")
            joltage = list(map(int, inside))
    return lights, buttons, joltage

def encode_lights(l):
    res = 0
    for i, b in enumerate(l):
        res = res | (b << i)
    return res

def encode_button(button):
    res = 0
    for i in button:
        res = res | (1 << i)
    return res

def xor(*args):
    res = 0
    if len(args) == 0:
        return res
    for arg in args:
        res ^= arg
    return res

def presses(lights, buttons):
    res = []
    for k in range(len(buttons) + 1):
        for comb in combinations(range(len(buttons)), k):
            if lights == xor(*(buttons[i] for i in comb)):
                res.append(comb)
    return res

def part1(machines):
    res = 0
    for lights, buttons, _ in machines:
        blights = encode_lights(lights)
        bbuttons = [encode_button(but) for but in buttons]
        mps = min(map(len, presses(blights, bbuttons)))
        res += mps
    return res

def solve(buttons, joltages):
    bbuttons = [encode_button(but) for but in buttons]

    @lru_cache(None)
    def rec(need):
        if any(n < 0 for n in need):
            return math.inf
        if all(n == 0 for n in need):
            return 0
        lights = encode_lights([v % 2 for v in need])
        res = math.inf
        for comb in presses(lights, bbuttons):
            nneed = list(need)
            for i in comb:
                for j in buttons[i]:
                    nneed[j] -= 1
            nneed = tuple(n // 2 for n in nneed)
            cur = (2 * rec(nneed)) + len(comb)
            res = min(res, cur)
        return res
    return rec(tuple(joltages))

def part2(machines):
    res = 0
    for _, buttons, joltages in machines: 
        res += solve(buttons, joltages)
    return res

txt = "".join(fileinput.input())
machines = [parse(line) for line in txt.splitlines()]

print(part1(machines))
print(part2(machines))
