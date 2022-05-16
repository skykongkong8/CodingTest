# BFS를 레이더망처럼 사용하는 방법
from collections import deque

n = 10
MAP = [[0]*n for _ in range(n)]

dx = [1,-1,0,0]
dy = [0,0,1,-1]

def bfs(x,y,board):
    q = deque([(x,y)])
    cost = 1
    board[x][y] = cost
    while q:
        cur = q.popleft()
        
        for i in range(4):
            xx = dx[i] + cur[0]
            yy = dy[i] + cur[1]
            if 0 <= xx < n and 0 <= yy < n and not board[xx][yy]:

                board[xx][yy] = board[cur[0]][cur[1]] +1
                q.append((xx,yy))
        
bfs(5,5, MAP)

for _ in MAP:
    print(_)


# 2차원 리스트에서 2차원 추출하고, 회전시키는 인덱싱

MAP = [[i*j for i in range(8)] for j in range(8)]
for row in MAP:
    print(row)
print()

for r in range(0,len(MAP),2):
    for c in range(0, len(MAP), 2):
        piece = [indexed_row[c:c+2] for indexed_row in MAP[r:r+2]] # 이거진짜 유용함
        
        for row in piece:
            print(row)
        print()

        # rotated_piece = [[None]*len(piece) for _ in range(len(piece))]

        # for i in range(len(rotated_piece)):
        #     for j in range(len(rotated_piece)-1, -1, -1):
        #         rotated_piece[len(piece) - i - 1][j] = piece[j][i]

        # CCW
        rotated_piece = list(zip(*piece))[::-1]
        rotated_piece = [list(row) for row in rotated_piece]

        # CW
        rotated_piece = list(zip(*piece[::-1]))
        rotated_piece = [list(row) for row in rotated_piece]



        final_piece = [[None]*len(rotated_piece) for _ in range(len(rotated_piece))]

        for j in range(len(rotated_piece)):
            for k in range(len(rotated_piece)):
                final_piece[j][k] = rotated_piece[j][k]

        for row in final_piece:
            print(row)
        print()

# 3. 1차원 리스트가 꼬리에 꼬리를 물고 회전하도록 하기
MAP = [i for i in range(10)]
MAP = [MAP[-1]] + MAP[:-1]

# 4. dice 모델링 아이디어
"""
dice = [
    TOP,
    동,
    서,
    남,
    북,
    BOTTOM
]
동쪽(X)으로 가면 -> 동(X)이 curTOP (= 서(X')가 curBOTTOM), 남and북 유지, TOP이 cur서 (= BOTTOM이 cur동),  
YAW 회전:
CW -> TOP/BOTTOM유지, 남이 cur동(= 북이 cur서), 동이 cur북 (= 서가 cur남)
CCW -> TOP/BOTTOM유지, 남이 cur서(= 북이 cur동), 동이 cur남 (= 서가 cur북) 
"""

# 5. index bounding 의 아이디어 잘 기억하기
def index_bounder(r, c, N):
    """0번 인덱스와 마지막 인덱스(N-1)를 계속해서 이어주기 위한 함수"""

    if r < 0:
        r += N
    elif r >=N:
        r -= N

    if c < 0:
        c += N
    elif c >=N:
        c -= N

    return r, c

# 6.  spiral indexing transformation

"""
골뱅이 모양 나선형 인덱스를 이해하는 방법 :
회전이라는 요소를 위아래방향, 좌우 방향으로 분해하여서 생각하면 뭔가 느낌이 온다.
"""

def spiral_matrix(N):
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]

    direction = 0

    cnt = 0

    r = 0
    c = 0

    right = N-1
    down = N -1
    left = 0
    up = 1

    MAP = [[0]*N for _ in range(N)]
    for _ in range(N**2):
        # MAP[r][c] = cnt
        MAP[r][c] = (cnt - (N**2))*(-1)
        cnt +=1

        if direction %4 == 0 and c == right:
            direction += 1
            right -=1
        elif direction %4 == 1 and r == down:
            direction += 1
            down -=1
        elif direction%4 == 2 and c == left:
            direction +=1
            left +=1
        elif direction%4 == 3 and r == up:
            direction +=1
            up +=1
        r += dr[direction%4]
        c += dc[direction%4]
    return MAP

sprialMAP = spiral_matrix(5)
for row in sprialMAP:
    print(row)
print()

"""
나머지는 cnt를 연산을 통해서 조절하거나,
dr dc의 방향 순서를 조절하거나,
rot = [list(row) for row in list(zip(*matrix[::-1]))] 을 통해서 해결할 수 있다.
"""
# spiralIndexing을 다시 한번 연습하자:

N = 5
dr = [0,1,0,-1]
dc = [1,0,-1,0]

example_matrix = [[i*j for i in range(1,7)] for j in range(4, 0,-1)]

def matrix_linearization(linearIndicies, matrix):
    linearized_matrix = []
    for i in range(len(linearIndicies)):
        r, c = linearIndicies[i][0], linearIndicies[i][1]
        linearized_matrix.append(matrix[r][c])

    return linearized_matrix


def spiral_matrix(N):
    N = 4
    M = 6

    MAP = [[0]*M for _ in range(N)] # Spiral Form of Indicies
    linearized_MAPindex = [] # Linear Form of Indicies
    cnt = 0
    direction = 0


    # 만약 N X M 의 직사각행렬이면 어떻게 될까?
    

    right = M-1
    down = N-1
    left = 0
    up = 1
    r = c = 0

    for i in range(N*M):
        MAP[r][c] = cnt
        cnt += 1
        linearized_MAPindex.append([r,c])

        if direction%4 == 0 and c == right:
            direction += 1
            right -= 1
        elif direction%4 == 1 and r == down:
            direction +=1
            down -= 1
        elif direction%4 == 2 and c == left:
            direction += 1
            left += 1
        elif direction%4 == 3 and r == up:
            direction += 1
            up += 1

        r += dr[direction%4]
        c += dc[direction%4]

    return MAP, linearized_MAPindex


MAP, linearized_MAPindex = spiral_matrix(N)

linearized_matrix = matrix_linearization(linearized_MAPindex, example_matrix)

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()


print('matrix indicies - spiral form')
MAP_printer(MAP)

print("linearized Indicies")
print(linearized_MAPindex)

print('matrix : ')
MAP_printer(example_matrix)

print("linearized matrix")
print(linearized_matrix)


#7. Connected Components 깔끔한 정리:
"""
KeyPoints:

- 처음 init을 가져올 때 조건을 잘 건다.
    결국 DFS할 init을 찾고, 그 init으로 맞는 조건 안에서 DFS 하는 것이므로

- global_visited 와 local_visited를 활용하기:
    global_visited : connected component라고 확정적으로 정해진 순간에만 True 표시
    ** local_visited ** : 내부 DFS 돌면서 visited 표시하는 것. N_4나 N_8기준으로 찾고자 하는 connected component보다 한 겹씩 더 방문해있음
    -> 이러한 모양새를 나중에 이용할 수도 있을 듯. 기억하두자.

"""

#7-1 MAP creation
connected_components_map = [[0]*10 for _ in range(10)]
for i in range(0,2):
    connected_components_map[i][3:6] = [1]*(6-3)

for i in range(3,7):
    connected_components_map[i][7:] = [1]*(len(connected_components_map) - 7)

for i in range(4, len(connected_components_map) -1):
    connected_components_map[i][5] = 1

for i in range(6,len(connected_components_map)):
    connected_components_map[i][:3] = [1]*(3-0)

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

MAP_printer(connected_components_map)

#7-2 DFS로 찾기
from collections import deque
dr = [0,1,0,-1]
dc = [1,0,-1,0]
def find_connected_components(MAP):
    """
    connected components의 여러 기능들을 한번에 구현하는게 목표

    1. 찾은 순서별로 넘버링한 MAP 가지고 오기
    2. 찾은 component별 구성요소 인덱스 가지고 오기
    3. component 개수 파악하기

    -> 생각해보니 이 모든게 2를 하면 쉽게 구현되므로, 2만 하도록 하겠다.
    """
    R = len(MAP)
    C = len(MAP[0])

    
    global_visited = [[False]*C for _ in range(R)]
    global_components_indicies = []
    for r in range(R):
        for c in range(C):
            if not global_visited[r][c]:
                if MAP[r][c] != 0:
                    this_init = [r, c]

                    this_group_index = [this_init]

                    queue = deque()
                    queue.append(this_init)

                    local_visited = [[False]*C for _ in range(R)]
                    while queue:
                        curData = queue.pop()
                        curR, curC = curData[0], curData[1]
                        global_visited[curR][curC] = True
                        local_visited[curR][curC] = True

                        for i in range(4):
                            tmp_r, tmp_c = curR + dr[i], curC + dc[i]
                            if 0<= tmp_r < R and 0 <= tmp_c < C:
                                if local_visited[tmp_r][tmp_c] == False:
                                    local_visited[tmp_r][tmp_c] = True
                                    if MAP[tmp_r][tmp_c] == 1: # 조건 : 현재 위치와 인접하며, 값이 1인(존재하는) 칸
                                        this_group_index.append([tmp_r, tmp_c])
                                        global_visited[tmp_r][tmp_c] = True
                                        queue.append([tmp_r, tmp_c])
                    # MAP_printer(local_visited) # -> local visited는 Neighbor 기준 한 겹 더 감싸놓은 형국이라고 할 수 있다. N4 or N8 등
                    global_components_indicies.append(this_group_index)
                        
    return global_components_indicies
                    

# 7-3 활용하는 기능 등                      
def numbering_connected_components(components_indicies, MAP):
    numberedMAP = MAP[:]
    component_numbering = 0
    for indicies in components_indicies:
        component_numbering += 1
        for index in indicies:
            r, c = index[0], index[1]
            numberedMAP[r][c] = component_numbering
    return numberedMAP


if __name__ == '__main__':
    components_indicies = find_connected_components(connected_components_map)
    numberedMAP = numbering_connected_components(components_indicies, connected_components_map)

    MAP_printer(numberedMAP)



# 8 재귀적 DFS로 combinations 구현하기
# 끝끝내 버티다가 내가 졌다...
total_combinations = []
experiment_list = [i for i in range(6)]


def combinations(queue, curDepth, r, target_list):
    global total_combinations
    if len(queue) == r:
        total_combinations.append(list(queue))
        return
    
    elif curDepth == len(target_list):
        return
    
    queue.append(target_list[curDepth])

    combinations(queue, curDepth+1, r, target_list)

    queue.pop()
    combinations(queue, curDepth+1, r, target_list)

combinations(deque(), 0, 3, experiment_list)

print(total_combinations)

# 9 우연히 발견한 3차원 리스트 초기화 방법:
MAP = [[[] for i in range(5)] for j in range(5)]

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

MAP[1][2].append(999)

MAP_printer(MAP)

# 10 다익스트라 알고리즘 이해하기
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
        print("infinite")
    # 도달할 수 있는 경우, 거리를 출력
    else:
        print(distance[i])

