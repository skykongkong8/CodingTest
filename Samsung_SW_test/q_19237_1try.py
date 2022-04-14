# 어른 상어

dr = [-1,1,0,0] # 이번 문제의 방향 순서 인덱스
dc = [0,0,-1,1]

def input_getter():
    N, M, k = map(int, input().split(' '))
    MAP = []
    PERFUME_MAP = [[[0,0]]*N for _ in range(N)]
    sharks_priority = []
    # sharks_position = [0]*M
    sharks_position = {}

    for _ in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)
    
    for i in range(N):
        for j in range(N):
            if MAP[i][j] !=  0:
                # sharks_position[MAP[i][j]-1] = [i,j]
                sharks_position[MAP[i][j]] = [i,j]


    sharks_init_direction = list(map(int, input().split(' ')))

    for _ in range(M):
        this_sharks_priority = []
        
        for i in range(4):
            this_sharks_this_directions_priority = list(map(int, input().split(' ')))
            this_sharks_priority.append(this_sharks_this_directions_priority)
        sharks_priority.append(this_sharks_priority)

    return N, M, k, MAP, sharks_init_direction, sharks_priority, sharks_position, PERFUME_MAP



def move_sharks(N, M, k, MAP, sharks_direction, sharks_priority, sharks_position, PERFUME_MAP,defeated_sharkCnt):
    """상어들을 움직이고 냄새를 뿌리는 함수"""
    #1 자기 위치에 냄새(  [번호, 남은시간]  )를 뿌린다. (냄새들의 인덱스 역시 움직일 때마다 후처리를 해줘야 하므로 기억해야 함)
    
    # for i in range(len(sharks_position.keys())):
    for i in sharks_position.keys():
        curR, curC = sharks_position[i][0], sharks_position[i][1]
        curSharkNum = MAP[curR][curC]
        PERFUME_MAP[curR][curC][0], PERFUME_MAP[curR][curC][1] = curSharkNum, k

        #2 이동 기준에 따라 이동 후 냄새를 뿌린다. 이때 중복시 냄새가 우선순위대로 dominant + 방향 업데이트 -> calculate_prioritized_indicies
        curD = sharks_direction[curSharkNum-1]
        curPriority = sharks_priority[curSharkNum-1]
        opt_r, opt_c = calculate_prioritized_indicies(curR, curC, curSharkNum, curD, curPriority, N, PERFUME_MAP)

        MAP[curR][curC] = 0

        #3 이동하는 중, 상어가 중복되었을 경우의 처리 및 남아있는 상어 현황 반환하면 좋을 듯 (정답을 위해서)
        if MAP[opt_r][opt_c] != 0:
            alreadySharkNum = MAP[opt_r][opt_c]

            finalSharkNum = min(alreadySharkNum, curSharkNum)
            defeatedSharkNum = max(alreadySharkNum, curSharkNum) 

            MAP[opt_r][opt_c] = finalSharkNum
            defeated_sharkCnt += 1
            PERFUME_MAP[opt_r][opt_c][0], PERFUME_MAP[opt_r][opt_c][1] = finalSharkNum, k

            del sharks_position[defeatedSharkNum]

        else:    
            MAP[opt_r][opt_c] = curSharkNum
            PERFUME_MAP[opt_r][opt_c][0], PERFUME_MAP[opt_r][opt_c][1] = curSharkNum, k

    return defeated_sharkCnt, MAP, sharks_direction, sharks_position, PERFUME_MAP
        

def perfume_map_processing(PERFUME_MAP, N):
    for l in range(N):
        for k in range(N):
            if PERFUME_MAP[l][k][0] != 0:
                if PERFUME_MAP[l][k][1] > 0:
                    PERFUME_MAP[l][k][1] -= 1
                else:
                    PERFUME_MAP[l][k][0], PERFUME_MAP[l][k] = 0,0
    return PERFUME_MAP

def calculate_prioritized_indicies(currentR, currentC, currentSharkNumber, currentDirection, currentPriority, N, PERFUME_MAP):
    """현재 상어가 이동할 다음 칸 중 가장 최우선 순위인 인덱스를 반환함"""
    # 기준 1 : 아무 냄새가 없는 칸
    nothing_index_list = []
    my_odor_list = []
    for j in range(4):
        tmp_r, tmp_c = currentR + dr[j], currentC + dc[j]
        if 0 <= tmp_r < N and 0 <= tmp_c < N:
            if PERFUME_MAP[tmp_r][tmp_c] == 0:
                nothing_index_list.append([tmp_r, tmp_c])

            elif PERFUME_MAP[tmp_r][tmp_c] == currentSharkNumber:
                my_odor_list.append([tmp_r, tmp_c])
    
    num_nothing_index_candidates = len(nothing_index_list)

    if num_nothing_index_candidates >= 1:
        if num_nothing_index_candidates == 1:
            return nothing_index_list[0][0], num_nothing_index_candidates[0][1]

        else:
            opt_r, opt_c = select_best_prioritized_index(currentPriority, currentDirection, nothing_index_list, currentR, currentC)
            return opt_r, opt_c
            

    # 기준 2: 1이 없으면 자신의 냄새가 있는 칸으로
    num_my_odor_index_candidates = len(my_odor_list)

    if num_my_odor_index_candidates >= 1:
        if num_my_odor_index_candidates == 1:
            return my_odor_list[0][0], my_odor_list[0][1]

        else:
            opt_r, opt_c = select_best_prioritized_index(currentPriority, currentDirection, my_odor_list, currentR, currentC)
            return opt_r, opt_c

def select_best_prioritized_index(currentPriority, currentDirection, index_list, currentR, currentC):
    """중복이 되는 인덱스가 있을 때 각 상어별 최우선순위인것을 선택함"""
    currentPriorityOrder = currentPriority[currentDirection-1]
    prioritized_indicies_inorder = []

    for index in index_list:
        currentIndexDirection = [index[0]-currentR, index[1]-currentC]
        hashedDirection = directionHasher(currentIndexDirection)

        prioritized_indicies_inorder.append([currentPriorityOrder.index(hashedDirection), index])

    prioritized_indicies_inorder.sort(key = lambda a : a[0])
    optimal_index = prioritized_indicies_inorder[1]

    return optimal_index[0], optimal_index[1]


def directionHasher(hashingIndex):
    direction_dict = {
        (-1,0) : 1,
        (1,0) : 2,
        (0,-1) : 3,
        (0,1) : 4
    }
    return direction_dict[tuple(hashingIndex)]


if __name__ == "__main__":
    N, M, k, MAP, sharks_direction, sharks_priority, sharks_position, PERFUME_MAP = input_getter()
    """
    N : 전체 MAP의 한 변 길이 (크기)
    M : 전체 상어의 수
    k : 상어 냄새가 없어지기까지의 딜레이 시간
    MAP : 상어의 위치를 알려주는 MAP
    sharks_priority = [각 상어별로 구분되어 있으며, [상어별 번호-1] 접근 후에는 방향 상하좌우별  개별 우선순위가 순서대로 저장되어 있음]
    sharks_position = 상어별 번호-1 index에 각 상어의 MAP에서 위치가 explicit하게 저장되어 있음
    PERFUME_MAP = MAP이랑 똑같은 구조에 다음의 object들의 저장되어있음 : [냄새남긴상어의 번호, 남은 시간]
    """
    defeated_sharkCnt = 0
    time_step = 0
    flag = False
    answer = -1

    for t in range(1000):
        defeated_sharkCnt, MAP, sharks_direction, sharks_position, PERFUME_MAP = move_sharks(N, M, k, MAP, sharks_direction, sharks_priority, sharks_position, PERFUME_MAP,defeated_sharkCnt)

        PERFUME_MAP = perfume_map_processing(PERFUME_MAP, N)

        for row in PERFUME_MAP:
            print(row)
        print()

        time_step += 1

        if defeated_sharkCnt >= M-1:
            flag = True
            break

    if flag:
        answer = time_step

    print(answer)


    
    
    
