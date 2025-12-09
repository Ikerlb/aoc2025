import fileinput
import math
from collections import Counter

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def __hash__(self):
        # Hashing a tuple of the attributes is a common and recommended practice
        return hash((self.x, self.y, self.z))

class UFS:
    def __init__(self, n):
        self.parents = [i for i in range(n)]
        self.sizes = [1 for i in range(n)]

    def _root(self, a):
        if self.parents[a] == a:
            return a
        rpa = self._root(self.parents[a])
        self.parents[a] = rpa
        return rpa


    def union(self, a, b):
        ra = self._root(a)
        rb = self._root(b)

        if ra == rb:
            return 0

        sa = self.sizes[ra]
        sb = self.sizes[rb]

        self.sizes[ra] = sa + sb    
        self.sizes[rb] = sa + sb

        self.parents[ra] = rb
        return sa + sb

    def groups(self):
        s = Counter()
        for i in range(len(self.parents)):
            s[self._root(i)] += 1    
        return s

def part1(points, k):
    ufs = UFS(len(points))

    s = []
    for i in range(len(points)): 
        for j in range(i + 1, len(points)):
            s.append((points[i].dist(points[j]), i, j))
    s.sort()

    for _, (d, p1, p2) in zip(range(k), s):
        ufs.union(p1, p2)
    a1, a2, a3 = ufs.groups().most_common(3)
    return a1[1] * a2[1] * a3[1]

def part2(points):
    ufs = UFS(len(points))

    s = []
    for i in range(len(points)): 
        for j in range(i + 1, len(points)):
            s.append((points[i].dist(points[j]), i, j))
    s.sort(reverse = True)

    while s:
        d, p1, p2 = s.pop()
        if ufs.union(p1, p2) == len(points):
            return points[p1].x * points[p2].x

txt = "".join(fileinput.input())
points = [Point(*map(int, line.split(","))) for line in txt.splitlines()]

print(part1(points, 1000))
print(part2(points))
