# Dijkstra algorithm
import heapq
from heapq import heappush, heappop
import sys

INF = float('inf')
n, m = map(int, sys.stdin.readline().split(' '))
start = int(sys.stdin.readline())

graph = [[]for i in range(n+1)]
distance = [INF]*n+1

for _ in range(m):
    a,b,c = map(int, sys.stdin.readline().split(' '))
    graph[a].append(b,c)

def dijkstra(start):
    minheap = heapq()
    heappush(minheap, (0, start))
    distance[start] = 0
    while minheap:
        dist, now = heappop(minheap)
        if distance[now] < dist:
            continue
        for i in graph[now]:
            cost = dist + i[1]
            if cost < distance[i[0]]:
                distance[i[0]] = cost
                heappush(minheap, (cost, i[0]))
dijkstra(start)

# 모든 노드로 가기 위한 최단 거리를 출력
for i in range(1, n+1):
    # 도달할 수 없는 경우, 무한(INFINITY)이라고 출력
    if distance[i] == INF:
        print("INFINITY")
    # 도달할 수 있는 경우, 거리를 출력
    else:
        print(distance[i])
