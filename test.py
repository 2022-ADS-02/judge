import sys

sys.setrecursionlimit(10 ** 8)

N = int(input())
parent = [*map(int, input().split())]
Remove = int(input())

childs = [[] for _ in range(N)]

rootNode = 0
rootNodeComplete = False
for idx in range(len(parent)):
    if parent[idx] == -1 and not rootNodeComplete:
        rootNode = idx
        rootNodeComplete = True
        continue
    childs[parent[idx]].append(idx)

for idx in range(len(childs)):
    if Remove in childs[idx]:
        childs[idx].remove(Remove)


def search(idx):
    sum = 0
    if len(childs[idx]) == 0:
        return 1
    else:
        for i in range(len(childs[idx])):
            sum += search(childs[idx][i])
        return sum

if Remove == rootNode:
    print(0)
else:
    print(search(rootNode))
exit(0)
