import fileinput

raw_txt = "".join(fileinput.input())

def parse_range(line):
    fst, snd = line.split("-")
    return int(fst), int(snd)

def get_invalid_ids_p1(start, end):
    res = []
    for i in range(start, end + 1):    
        s = str(i)
        n = len(s)
        m = n >> 1
        if n % 2 == 0 and s[:m] == s[m:]:
            res.append(i)
    return res

def get_invalid_ids_p2(start, end):
    res = []
    for i in range(start, end + 1):
        s = str(i)
        # if periodic then
        # this holds true:
        if s in (s + s)[1:-1]:
            res.append(i)
    return res

def part1(ranges):
    res = 0
    return sum(sum(get_invalid_ids_p1(s, e)) for s, e in ranges)

def part2(ranges):
    return sum(sum(get_invalid_ids_p2(s, e)) for s, e in ranges)

ranges = [parse_range(line) for line in raw_txt.split(",")]

print(part1(ranges))
print(part2(ranges))
