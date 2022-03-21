import collections
import functools
import itertools as it
from functools import partial
from typing import Dict, Generator, Hashable, Iterable, List, Set, Tuple

AdjList = Dict[Hashable, List[Hashable]]

AAS = "ACDEFGHIKLMNPQRSTVWY"
BLOSUM62 = [
    [ 4,  0, -2, -1, -2,  0, -2, -1, -1, -1, -1, -2, -1, -1, -1,  1,  0,  0, -3, -2],
    [ 0,  9, -3, -4, -2, -3, -3, -1, -3, -1, -1, -3, -3, -3, -3, -1, -1, -1, -2, -2],
    [-2, -3,  6,  2, -3, -1, -1, -3, -1, -4, -3,  1, -1,  0, -2,  0, -1, -3, -4, -3],
    [-1, -4,  2,  5, -3, -2,  0, -3,  1, -3, -2,  0, -1,  2,  0,  0, -1, -2, -3, -2],
    [-2, -2, -3, -3,  6, -3, -1,  0, -3,  0,  0, -3, -4, -3, -3, -2, -2, -1,  1,  3],
    [ 0, -3, -1, -2, -3,  6, -2, -4, -2, -4, -3,  0, -2, -2, -2,  0, -2, -3, -2, -3],
    [-2, -3, -1,  0, -1, -2,  8, -3, -1, -3, -2,  1, -2,  0,  0, -1, -2, -3, -2,  2],
    [-1, -1, -3, -3,  0, -4, -3,  4, -3,  2,  1, -3, -3, -3, -3, -2, -1,  3, -3, -1],
    [-1, -3, -1,  1, -3, -2, -1, -3,  5, -2, -1,  0, -1,  1,  2,  0, -1, -2, -3, -2],
    [-1, -1, -4, -3,  0, -4, -3,  2, -2,  4,  2, -3, -3, -2, -2, -2, -1,  1, -2, -1],
    [-1, -1, -3, -2,  0, -3, -2,  1, -1,  2,  5, -2, -2,  0, -1, -1, -1,  1, -1, -1],
    [-2, -3,  1,  0, -3,  0,  1, -3,  0, -3, -2,  6, -2,  0,  0,  1,  0, -3, -4, -2],
    [-1, -3, -1, -1, -4, -2, -2, -3, -1, -3, -2, -2,  7, -1, -2, -1, -1, -2, -4, -3],
    [-1, -3,  0,  2, -3, -2,  0, -3,  1, -2,  0,  0, -1,  5,  1,  0, -1, -2, -2, -1],
    [-1, -3, -2,  0, -3, -2,  0, -3,  2, -2, -1,  0, -2,  1,  5, -1, -1, -3, -3, -2],
    [ 1, -1,  0,  0, -2,  0, -1, -2,  0, -2, -1,  1, -1,  0, -1,  4,  1, -2, -3, -2],
    [ 0, -1, -1, -1, -2, -2, -2, -1, -1, -1, -1,  0, -1, -1, -1,  1,  5,  0, -2, -2],
    [ 0, -1, -3, -2, -1, -3, -3,  3, -2,  1,  1, -3, -2, -2, -3, -2,  0,  4, -3, -1],
    [-3, -2, -4, -3,  1, -2, -2, -3, -3, -2, -1, -4, -4, -2, -3, -3, -2, -3, 11,  2],
    [-2, -2, -3, -2,  3, -3,  2, -1, -2, -1, -1, -2, -3, -1, -2, -2, -2, -1,  2,  7],
]
BLOSUM62_DICT = {(x, y): BLOSUM62[i][j] for i, x in enumerate(AAS) for j, y in enumerate(AAS)}


PAM250 = [
    [ 2, -2,  0,  0, -3,  1, -1, -1, -1, -2, -1,  0,  1,  0, -2,  1,  1,  0, -6, -3],
    [-2, 12, -5, -5, -4, -3, -3, -2, -5, -6, -5, -4, -3, -5, -4,  0, -2, -2, -8,  0],
    [ 0, -5,  4,  3, -6,  1,  1, -2,  0, -4, -3,  2, -1,  2, -1,  0,  0, -2, -7, -4],
    [ 0, -5,  3,  4, -5,  0,  1, -2,  0, -3, -2,  1, -1,  2, -1,  0,  0, -2, -7, -4],
    [-3, -4, -6, -5,  9, -5, -2,  1, -5,  2,  0, -3, -5, -5, -4, -3, -3, -1,  0,  7],
    [ 1, -3,  1,  0, -5,  5, -2, -3, -2, -4, -3,  0,  0, -1, -3,  1,  0, -1, -7, -5],
    [-1, -3,  1,  1, -2, -2,  6, -2,  0, -2, -2,  2,  0,  3,  2, -1, -1, -2, -3,  0],
    [-1, -2, -2, -2,  1, -3, -2,  5, -2,  2,  2, -2, -2, -2, -2, -1,  0,  4, -5, -1],
    [-1, -5,  0,  0, -5, -2,  0, -2,  5, -3,  0,  1, -1,  1,  3,  0,  0, -2, -3, -4],
    [-2, -6, -4, -3,  2, -4, -2,  2, -3,  6,  4, -3, -3, -2, -3, -3, -2,  2, -2, -1],
    [-1, -5, -3, -2,  0, -3, -2,  2,  0,  4,  6, -2, -2, -1,  0, -2, -1,  2, -4, -2],
    [ 0, -4,  2,  1, -3,  0,  2, -2,  1, -3, -2,  2,  0,  1,  0,  1,  0, -2, -4, -2],
    [ 1, -3, -1, -1, -5,  0,  0, -2, -1, -3, -2,  0,  6,  0,  0,  1,  0, -1, -6, -5],
    [ 0, -5,  2,  2, -5, -1,  3, -2,  1, -2, -1,  1,  0,  4,  1, -1, -1, -2, -5, -4],
    [-2, -4, -1, -1, -4, -3,  2, -2,  3, -3,  0,  0,  0,  1,  6,  0, -1, -2,  2, -4],
    [ 1,  0,  0,  0, -3,  1, -1, -1,  0, -3, -2,  1,  1, -1,  0,  2,  1, -1, -2, -3],
    [ 1, -2,  0,  0, -3,  0, -1,  0,  0, -2, -1,  0,  0, -1, -1,  1,  3,  0, -5, -3],
    [ 0, -2, -2, -2, -1, -1, -2,  4, -2,  2,  2, -2, -1, -2, -2, -1,  0,  4, -6, -2],
    [-6, -8, -7, -7,  0, -7, -3, -5, -3, -2, -4, -4, -6, -5,  2, -2, -5, -6, 17,  0],
    [-3,  0, -4, -4,  7, -5,  0, -1, -4, -1, -2, -2, -5, -4, -4, -3, -3, -2,  0, 10],
]
PAM250_DICT = {(x, y): PAM250[i][j] for i, x in enumerate(AAS) for j, y in enumerate(AAS)}

SIMPLE_DICT = {(x, y): (1 if x == y else -1) for x in AAS for y in AAS}
SIMPLE_DICT2 = {(x, y): (1 if x == y else -2) for x in AAS for y in AAS}


def toposort(g: AdjList) -> List[Hashable]:
    """
    >>> g = {2: [3], 3: [1], 4: [0, 1], 5: [0, 2]}
    >>> toposort(g)
    [5, 4, 2, 3, 1, 0]
    """
    def _helper(v: Hashable, visited: Set[Hashable], q: collections.deque):
        if v in visited:
            return
        visited.add(v)
        for v_next in g.get(v, []):
                _helper(v_next, visited, q)
        q.appendleft(v)

    queue = collections.deque([])
    visited = set()

    vertices = set(g.keys()) | functools.reduce(set.union, map(set, g.values()))

    for v in vertices:
        _helper(v, visited, queue)

    return list(queue)


def chunked(iterable: Iterable, n: int) -> Generator:
    """
    [NOTE] Borrowed from more-itertools
    >>> list(chunked([1, 2, 3, 4, 5, 6, 7], 3))
    [(1, 2, 3), (4, 5, 6), (7,)]
    """
    iterator = iter(partial(take, n, iter(iterable)), ())
    return iterator


def take(n: int, iterable: Iterable) -> Tuple:
    """
    >>> take(3, [1, 2, 3, 4])
    (1, 2, 3)
    """
    return tuple(it.islice(iterable, n))


"""
Comparing genomes (UCSD Bioinformatics III)


"""

import collections
import itertools as it
from typing import Dict, Hashable, Iterable, List, Set, Tuple
import sys

sys.setrecursionlimit(100000)

Path = List[Hashable]
Grid = List[List[int]]
StrGrid = List[List[str]]
AdjList = Dict[Hashable, List[Hashable]]
EdgeWeight = Dict[Tuple[Hashable, Hashable], int]


def dp_change(money: int, coins: Iterable[int]) -> int:
    """Return the minimum number of coins whose total is money

    >>> dp_change(40, [50, 25, 20, 10, 5, 1])
    2
    """
    maxval = 100000000
    dp = collections.defaultdict(lambda: maxval)
    dp[0] = 0
    for x in range(1, money + 1):
        dp[x] = 1 + min(dp[x - coin] for coin in coins)
    return dp[money]


def dp_change_with_backtracking(money: int, coins: Iterable[int]) -> Tuple[int, Path]:
    """Return the minimum number of coins whose total is money and its composition

    >>> dp_change_with_backtracking(40, [50, 25, 20, 10, 5, 1])
    (2, [20, 20])
    """
    maxval = 100000000
    dp = collections.defaultdict(lambda: (maxval, None))
    dp[0] = (0, 0)  # (count, predecessor)
    for x in range(1, money + 1):
        count, pred = min((dp[x - coin][0], x - coin) for coin in coins)
        dp[x] = (1 + count, pred)

    path = []
    x = money
    while x > 0:
        _, x_prev = dp[x]
        path.append(x - x_prev)
        x = x_prev

    return dp[money][0], list(path)


def manhattan_tourist(down: Grid, right: Grid, n: int, m: int) -> int:
    """
    >>> down = [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]]
    >>> right = [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3, 3], [3, 3, 0, 2], [1, 3, 2, 2]]
    >>> manhattan_tourist(down, right, 4, 4)
    34
    """
    assert len(down) == n
    assert len(down[0]) == m + 1
    assert len(right) == n + 1
    assert len(right[0]) == m

    minval = -100000000000
    dp = collections.defaultdict(lambda: minval)

    for r in range(0, n + 1):
        for c in range(0, m + 1):
            if r == c == 0:
                dp[0, 0] = 0
            else:
                dp[r, c] = max(
                    dp[r - 1, c] + down[r - 1][c], dp[r, c - 1] + right[r][c - 1]
                )
    return dp[n, m]


def lcs_backtrack(v: str, w: str) -> StrGrid:
    s = collections.defaultdict(int)
    backtrack = [[""] * (len(w) + 1) for _ in range(len(v) + 1)]
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = int(v[i - 1] == w[j - 1])
            s[i, j] = max(s[i - 1, j], s[i, j - 1], s[i - 1, j - 1] + match)
            if s[i, j] == s[i - 1, j]:
                backtrack[i][j] = "↓"
            elif s[i, j] == s[i, j - 1]:
                backtrack[i][j] = "→"
            else:
                backtrack[i][j] = "↘"
    return backtrack


def output_lcs(backtrack: StrGrid, v: str, i: int, j: int) -> str:
    if i == 0 or j == 0:
        return ""
    if backtrack[i][j] == "↓":
        return output_lcs(backtrack, v, i - 1, j)
    elif backtrack[i][j] == "→":
        return output_lcs(backtrack, v, i, j - 1)
    else:
        return output_lcs(backtrack, v, i - 1, j - 1) + v[i - 1]


def lcs(v: str, w: str) -> str:
    """
    >>> lcs("AACCTTGG", "ACACTGTGA")
    'AACTTG'
    """
    backtrack = lcs_backtrack(v, w)
    res = output_lcs(backtrack, v, len(v), len(w))
    return res


def lcs_backtrack_all(v: str, w: str) -> StrGrid:
    s = collections.defaultdict(int)
    backtrack = [[set() for _ in (len(w) + 1)] for _ in range(len(v) + 1)]
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = int(v[i - 1] == w[j - 1])
            candidates = (s[i - 1, j], s[i, j - 1], s[i - 1, j - 1] + match)
            for candidate, dir_ in zip(candidates, "↓→↘"):
                if s[i, j] < candidate:
                    s[i, j] = candidate
                    backtrack[i][j] = {dir_}
                elif s[i, j] == candidate:
                    backtrack[i][j].add(dir_)
    return backtrack


# def lcs_all(v: str, w: str) -> Set[str]:
#     """
#     >>> lcs_all("AACCTTGG", "ACACTGTGA")
#     'AACTTG'
#     """
#     backtrack = lcs_backtrack_all(v, w)
#     res = output_lcs_all(backtrack, v, len(v), len(w))
#     return res


def longest_path_in_dag(
    g: AdjList, w: EdgeWeight, start: Hashable, goal: Hashable
) -> Tuple[int, Path]:
    """
    >>> g = {0: [1, 2], 1: [4], 2: [3], 3: [4]}
    >>> w = {(0, 1): 7, (0, 2): 4, (2, 3): 2, (1, 4): 1, (3, 4): 3}
    >>> longest_path_in_dag(g, w, 0, 4)
    (9, [0, 2, 3, 4])
    """
    g_pred = collections.defaultdict(list)
    for x, preds in g.items():
        for pred in preds:
            g_pred[pred].append(x)

    vs = toposort(g)
    dp = collections.defaultdict(lambda: -1000000)
    pred = dict()
    dp[start] = 0
    for v in vs:
        if v == start:
            continue
        for v_prev in g_pred.get(v, []):
            if dp[v] < (newmax := dp[v_prev] + w[v_prev, v]):
                dp[v] = newmax
                pred[v] = v_prev

    x = goal
    path = collections.deque([x])
    while x != start:
        x = pred[x]
        path.appendleft(x)

    return dp[goal], list(path)


if __name__ == "__main__":

    # n, m = map(int, input().split())
    # down = [[int(s) for s in input().split()] for s in range(n)]
    # _ = input()
    # right = [[int(s) for s in input().split()] for s in range(n + 1)]

    # res = manhattan_tourist(down, right, n, m)
    # print(res)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        start = int(f.readline())
        goal = int(f.readline())
        pairs = [line.strip().split(":") for line in f.readlines()]

    g = collections.defaultdict(list)
    edge_weight = dict()
    for edge, weight in pairs:
        w = int(weight)
        a, b = map(int, edge.split("->"))
        edge_weight[a, b] = w
        g[a].append(b)

    x, path = longest_path_in_dag(g, edge_weight, start, goal)
    print(x)
    print("->".join(map(str, path)))
