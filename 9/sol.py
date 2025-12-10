import fileinput
import math

def parse(line):
    c, r = map(lambda x: int(x) - 1, line.split(","))
    return r, c

def minmax(*args):
    mn = math.inf
    mx = -math.inf
    for n in iter(args):
        mn = min(mn, n)
        mx = max(mx, n)
    return mn, mx

def format(tiles, padding = 2):
    res = [] 
    mnr, mxr = minmax(*(r for r, c in tiles))
    mnc, mxc = minmax(*(c for r, c in tiles))

    for r in range(mnr - padding, mxr + padding + 1):
        row = []
        for c in range(mnc - padding, mxc + padding + 1):
            if (r, c) in tiles:
                row.append(tiles[(r, c)])
            else:
                row.append(".")
        res.append("".join(row))
    return "\n".join(res)

def area(r1, r2):
    r1, c1 = r1
    r2, c2 = r2

    w = abs(r1 - r2) + 1
    h = abs(c1 - c2) + 1
    return w * h

# finds intersection t-value (0..1) between two edges
def get_intersection_t(r1, c1, r2, c2, edge):
    (r3, c3), (r4, c4) = edge

    # cross product
    denom = (r4 - r3) * (c2 - c1) - (c4 - c3) * (r2 - r1)

    # collinear?
    if denom == 0:
        return None

    # calculate t(ua) and u(ub) for the intersection
    ua = ((c4 - c3) * (r1 - r3) - (r4 - r3) * (c1 - c3)) / denom
    ub = ((c2 - c1) * (r1 - r3) - (r2 - r1) * (c1 - c3)) / denom

    # check if intersection is valid for both segments
    # ua is the t-value along edge1 (the segment we care about)
    # ub is the t-value along edge2 (the polygon edge)
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return ua
    
    return None

# checks if point p lies exactly on the segment a-b.
def is_on_segment(p, a, b):
    r, c = p
    (r1, c1), (r2, c2) = a, b
    
    if not (min(r1, r2) <= r <= max(r1, r2) and 
            min(c1, c2) <= c <= max(c1, c2)):
        return False

    # are they collinear?
    cross_prod = (r2 - r1) * (c - c1) - (c2 - c1) * (r - r1)
    return abs(cross_prod) < 1e-9

# memoable before calling 
# expensive is_inside function
def is_inside_memo(p, edges, memo_pt):
    if p in memo_pt:
        return memo_pt[p]
    res = is_inside(edges, p[0], p[1])
    memo_pt[p] = res
    return res

# checks if (r, c) is inside
# the edges of a polygon
def is_inside(edges, r, c):
    cnt = 0
    for e1, e2 in edges:
        r1, c1 = e1
        r2, c2 = e2
        if is_on_segment((r, c), e1, e2):
            return True
        if (r < r1) != (r < r2) and c < c1 + ((r - r1) / (r2 - r1)) * (c2 - c1):
            cnt += 1
    return cnt % 2 == 1

# checks if segment is completely
# inside of edges of the polygon
# includes memoization dicts
def is_segment_completely_inside(segment, edges, memo_seg, memo_pt):
    p1, p2 = segment
    if p1 > p2: 
        p1, p2 = p2, p1
        segment = (p1, p2)

    if segment in memo_seg:
        return memo_seg[segment]

    rs, cs = p1
    re, ce = p2

    tvals = [0.0, 1.0]
    for edge in edges:
        if (t := get_intersection_t(rs, cs, re, ce, edge)) is not None:
            tvals.append(t)

    tvals.sort()
    for i in range(len(tvals) - 1):
        t1, t2 = tvals[i], tvals[i+1]
        
        # practically the same
        if t2 - t1 < 1e-9:
            continue

        t_mid = (t1 + t2) / 2
        
        # get mids
        mr = rs + t_mid * (re - rs)
        mc = cs + t_mid * (ce - cs)
        
        # check if mids are inside
        if not is_inside(edges, mr, mc):
            memo_seg[segment] = False
            return False

    memo_seg[segment] = True
    return True

# creates the 4 corners of a rectangle given ANY two opposite corners.
def get_rect_corners(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    
    rmin, rmax = min(r1, r2), max(r1, r2)
    cmin, cmax = min(c1, c2), max(c1, c2)
    
    return [(rmin, cmin), (rmin, cmax), (rmax, cmax), (rmax, cmin)]

# is the rectangle is completely inside the polygon?
def rect_inside(p1, p2, edges, memo_seg = {}, memo_pt = {}):
    corners = get_rect_corners(p1, p2)
    if not all(is_inside_memo(corner, edges, memo_pt) for corner in corners):
        return False
    n = len(corners)
    for seg in [(corners[i], corners[(i + 1) % n]) for i in range(n)]:
        if not is_segment_completely_inside(seg, edges, memo_seg, memo_pt):    
            return False
    return True

def part1(tiles):
    mx = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            mx = max(mx, area(tiles[i], tiles[j]))
    return mx

def part2(tiles):
    edges = list(zip(tiles, tiles[1:] + tiles[:1]))

    candidates = []
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            candidates.append((area(tiles[i], tiles[j]), i, j))

    memo_seg, memo_pt = {}, {}
    candidates.sort(reverse = True)
    for score, i, j in candidates:
        if rect_inside(tiles[i], tiles[j], edges, memo_seg, memo_pt):
            return score

def segment_span(e1, e2):
    r1, c1 = e1
    r2, c2 = e2

    if r1 == r2:
        return [(r1, c) for c in range(min(c1, c2), max(c1, c2) + 1)]
    return [(r, c1) for r in range(min(r1, r2), max(r1, r2) + 1)]

txt = "".join(fileinput.input())
tiles = [parse(line) for line in txt.splitlines()] 

print(part1(tiles))
print(part2(tiles))
