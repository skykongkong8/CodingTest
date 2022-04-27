# connected components 찾기

#1 MAP creation
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

#2 DFS로 찾기
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
                    MAP_printer(local_visited)
                    global_components_indicies.append(this_group_index)
                        
    return global_components_indicies
                    

                        
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
