# So far...

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

#1 BFS를 레이더망처럼 사용하기


from collections import deque

from numpy import number

N = 5
MAP = [[0]*N for _ in range(N)]
dr = [0,0,1,-1]
dc = [-1,1,0,0]

def radarScan(MAP, x, y):
    # 특정 위치를 기준으로 distanceMAP을 형성하기
    visited = [[False]*N for _ in range(N)]
    queue = deque()
    init_pos = [x,y]
    queue.append(init_pos)

    visited[x][y] = True
    while queue:
        curPos = queue.popleft()

        curR, curC = curPos[0], curPos[1]

        visited[curR][curC] = True
        for i in range(4):
            tmp_r, tmp_c = curR + dr[i], curC+dc[i]
            if 0<= tmp_r < N and 0<= tmp_c < N:
                if not visited[tmp_r][tmp_c]:
                    MAP[tmp_r][tmp_c] = MAP[curR][curC] + 1
                    queue.append([tmp_r, tmp_c])
    return MAP

# radarScanData = radarScan(MAP, 2,2)
# MAP_printer(radarScanData)


# 2. 2차원 리스트에서 2차원으로 추출하고, 회전시키기

MAP = [[i*j for i in range(1,7)] for j in range(6,0,-1)]

# print("original MAP :")
# MAP_printer(MAP)

for r in range(0,len(MAP),2):
    for c in range(0, len(MAP[0]) ,2):
        twoByTwo = [maskRow[c:c+2] for maskRow in MAP[r:r+2]] 
        
        # print("extracted mask")
        # MAP_printer(twoByTwo)

        # print("CCW")
        # MAP_printer([list(row) for row in list(zip(*twoByTwo))[::-1]])

        # print("CW")
        # MAP_printer(list(row) for row in list(zip(*twoByTwo[::-1])))

# 3. 1차원 리스트를 circulating list로 바꾼 뒤 사용하기
oneDarray = [i for i in range(5)]
# print(f"before : {oneDarray}")
circulated = [oneDarray[-1]] + oneDarray[:-1]
# print(f"circulate once : {circulated}")



# 4. dice 모델링 아이디어\

"""dice = [
    TOP,
    d,
    s,
    n,
    b,
    BOTTOM
]"""


# 5. index bounding

# 5-1 : 계속해서 이어지게 하기
def index_bounder(r, c, N):
    if r >= N:
        r += N
    elif r < 0:
        r -= N
    if c >= N:
        c += N
    elif c < 0:
        c -= N
    return r,c

# 5-2 : 닿으면 반대로 돌아오게 왔다갔다하게하기
psuedo_MAP = [[[] for _ in range(N)] for i in range(N)]
# print("initMAP")
# MAP_printer(psuedo_MAP)

def index_bounder2(r, c, dr, dc, N):
    if r+dr >= N:
        dr *= -1
    elif r+dr < 0:
        dr *= -1
    if c+dc >= N:
        dc *= -1
    elif c+dc < 0:
        dc *= -1

    return r+dr, c+dc, dr, dc

sample_index = [0,0]
# dr = dr[0]
# dc = dc[0] 
r, c = sample_index[0], sample_index[1]

# for i in range(10):
#     r, c, dr, dc = index_bounder2(r, c, dr, dc, N)
    # print(f"r : {r}, c : {c}")
    # psuedo_MAP[r][c].append('*')
    # MAP_printer(psuedo_MAP)
    # psuedo_MAP[r][c].pop()






# 6. spiral indexing\

MAP = [[i*j  for i in range(1,6)] for j in range(5,-1,-1)]

def spiralIndexing(N, M): # MAP : N * M
    spiralMAPIndex = [[0]*N for _ in range(M)] 
    count = 0
    r = c = 0

    right = M - 1
    down = N -1
    left = 0
    up = 1

    dr = [0,1,0,-1]
    dc = [1,0,-1,0]

    direction = 0
    linear_index = []

    for i in range(N*M):
        spiralMAPIndex[r][c] = count
        count += 1
        linear_index.append([r,c])
        if (direction %4 == 0) and (c == right):
            direction += 1
            right -= 1
        elif (direction%4 == 1) and (r == down):
            direction += 1
            down -= 1
        elif (direction %4 == 2) and (c == left):
            direction += 1
            left += 1
        elif (direction %4 == 3) and (r == up):
            direction += 1
            up += 1
        
        r += dr[direction%4]
        c += dc[direction%4]
    return linear_index, spiralMAPIndex

linear_index, spiralMAPIndex = spiralIndexing(5, 5)

def linearizeMAP(MAP, N, M, linear_index):
    linearized_MAP = []
    for i in range(N*M):
        sp_r, sp_c = linear_index[i][0], linear_index[i][1]

        linearized_MAP.append(MAP[sp_r][sp_c])

    return linearized_MAP

# print(f"original MAP:")
# MAP_printer(MAP)

# print(f"linear_index : {linear_index}")

# print("spiralMAPIndex")
# MAP_printer(spiralMAPIndex)

# linearized_MAP = linearizeMAP(MAP, 5,5,linear_index)

# print(f"linearized Index : {linearized_MAP}")


# 7. Connected Components
connected_components_map = [[0]*10 for _ in range(10)]
for i in range(0,2):
    connected_components_map[i][3:6] = [1]*(6-3)

for i in range(3,7):
    connected_components_map[i][7:] = [1]*(len(connected_components_map) - 7)

for i in range(4, len(connected_components_map) -1):
    connected_components_map[i][5] = 1

for i in range(6,len(connected_components_map)):
    connected_components_map[i][:3] = [1]*(3-0)
# print("ORIGINAL MAP")
# MAP_printer(connected_components_map)

def getConnectedComponents(MAP, N):
    connected_components_list = []
    global_visited = [[False]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if not global_visited[r][c]:
                global_visited[r][c] = True
                if MAP[r][c] != 0:
                    new_init = [r,c]
                    queue = deque()
                    queue.append([r,c])
                    visited = [[False]*N for _ in range(N)]
                    visited[r][c] = True
                    connected_component = [[r,c]]

                    while queue:
                        curPos = queue.pop()
                        curR, curC = curPos[0], curPos[1]
                        global_visited[curR][curC] = True
                        for i in range(4):
                            tmp_r, tmp_c = curR + dr[i], curC + dc[i]
                            if 0 <= tmp_r < N and 0 <= tmp_c < N:
                                if not visited[tmp_r][tmp_c]:
                                    visited[tmp_r][tmp_c] = True
                                    if MAP[tmp_r][tmp_c] != 0:
                                        connected_component.append([tmp_r, tmp_c])
                                        queue.append([tmp_r, tmp_c])
                                        global_visited[tmp_r][tmp_c] = True

                    if len(connected_component) >= 2:
                        connected_components_list.append(connected_component)
    return connected_components_list

def number_connected_components(connected_components_map, conencted_components_list):
    component_number = 2
    for c_c in conencted_components_list:
        component_number += 1
        for index in c_c:
            r, c = index[0], index[1]
            connected_components_map[r][c] = component_number

    return connected_components_map

# connected_components_list = getConnectedComponents(connected_components_map, 10)
# numberedComponents = number_connected_components(connected_components_map, connected_components_list)
# MAP_printer(numberedComponents)
target_list = [i for i in range(5)]
combinations_of_target = []

def combinations(queue, depth, r, target_list):
    global combinations_of_target
    N = len(target_list)
    if len(queue) == r:
        combinations_of_target.append(list(queue))
        return
    elif depth == N:
        return

    queue.append(target_list[depth])
    combinations(queue, depth+1, r, target_list)

    queue.pop()
    combinations(queue, depth+1, r, target_list)

combinations(deque(), 0, 3, target_list)
print(f"combinations : {combinations_of_target}")