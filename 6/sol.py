import fileinput
from functools import reduce
import operator

# get op and list of nums on each column 
# assumes operator is at the begining of
# the column
def parse(ops, nums):
    ops_cols = []
    prev = 0
    for i in range(1, len(ops)):
        if ops[i] != " ":    
            ops_cols.append((ops[prev], [line[prev:i - 1] for line in nums]))
            prev = i
    ops_cols.append((ops[prev], [line[prev:i + 1] for line in nums]))
    return ops_cols

def cephalod_nums(cols):
    return [int("".join(num[i] for num in cols)) for i in range(len(cols[0]))]

def _eval(op, args):
    if op == "*":
        return reduce(operator.mul, args)
    else:
        return reduce(operator.add, args)

def solve(nums, ops):
    return sum(_eval(op, cols) for op, cols in zip(ops, nums))

raw_txt = "".join(fileinput.input())
lines = list(raw_txt.splitlines())
ops, nums = zip(*parse(lines[-1], lines[:-1]))

#p1 
print(solve([map(int, col) for col in nums], ops))

#p2
print(solve(map(cephalod_nums, nums), ops))
