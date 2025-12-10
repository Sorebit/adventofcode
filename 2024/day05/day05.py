from collections import defaultdict
from pprint import pprint
import sys

rules = []
queries = []
rules_done = False

filename = "problem.in"
filename = "example.in"
filename = sys.argv[1]

with open(filename) as f:
    for l in f.readlines():
        l = l.strip()
        if not l:
            rules_done = True
        elif not rules_done:
            rules.append([int(a) for a in l.split("|")])
        else:
            queries.append([int(a) for a in l.split(",")])



graph = dict()
inv_graph = defaultdict(list)
in_degrees = defaultdict(lambda: 0)
ssc = dict()
"""strongly connected components. If ssc[u] == root, then u is in component number `root`"""

def find_ssc():
    L = []
    visited = set()

    def visit(u):
        if u in visited:
            return
        visited.add(u)
        for v in graph[u]:
            visit(v)
        L.insert(0, u)

    for n in graph:
        visit(n)

    def assign(u, root):
        if u in ssc:
            return
        ssc[u] = root
        for v in inv_graph[u]:
            assign(v, root)

    pprint(L)
    for u in L:
        assign(u, u)
    pprint(ssc)



def one():
    for src, dst in rules:
        if src not in graph:
            graph[src] = []
        graph[src].append(dst)
        inv_graph[dst].append(src)
        in_degrees[dst] += 1
        if src not in in_degrees:
            in_degrees[src] = 0
        if dst not in graph:
            graph[dst] = []

    pprint(graph)
    pprint(inv_graph)
    pprint(in_degrees)
    find_ssc()

def one_brute():
    for src, dst in rules:
        if src not in graph:
            graph[src] = set()
        if dst not in graph:
            graph[dst] = set()
        graph[src].add(dst)

    pprint(graph)

one_brute()

total = 0
for q in queries:
    print(q)
    ok = True
    for i in range(len(q) - 1):
        print(q[i], q[i+1])
        if q[i] in graph[q[i+1]]:
           print(q[i+1], "<", q[i])
           ok = False
           break
    if ok:
        total += q[len(q) // 2]
print(total)
