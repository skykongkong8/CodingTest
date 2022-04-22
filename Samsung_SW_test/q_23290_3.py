# 마법사 상어와 복제
from collections import deque
dr = [0,-1,-1,-1,0,1,1,1]
dc = [-1,-1,0,1,1,1,0,-1]

shark_dr = [-1,0,1,0]
shark_dc = [0,-1,0,1]

N = 4

"""
MAP = [
    ...
    [[[fishCnt, [fishDir1, fishDir2, ...]], fishSmellCnt], ...      ]
    ...
]

MAP[r][c][0] = [fishCnt, fishDirList]
MAP[r][c][0][0] =fishCnt
MAP[r][c][0][1] = fishDirList
MAP[r][c][1] = fishSmellCnt
"""
queue_list = []
for _ in range(16):
    new_deque = deque()
    queue_list.append(new_deque)

MAP = [
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]],
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]], 
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]], 
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]]

]

cnt = 0
for i in range(N):
    for j in range(N):
        MAP[i][j][0][1] = queue_list[cnt]
        cnt+=1


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

def input_getter():
    # MAP = [[[[0,[]], 0]]*4 for _ in range(4)] # -> 파이썬 그 4차원 이상 들어가면 메모리 복제된다는 그 문제인가?
    M, S = map(int, input().split(' '))

    for _ in range(M):
        r, c, d = map(int, input().split(' '))
        MAP[r-1][c-1][0][0] += 1
        MAP[r-1][c-1][0][1].append(d-1)

    shark_r, shark_c = map(int, input().split(' '))

    return MAP, M, S, [shark_r-1, shark_c-1]

def fishMove(MAP, shark_idx):
    total_movement_history = []
    old_fishes = []
    """
    old_fishes = [
        ...
        [r,c,d]
        ...
    ]
    """
    # print()
    # print("FISH MOVE START \n")
    MAP_printer(MAP)
    for i in range(4):
        for j in range(4):
            curFishCnt = MAP[i][j][0][0]

            if curFishCnt == 0:
                continue
 
            curR, curC = i,j
            goodbye_fish_list = []
            # print(f"{i},{j} fishCount : {curFishCnt}")
            for k in range(curFishCnt):
                # print(f"{i},{j} fishList : {MAP[i][j][0][1]}")
                curFishDir = MAP[i][j][0][1].pop() # 삭제하면서 가져오는 방법 떠올리기 : 인덱싱을 하지 않기! 이 경우 대신, 움직이지 않는 물고기는 다시 넣어주어야 한다.
                old_fishes.append([curR, curC, curFishDir])

                move_out_flag = False
                original_direction = curFishDir
                for l in range(8):
                    tmp_r, tmp_c = curR + dr[curFishDir], curC + dc[curFishDir]
                    if 0 <= tmp_r < N and 0 <= tmp_c < N:
                        if MAP[tmp_r][tmp_c][1] == 0 and ([tmp_r, tmp_c] != [shark_idx[0], shark_idx[1]]):

                            """
                            goodbye_fish_list = [
                                ...
                                [[curR, curC], [tmp_r, tmp_c], changedDir, curFishDirList[k], MAP[curR][curC][0][0]] : 물고기 하나당 정보
                                ...
                            ]
                            """
                            
                            goodbye_fish_list.append([[curR, curC], [tmp_r, tmp_c], curFishDir, None, MAP[curR][curC][0][0]])
                        
                            move_out_flag = True
                            break
                


                    # print(f"cannot move to : {tmp_r}, {tmp_c}")
                    curFishDir -= 1
                    if curFishDir < 0:
                        curFishDir += 8

                if not move_out_flag:
                    MAP[curR][curC][0][1].appendleft(original_direction)

            total_movement_history.append(goodbye_fish_list)

    for goodbye_fish_list in total_movement_history:
        for info in goodbye_fish_list:
            pastR, pastC = info[0][0], info[0][1]
            currentR, currentC = info[1][0], info[1][1]
            currentDir = info[2]

            MAP[currentR][currentC][0][0] +=1
            MAP[currentR][currentC][0][1].append(currentDir)
            MAP[pastR][pastC][0][0] -= 1

    return MAP, old_fishes

# 재귀적으로 구현하기 위한 visited map 등의 각종 변수 선언:
max_fish_count = -1
optimal_path = []
visited = [[False]*4 for _ in range(4)]

def get_shark_routes_with_dfs(MAP, shark_idx, move_count, fish_count, tmp_path):
    global visited, max_fish_count, optimal_path

    if move_count == 3:
        if fish_count > max_fish_count:
            max_fish_count = fish_count
            optimal_path = [d for d in tmp_path]

        elif fish_count == max_fish_count:
            if optimal_path:
                tmp_path_num = 100*(1+tmp_path[0]) + 10 * (1+tmp_path[1]) + (1+tmp_path[2])
                curopt_path_num = 100*(1+optimal_path[0]) + 10 * (1+optimal_path[1]) + (1+optimal_path[2])
                if tmp_path_num < curopt_path_num:
                    optimal_path = [d for d in tmp_path]
        return

    currentR, currentC = shark_idx[0], shark_idx[1]

    for d in range(4):
        tmp_r, tmp_c = currentR+shark_dr[d], currentC+shark_dc[d]
        if 0 <= tmp_r < N and 0 <= tmp_c < N:
            if not visited[tmp_r][tmp_c]:
                visited[tmp_r][tmp_c] = True
                nxt_fish_cnt = fish_count + MAP[tmp_r][tmp_c][0][0]
                get_shark_routes_with_dfs(MAP, [tmp_r, tmp_c], move_count+1, nxt_fish_cnt, tmp_path+[d])
                visited[tmp_r][tmp_c] = False

            else: # 이미 방문한 곳이라면 물고기가 이미 0일 것이므로
                get_shark_routes_with_dfs(MAP, [tmp_r, tmp_c], move_count+1, fish_count, tmp_path+[d])
                 
def move_shark_from_dfs(MAP, shark_idx):
    global optimal_path, max_fish_count
    max_fish_count = -1
    curR, curC = shark_idx[0], shark_idx[1]
    get_shark_routes_with_dfs(MAP, shark_idx, 0, 0, [])
    # print(f"optimal path : {optimal_path}")
    for dir in optimal_path:

        curR, curC = curR+shark_dr[dir], curC+shark_dc[dir]
        # print(f"shark Move! {curR}, {curC}\n")

        if MAP[curR][curC][0][0] != 0:
            MAP[curR][curC][0][0] = 0
            MAP[curR][curC][0][1] = deque()
            MAP[curR][curC][1] = 3 #3?

    shark_idx = [curR, curC]
    return MAP, shark_idx

def cast_duplication(MAP, old_fishes):
    for i in range(len(old_fishes)):
        fishR, fishC, fishD = old_fishes[i][0], old_fishes[i][1], old_fishes[i][2]

        MAP[fishR][fishC][0][0] += 1
        MAP[fishR][fishC][0][1].append(fishD)
    return MAP


def fishSmell_fadeAway(MAP):
    """맨 처음에 넣어주면 될듯"""
    for i in range(4):
        for j in range(4):
            smellArea = MAP[i][j][1]
            if smellArea > 0:
                MAP[i][j][1] -= 1

    return MAP

def main(MAP, shark_idx):
    # print("init MAP")
    # MAP_printer(MAP)
    # print(f"curSharkIdx : {shark_idx}\n")

   

    MAP, old_fishes = fishMove(MAP, shark_idx)
    # print("after fishMove : ")
    # MAP_printer(MAP)
    # print("OLD_MAP : ")
    # MAP_printer(OLD_MAP)

    
    # MAP, shark_idx = move_shark(MAP, shark_idx)
    MAP, shark_idx = move_shark_from_dfs(MAP, shark_idx)
    MAP = fishSmell_fadeAway(MAP)


    # print("after sharkMove :")
    # MAP_printer(MAP)

    MAP = cast_duplication(MAP, old_fishes)
    # print("after duplication :")
    # MAP_printer(MAP)

    return MAP, shark_idx

def get_answer(MAP):
    ans = 0
    for i in range(N):
        for j in range(N):
            fishNum = MAP[i][j][0][0]
            ans += fishNum
    return ans


if __name__ == "__main__":
    MAP, M, S, shark_idx = input_getter()
    for _ in range(S):

        MAP, shark_idx = main(MAP, shark_idx)

    ans = get_answer(MAP)
    print(ans)
