"""Exact census of the graph reduction and eight-fact example."""

from collections import Counter
from itertools import combinations
from math import comb


def tuples_for_graph(n, edges):
    r = max(2, max(sum(v in edge for edge in edges) for v in range(n)))
    rows = []
    for v in range(n):
        labels = [i for i, edge in enumerate(edges) if v in edge]
        labels.extend(-1 - v*r-j for j in range(r-len(labels)))
        rows.extend((v, label) for label in labels)
    assert len(set(rows)) == len(rows) == n*r
    return r, rows


def aggregate(retained):
    total = comb(len(retained), 2)
    return tuple(total - sum(comb(k, 2) for k in Counter(row[i] for row in retained).values())
                 for i in range(2))


def all_subsets(rows):
    for mask in range(1 << len(rows)):
        yield tuple(row for i, row in enumerate(rows) if mask & (1 << i))


def check_graphs():
    trials, checked_subsets = 0, 0
    for n in range(1, 5):
        possible_edges = tuple(combinations(range(n), 2))
        for edges in all_subsets(possible_edges):
            r, rows = tuples_for_graph(n, edges)
            N, W = len(rows), 2*len(rows)**2
            scores = []
            for retained in all_subsets(rows):
                m = len(retained)
                packed = all(k == r for k in Counter(row[0] for row in retained).values())
                b, c = aggregate(retained)
                scores.append((m, packed, W*b+c))
                checked_subsets += 1
            for k in range(1, n+1):
                w = W*r*(2*k-1)//2
                best = min(w*(N-m)+p for m, packed, p in scores)
                assert all(packed and m == k*r for m, packed, p in scores if w*(N-m)+p == best)
                max_edges = max(sum(i in S and j in S for i, j in edges)
                                for S in combinations(range(n), k))
                formula = w*(N-k*r)+W*r*r*comb(k, 2)+comb(k*r, 2)-max_edges
                assert best == formula
                trials += 1
    print(f"{trials} graph/target cases; {checked_subsets} exhaustive subset scores reused across targets.")


def direct_example():
    r, rows = tuples_for_graph(4, ((0, 1), (0, 2), (1, 2)))
    assert r == 2 and len(rows) == 8
    best = 10_000
    winners = []
    for retained in all_subsets(rows):
        b = sum(a[0] != d[0] for a, d in combinations(retained, 2))
        c = sum(a[1] != d[1] for a, d in combinations(retained, 2))
        assert aggregate(retained) == (b, c)
        cost = 640 * (8-len(retained)) + 128*b + c
        if cost < best:
            best = cost
            winners = []
        if cost == best:
            winners.append(retained)
        if retained == tuple(row for row in rows if row[0] in (0, 1, 3)):
            assert (b, c, cost) == (12, 14, 2830)
    assert best == 2828 and winners == [tuple(row for row in rows if row[0] != 3)]
    print("All 256 example subsets checked by direct pair scoring. Triangle cost 2828; blocks 1,2,4 cost 2830.")


if __name__ == "__main__":
    check_graphs()
    direct_example()
