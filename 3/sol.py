import fileinput

def mono_stack(l, k):
    s = []
    for i, n in enumerate(l):
        rem = len(l) - 1 - i
        while s and n > s[-1] and len(s) + rem >= k:
            s.pop()
        if len(s) < k:
            s.append(n)
    return int("".join(map(str, s)))

def solve(battery_packs, k):
    res = 0
    for pack in battery_packs:
        res += mono_stack(pack, k)
    return res

def part1(battery_packs):
    return solve(battery_packs, 2)
        
def part2(battery_packs):
    return solve(battery_packs, 12)

def parse_pack(line):
    return [int(c) for c in line]

raw_txt = "".join(fileinput.input())
battery_packs = [parse_pack(line) for line in raw_txt.splitlines()]

print(part1(battery_packs))
print(part2(battery_packs))
