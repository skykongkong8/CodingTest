# 마법사 상어와 복제
import sys

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
    M, S = map(int, sys.stdin.readline().split(' '))

    for _ in range(M):
        r, c, d = map(int, sys.stdin.readline().split(' '))
        MAP[r-1][c-1][0][0] += 1
        MAP[r-1][c-1][0][1].append(d-1)

    shark_r, shark_c = map(int, sys.stdin.readline().split(' '))

    return MAP, M, S, [shark_r-1, shark_c-1]
def fishMove(MAP, shark_idx):
    total_movement_history = []
    # 시간초과이슈 : deepcopy를 제거해보자! deepcopy is actually, 'extremely' slow
    old_fishes = []
    """
    old_fishes = [
        ...
        [r,c,d]
        ...
    ]
    """
    MAP_printer(MAP)
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
                old_fishes.append([curR, curC, curFishDir])
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

    return MAP, old_fishes
# def fishMove(MAP, shark_idx):
#     total_movement_history = []
#     OLD_MAP = deepcopy(MAP)
#     # 시간초과이슈 : deepcopy를 제거해보자! deepcopy is actually, 'extremely' slow
#     old_fishes = []
#     """
#     old_fishes = [
#         ...
#         [r,c,d]
#         ...
#     ]
#     """

#     for i in range(4):
#         for j in range(4):
#             curFishCnt = MAP[i][j][0][0]
#             if curFishCnt == 0:
#                 continue

#             curFishDirList = MAP[i][j][0][1]
#             curR, curC = i,j
#             goodbye_fish_list = []
#             for k in range(curFishCnt):
#                 curFishDir = curFishDirList[k]
#                 old_fishes.append([curR, curC, curFishDir])
#                 for l in range(8):
#                     tmp_r, tmp_c = curR + dr[curFishDir], curC + dc[curFishDir]
#                     if 0 <= tmp_r < N and 0 <= tmp_c < N:
#                         if MAP[tmp_r][tmp_c][1] == 0 and ([tmp_r, tmp_c] != [shark_idx[0], shark_idx[1]]):
#                             # 조건 성립 : 물고기 이동 = 현위치 삭제 + 다음 위치에 삽입
#                             # print(f"fish move from {curR}, {curC} to {tmp_r}, {tmp_c}")
#                             # MAP[tmp_r][tmp_c][0][0] += 1
#                             # MAP[curR][curC][0][0] -= 1
#                             # MAP[tmp_r][tmp_c][0][1].append(curFishDir)

#                             """
#                             goodbye_fish_list = [
#                                 ...
#                                 [[curR, curC], [tmp_r, tmp_c], changedDir, curFishDirList[k], MAP[curR][curC][0][0]] : 물고기 하나당 정보
#                                 ...
#                             ]
#                             """
#                             goodbye_fish_list.append([[curR, curC], [tmp_r, tmp_c], curFishDir, curFishDirList[k], MAP[curR][curC][0][0]])

#                             break

#                     # print(f"cannot move to : {tmp_r}, {tmp_c}")
#                     curFishDir -= 1
#                     if curFishDir < 0:
#                         curFishDir += 8
#             total_movement_history.append(goodbye_fish_list)

#     for goodbye_fish_list in total_movement_history:
#         for info in goodbye_fish_list:
#             pastR, pastC = info[0][0], info[0][1]
#             currentR, currentC = info[1][0], info[1][1]
#             currentDir = info[2]

#             MAP[currentR][currentC][0][0] +=1
#             MAP[currentR][currentC][0][1].append(currentDir)
#             MAP[pastR][pastC][0][0] -= 1

#             pastDir = info[3]
#             MAP[pastR][pastC][0][1].remove(pastDir)

#     return MAP, OLD_MAP

def move_shark(MAP, shark_idx):
    
    curR, curC = shark_idx[0], shark_idx[1]
    # print(f"START MOVE SHARK AT : {curR}, {curC}")
    possible_routes = []
    """
    possible_routes = [
        ...
        [[0,1,1], TotalNumOfFishes]
        ...
    ]
    """

    # DFS 같은걸로 안되지 않나, 모든 경우를 무조건 다해보아야하니까 (최단경로가 아니라)
    optimal_route = [[-1,-1,-1,0],-1] # init은 그냥 전부 해당사항이 없는걸로 맞춰주어야 한다.
    """
    optimal_route = [[j,k,l,RouteNumber], TotalFishNum]

    차라리 sort를 안해도 되게 여기서 필터링을 해보자.
    """
    for j in range(4):
        tmp_r, tmp_c = curR + shark_dr[j], curC + shark_dc[j]
        if 0 <= tmp_r < N and 0 <= tmp_c < N:
            first_fish = MAP[tmp_r][tmp_c][0][0]
            # print(f"direction : {j} | tmp_r : {tmp_r}, tmp_c : {tmp_c}, fish1 : {first_fish}\n")

            for k in range(4):
                tmp_tmp_r, tmp_tmp_c = tmp_r + shark_dr[k], tmp_c + shark_dc[k]
                if 0 <= tmp_tmp_r < N and 0 <= tmp_tmp_c < N:

                    if [tmp_tmp_r, tmp_tmp_c] == [tmp_r, tmp_c] or [tmp_tmp_r, tmp_tmp_c] == [curR, curC]:
                        second_fish = 0
                    else:
                        second_fish = MAP[tmp_tmp_r][tmp_tmp_c][0][0]
                    # print(f"direction : {k} |tmp_tmp_r : {tmp_tmp_r}, tmp_tmp_c : {tmp_tmp_c}, fish2 : {second_fish}\n")

                    for l in range(4):
                        tmp_tmp_tmp_r, tmp_tmp_tmp_c = tmp_tmp_r + shark_dr[l], tmp_tmp_c + shark_dc[l]
                        if 0 <= tmp_tmp_tmp_r < N and 0 <= tmp_tmp_tmp_c < N:

                            if [tmp_tmp_tmp_r, tmp_tmp_tmp_c] == [tmp_tmp_r, tmp_tmp_c] or [tmp_tmp_tmp_r, tmp_tmp_tmp_c] == [tmp_r, tmp_c] or [tmp_tmp_tmp_r, tmp_tmp_tmp_c] == [curR, curC]:
                                third_fish = 0
                            else:
                                third_fish = MAP[tmp_tmp_tmp_r][tmp_tmp_tmp_c][0][0]
                            # print(f"direction : {l} | tmp_tmp_tmp_r : {tmp_tmp_tmp_r}, tmp_tmp_tmp_c : {tmp_tmp_tmp_c}, fish3 : {third_fish}\n")

                            currentRoute = [[j,k,l, (j+1)*100 + (k+1)*10 + (l+1)], first_fish + second_fish + third_fish]
                            """
                            optimal_route = [[j,k,l,RouteNumber], TotalFishNum]

                            차라리 sort를 안해도 되게 여기서 필터링을 해보자.
                            """
                            if optimal_route[1] < currentRoute[1]:
                                optimal_route = currentRoute[:]
                                # print(f"Route update! : {optimal_route}")
                            
                            elif optimal_route[1] == currentRoute[1]:
                                if optimal_route[0][-1] > currentRoute[0][-1]:
                                    optimal_route = currentRoute[:]
                                    # print(f"Route update! : {optimal_route}")



                            possible_routes.append(currentRoute)

    # DFS로 해도 되는 것으로 판명났다. 아마 여기를 알고리즘적으로 해결하지 않고 BruteForce로 해결해서 시간 초과가 뜬 것 같다.
    # Brute Force로 하면 탐색도 오래걸리고, 추후 sort도 해줘야 하므로 두배로 시간이 오래 걸린다 ->-> sort를 미리 필터링 업데이트를 통해 해결하자

    # 왜? 그리고 어떻게?

    print(f"optimal_route {optimal_route[0][:-1]}")


    # possible_routes.sort(key= lambda a : (-a[1], a[0][3]))
    # optimal_route = possible_routes[0][0][:-1]
    # print(f"actual_optimal_route : {optimal_route}\n")
    optimal_route = optimal_route[0][:-1]

    # 상어의 움직임 : 움직인 칸마다 = 물고기 0 + 물고기 냄새
    # print(f"possibles : {possible_routes}")
    # print(f"shark will move like: {possible_routes[0][0]}")
    for dir in optimal_route:
        curR, curC = curR+shark_dr[dir], curC+shark_dc[dir]
        # print(f"shark Move! {curR}, {curC} with direction {dir}\n")

        if MAP[curR][curC][0][0] != 0:
            MAP[curR][curC][0][0] = 0
            MAP[curR][curC][0][1] = []
            MAP[curR][curC][1] = 2 #3?

    shark_idx = [curR, curC]
    return MAP, shark_idx

# def cast_duplication(MAP, OLD_MAP):
#     for i in range(4):
#         for j in range(4):
#             if OLD_MAP[i][j][0][0] != 0:
#                 MAP[i][j][0][0] += OLD_MAP[i][j][0][0]
#                 MAP[i][j][0][1].extend(OLD_MAP[i][j][0][1])
#     return MAP

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

    MAP = fishSmell_fadeAway(MAP)
    
    MAP, shark_idx = move_shark(MAP, shark_idx)
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
            if fishNum != 0:
                ans += fishNum
    return ans


if __name__ == "__main__":
    MAP, M, S, shark_idx = input_getter()
    for _ in range(S):

        MAP, shark_idx = main(MAP, shark_idx)

    ans = get_answer(MAP)
    print(ans)

"""
배운점 :

1. N차원 리스트 자료구조에 모든 것을 담으려 하면 메모리가 꼬이는 일이 발생할 수 있다.
    깊이가 깊은 메모리를 하나하나 참조하여 접근하거나, 복사하는 것 자체가 연산량이 많이 드는 작업이다.
    따라서, 다차원의 리스트를 만드는 것은 최대 2,3차원까지가 적당하고 그 이상은 다른 1,2차원의 보조 자료구조를
    생성하는 것이 바람직하다.


"""