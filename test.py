
import sys

a = 0
while True:
    a = a + 1
    
sys.setrecursionlimit(10 ** 8)

N, M = list(map(int, input().split()))

arr = [[] for i in range(N)]
visit = [-1 for i in range(N)]
visitIndex = [[i] for i in range(N)]
rel = [list(map(int, input().split())) for _ in range(M)]

for idx in range(len(rel)):
    _sender = rel[idx][0] - 1
    _receiver = rel[idx][1] - 1
    arr[_receiver].append(_sender)
    visitIndex[_sender].append(_receiver)


def search(idx):
    if visit[idx] > -1:
        return visit[idx]

    sum = len(arr[idx])
    for number in arr[idx]:
        if number in visitIndex[idx]:
            continue
        sum += search(number)
    visit[idx] = sum
    return sum


max = [0]
for idx in range(len(visit)):

    new = search(idx)
    if idx == 0:
        continue
    if visit[max[len(max) - 1]] < new:
        max = [idx]
    elif visit[max[len(max) - 1]] == new:
        max.append(idx)

for n in range(len(max)):
    max[n] += 1
print(*max)

