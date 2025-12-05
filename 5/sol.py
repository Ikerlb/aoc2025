import fileinput

def parse_range(line):
    a, b = line.split("-")    
    return int(a), int(b) 

def in_ranges(i, ranges):
    for l, r in ranges:
        if l <= i <= r:
            return True
    return False

def to_disjoint_intervals(ranges):
    sranges = list(sorted(ranges))
    nranges = [sranges[0]]
    for l, r in sranges[1:]:
        pl, pr = nranges[-1]
        if pr < l: 
            nranges.append((l, r))
        elif pl <= l <= pr <= r:
            nranges.pop()
            nranges.append((pl, r))
    return nranges
            
def part1(ranges, ingredients):
    return sum(in_ranges(i, ranges) for i in ingredients)

def part2(ranges):
    res = 0
    for l, r in to_disjoint_intervals(ranges):
        res += r + 1 - l
    return res

raw_txt = "".join(line for line in fileinput.input())
raw_ranges, raw_ingredients = raw_txt.split("\n\n")

ranges = [parse_range(line) for line in raw_ranges.splitlines()]
ingredients = [int(line) for line in raw_ingredients.splitlines()]

print(part1(ranges, ingredients))
print(part2(ranges))
