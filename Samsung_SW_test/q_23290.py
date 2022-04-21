# 마법사 상어와 복제
from copy import deepcopy

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
MAP = [
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]],
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]], 
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]], 
    [[[0, []], 0], [[0, []], 0], [[0, []], 0], [[0, []], 0]]

]
        

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
    OLD_MAP = deepcopy(MAP)
    for i in range(4):
        for j in range(4):
            curFishCnt = MAP[i][j][0][0]
            if curFishCnt == 0:
                continue

            curFishDirList = MAP[i][j][0][1]
            curR, curC = i,j
            goodbye_fish_list = []
            for k in range(curFishCnt):
                curFishDir = curFishDirList[k]
                for l in range(8):
                    tmp_r, tmp_c = curR + dr[curFishDir], curC + dc[curFishDir]
                    if 0 <= tmp_r < N and 0 <= tmp_c < N:
                        if MAP[tmp_r][tmp_c][1] == 0 and ([tmp_r, tmp_c] != [shark_idx[0], shark_idx[1]]):
                            # 조건 성립 : 물고기 이동 = 현위치 삭제 + 다음 위치에 삽입
                            # print(f"fish move from {curR}, {curC} to {tmp_r}, {tmp_c}")
                            # MAP[tmp_r][tmp_c][0][0] += 1
                            # MAP[curR][curC][0][0] -= 1
                            # MAP[tmp_r][tmp_c][0][1].append(curFishDir)

                            """
                            goodbye_fish_list = [
                                ...
                                [[curR, curC], [tmp_r, tmp_c], changedDir, curFishDirList[k], MAP[curR][curC][0][0]] : 물고기 하나당 정보
                                ...
                            ]
                            """
                            goodbye_fish_list.append([[curR, curC], [tmp_r, tmp_c], curFishDir, curFishDirList[k], MAP[curR][curC][0][0]])

                            break

                    # print(f"cannot move to : {tmp_r}, {tmp_c}")
                    curFishDir -= 1
                    if curFishDir < 0:
                        curFishDir += 8
            total_movement_history.append(goodbye_fish_list)

    for goodbye_fish_list in total_movement_history:
        for info in goodbye_fish_list:
            pastR, pastC = info[0][0], info[0][1]
            currentR, currentC = info[1][0], info[1][1]
            currentDir = info[2]

            MAP[currentR][currentC][0][0] +=1
            MAP[currentR][currentC][0][1].append(currentDir)
            MAP[pastR][pastC][0][0] -= 1

            pastDir = info[3]
            MAP[pastR][pastC][0][1].remove(pastDir)

    return MAP, OLD_MAP

def move_shark(MAP, shark_idx):
    curR, curC = shark_idx[0], shark_idx[1]
    possible_routes = []
    """
    possible_routes = [
        ...
        [[0,1,1], TotalNumOfFishes]
        ...
    ]
    """
    
    # DFS 같은걸로 안되지 않나, 모든 경우를 무조건 다해보아야하니까 (최단경로가 아니라)
    for j in range(4):
        tmp_r, tmp_c = curR + shark_dr[j], curC + shark_dc[j]
        if 0 <= tmp_r < N and 0 <= tmp_c < N:
            first_fish = MAP[tmp_r][tmp_c][0][0]
            for k in range(4):
                tmp_tmp_r, tmp_tmp_c = tmp_r + shark_dr[k], tmp_c + shark_dc[k]
                if 0 <= tmp_tmp_r < N and 0 <= tmp_tmp_c < N:
                    if [tmp_tmp_r, tmp_tmp_c] == [tmp_r, tmp_c]:
                        second_fish = 0
                    else:
                        second_fish = MAP[tmp_tmp_r][tmp_tmp_c][0][0]
                    for l in range(4):
                        tmp_tmp_tmp_r, tmp_tmp_tmp_c = tmp_tmp_r + shark_dr[l], tmp_tmp_c + shark_dc[l]
                        if 0 <= tmp_tmp_tmp_r < N and 0 <= tmp_tmp_tmp_c < N:
                            if [tmp_tmp_tmp_r, tmp_tmp_tmp_c] == [tmp_tmp_r, tmp_tmp_c] or [tmp_tmp_tmp_r, tmp_tmp_tmp_c] == [tmp_r, tmp_c]:
                                third_fish = 0
                            else:
                                third_fish = MAP[tmp_tmp_tmp_r][tmp_tmp_tmp_c][0][0]

                            currentRoute = [[j,k,l, (j+1)*100 + (k+1)*10 + (l+1)], first_fish + second_fish + third_fish]
                            possible_routes.append(currentRoute)
    
    possible_routes.sort(key= lambda a : (-a[1], a[0][3]))
    optimal_route = possible_routes[0][0][:-1]

    # 상어의 움직임 : 움직인 칸마다 = 물고기 0 + 물고기 냄새
    # print(f"possibles : {possible_routes}")
    # print(f"shark will move like: {possible_routes[0][0]}")
    for dir in optimal_route:
        curR, curC = curR+shark_dr[dir], curC+shark_dc[dir]
        # print(f"shark Move! {curR}, {curC}\n")

        if MAP[curR][curC][0][0] != 0:
            MAP[curR][curC][0][0] = 0
            MAP[curR][curC][0][1] = []
            MAP[curR][curC][1] = 2 #3?

    shark_idx = [curR, curC]
    return MAP, shark_idx

def cast_duplication(MAP, OLD_MAP):
    for i in range(4):
        for j in range(4):
            if OLD_MAP[i][j][0][0] != 0:
                MAP[i][j][0][0] += OLD_MAP[i][j][0][0]
                MAP[i][j][0][1].extend(OLD_MAP[i][j][0][1])
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

   

    MAP, OLD_MAP = fishMove(MAP, shark_idx)
    # print("after fishMove : ")
    # MAP_printer(MAP)
    # print("OLD_MAP : ")
    # MAP_printer(OLD_MAP)

    MAP = fishSmell_fadeAway(MAP)
    
    MAP, shark_idx = move_shark(MAP, shark_idx)
    # print("after sharkMove :")
    # MAP_printer(MAP)

    MAP = cast_duplication(MAP, OLD_MAP)
    # print("after duplication :")
    # MAP_printer(MAP)

    return MAP, shark_idx

def get_answer(MAP):
    ans = 0
    for i in range(N):
        for j in range(N):
            fishNum = MAP[i][j][0][0]
            if fishNum != 0:
                ans += fishNum
    return ans


if __name__ == "__main__":
    MAP, M, S, shark_idx = input_getter()
    for _ in range(S):

        MAP, shark_idx = main(MAP, shark_idx)

    ans = get_answer(MAP)
    print(ans)
