import fileinput

def parse_rotation(line):
    return (line[0], int(line[1:]))

txt_raw = "".join(fileinput.input())
combination = [parse_rotation(line) for line in txt_raw.splitlines()]

def step(dial, d):
    if d == "R":
        s = (dial + 1) % 100
    else:
        s = (dial - 1) % 100
    return s, int(s == 0)

def steps(dial, d, dist):
    turns = 0
    for _ in range(dist):    
        dial, nturns = step(dial, d)
        turns += nturns
    return dial, turns

def part1(combinations, start):
    dial = start
    password = 0
    for d, dist in combinations:
        dial, _ = steps(dial, d, dist)
        if dial == 0:
            password += 1
    return password

def part2(combinations, start):
    dial = start
    password = 0
    for d, dist in combinations:
        dial, turns = steps(dial, d, dist)
        password += turns
    return password

print(part1(combination, 50))
print(part2(combination, 50))
