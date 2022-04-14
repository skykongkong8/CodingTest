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

    shark_init_direction_dict = {}
    for i in range(M):
        shark_init_direction_dict[i+1] = sharks_init_direction[i]

    sharks_init_direction = shark_init_direction_dict


    for _ in range(M):
        this_sharks_priority = []
        
        for i in range(4):
            this_sharks_this_directions_priority = list(map(int, input().split(' ')))
            this_sharks_priority.append(this_sharks_this_directions_priority)
        sharks_priority.append(this_sharks_priority)

    return N, M, k, MAP, sharks_init_direction, sharks_priority, sharks_position, PERFUME_MAP

def shark_init(PERFUME_MAP, sharks_position, k, sharks_init_direction):
    """1초가 되기 전, 자기 위치에 냄새를 뿌린다. PERFUME_MAP에 한다. 최초 1회만 사용되는 함수
    sharks_position = {
        sharkNum : [r, c, dir]
    }

    PERFUME_MAP = [
        ...
        [[0,0],[0,0],[0,0],[sharkNum, t], [0,0], [0,0]]
        ...
    ]

    perfumes_position = {
        ...
        sharkNum : [[r,c,t]. [r,c,t], ...]
        ...
    }

    MAP = [
        ...
        [0,0,0,0,2,0]
        ...
    ]
    """
    perfumes_position = {}
    for sharkNum, sharkPos in zip(sharks_position.keys(), sharks_position.values()):
        sharks_position[sharkNum] = [sharks_position[sharkNum][0],sharks_position[sharkNum][1], sharks_init_direction[sharkNum]]
        r,c = sharkPos[0], sharkPos[1]
        PERFUME_MAP[r][c] = [sharkNum,k]
        perfumes_position[sharkNum] = [[r,c,k]]
        
    return PERFUME_MAP, perfumes_position

def move_shark(sharks_position, MAP, PERFUME_MAP, perfumes_position, N, k, sharks_priority):
    """
    1초마다 실행되는 함수 - 상어를 그때에 맞는 적절한 인덱스로 이동시키고  (좌표를 옮긴 후, 방향을 변경한다.), 중복된 상어처리를 한다.
    이때, 중복처리를 shark_positions의 딕셔너리에서 중복을 확인한 후 최종 남은 상어를 MAP (상어의 MAP)에 처리해주는 것으로 하자.

    또한 상어냄새또한 처리해주어야 한다. 각 칸에 있는 상어 냄새들이 1초마다 1씩 감소되도록 하여야하는데, 이때문에 굳굳이 PERFUME_INDEX를 만들어야할까??
    만들어주지뭐 : PERFUME_INDEX는 딕셔너리이며, 각 상어번호별 남아있는 냄새의 정보가 담겨있다. {1 : [[r,c], t], ...}의 꼴
    
    sharks_position = {
        sharkNum : [r, c, dir]
    }

    PERFUME_MAP = [
        ...
        [[0,0],[0,0],[0,0],[sharkNum, t], [0,0], [0,0]]
        ...
    ]

    perfumes_position = {
        ...
        sharkNum : [[r,c,t], [r,c,t], ...]
        ...
    }
    """
    #  init으로부터 시간이 1초 지났음 및 시간 지남에 따른 냄새 약화/사라짐
    perShark_overTimePerfumeIndixies = {}
    for sharkNum, perfumePosList in zip(perfumes_position.keys(), perfumes_position.values()):
        overTimePerfumeIndixies = []
        for i in range(len(perfumePosList[:])):
            perfumePos = perfumePosList[i]
            curPosTime = perfumePos[2]
            curPosR, curPosC = perfumePos[0], perfumePos[1]

            if curPosTime == 0 or PERFUME_MAP[curPosR][curPosC][1] == 0:
                # perfumes_position[sharkNum].remove(perfumePos)
                overTimePerfumeIndixies.append([sharkNum, perfumePos])
                PERFUME_MAP[curPosR][curPosC][0] = 0
            else:
                perfumes_position[sharkNum][i][2] -= 1
                PERFUME_MAP[curPosR][curPosC][1] -= 1 

        perShark_overTimePerfumeIndixies[sharkNum] = overTimePerfumeIndixies

        # for data in overTimePerfumeIndixies:
            # perfumes_position[data[0]].remove(data[1])


    # for row in PERFUME_MAP:
    #     print(row)
    # print()

    # 상어 움직임 - 아직 MAP이나 PERFUME_MAP에 반영하지 않는다.
    tmp_cur_position = {}
    for sharkNum, sharkPos in zip(sharks_position.keys(), sharks_position.values()):
        cur_r, cur_c, cur_dir = sharkPos[0], sharkPos[1], sharkPos[2]
        cur_priority = sharks_priority[sharkNum-1]
        tmp_cur_position[sharkNum] = [cur_r, cur_c]
       
        print(f"cur_r : {cur_r}, cur_c : {cur_c}, sharknum : {sharkNum}, cur_dir : {cur_dir}, tmp_cur_position = {tmp_cur_position}\n")
        for p in cur_priority:
            print(p)
        print()
        
        opt_r, opt_c, opt_dir = calculate_prioritized_indicies(cur_r, cur_c, sharkNum, cur_dir, cur_priority, N, PERFUME_MAP)

        sharks_position[sharkNum] = [opt_r, opt_c, opt_dir]
        
        # 이미 방문하였던 position이라면, 새로 추가할시 중복되서 빠지게 됨! 이것도 dict으로 했어야 하네...
        # 억지로 방문하였었던 것인지 찾아주자. 근데 k가 껴있어서 킹받음
        isVisited = False

        for p in range(len(perfumes_position[sharkNum])):
            currentPerfumePosition = perfumes_position[sharkNum][p]

            if currentPerfumePosition[0] == opt_r and currentPerfumePosition[1] == opt_c:
                isVisited = True
                perfumes_position[sharkNum][p][2] = k

        if not isVisited:
            perfumes_position[sharkNum].append([opt_r, opt_c, k])

    
    # 중복 상어 처리 : sharks_position을 돌면서 중복된 인덱스가 있는지 확인한다. 이때 위치+방향/냄새도 최종적으로 MAP에 반영해준다.
    """
    goodbye_sharks = [ [r,c, N], ...]
    """
    goodbye_sharks = []

    for strongerSharks in sharks_position.keys():
        OriginalSharkIndex = [sharks_position[strongerSharks][0],sharks_position[strongerSharks][1]]
        for weakerSharks in sharks_position.keys():
            if strongerSharks < weakerSharks: # 번호가 작을 수록 강함 + 같아서는 안됨
                ComparingSharkIndex = [sharks_position[weakerSharks][0], sharks_position[weakerSharks][1]]
                print(f"comparing... {strongerSharks} in {OriginalSharkIndex} and {weakerSharks} in {ComparingSharkIndex}\n")
                if OriginalSharkIndex == ComparingSharkIndex:
                    print("WARNING : multiple sharks!\n")
                    # 중복이 있으면 무조건 i가 작으므로 i가 우선, j가 제거 대상이다. i는 MAP들에 직접 반영해주고 j는 영구제거된다.
                    # goodbye_sharks.append([sharks_position[j][0], sharks_position[j][1],j])
                    
                    goodbye_sharks.append(weakerSharks)

    """for i in range(1, M): # 1, 2, 3
        OriginalSharkIndex = [sharks_position[i][0],sharks_position[i][1]]
        for j in range(i+1, M+1): #2, 3, 4/ 3, 4/ 4
            ComparingSharkIndex = [sharks_position[j][0], sharks_position[j][1]]
            print(f"comparing... {i} in {OriginalSharkIndex} and {j} in {ComparingSharkIndex}\n")
            if OriginalSharkIndex == ComparingSharkIndex:
                print("WARNING : multiple sharks!\n")
                # 중복이 있으면 무조건 i가 작으므로 i가 우선, j가 제거 대상이다. i는 MAP들에 직접 반영해주고 j는 영구제거된다.
                # goodbye_sharks.append([sharks_position[j][0], sharks_position[j][1],j])
                goodbye_sharks.append(j)"""


    # 제거
    print(f"sharks to be deleted : {goodbye_sharks}\n")
    for goodbye_shark in goodbye_sharks:
        del sharks_position[goodbye_shark]
        old_r, old_c = tmp_cur_position[goodbye_shark][0], tmp_cur_position[goodbye_shark][1]
        MAP[old_r][old_c] = 0
        
        
        # 근데 사실 MAP은 전체 초기화해도 상관없지않나?
        #PERFUME_MAP, perfumes_position에서는 지울 필요 없다.
    
    # 반영
    for sharkNum, sharkPos in zip(sharks_position.keys(), sharks_position.values()):
        cur_r, cur_c, cur_dir = sharkPos[0], sharkPos[1], sharkPos[2]
        MAP[cur_r][cur_c] = sharkNum
        PERFUME_MAP[cur_r][cur_c] = [sharkNum, k]

        old_r, old_c = tmp_cur_position[sharkNum][0], tmp_cur_position[sharkNum][1]
        MAP[old_r][old_c] = 0

    for SharkNum in perShark_overTimePerfumeIndixies.keys():
        current_overTimePerfumeIndicies = perShark_overTimePerfumeIndixies[SharkNum]
        for data in current_overTimePerfumeIndicies:
            perfumes_position[data[0]].remove(data[1])

    return MAP, PERFUME_MAP, sharks_position, perfumes_position

def calculate_prioritized_indicies(currentR, currentC, currentSharkNumber, currentDirection, currentPriority, N, PERFUME_MAP):
    """현재 상어가 이동할 다음 칸 중 가장 최우선 순위인 인덱스를 반환함"""
    # 기준 1 : 아무 냄새가 없는 칸
    nothing_index_list = []
    my_odor_list = []
    for j in range(4):
        tmp_r, tmp_c = currentR + dr[j], currentC + dc[j]
        if 0 <= tmp_r < N and 0 <= tmp_c < N:
            if PERFUME_MAP[tmp_r][tmp_c][0] == 0:
                nothing_index_list.append([tmp_r, tmp_c])

            elif PERFUME_MAP[tmp_r][tmp_c][0] == currentSharkNumber:
                my_odor_list.append([tmp_r, tmp_c])
    
    num_nothing_index_candidates = len(nothing_index_list)

    print(f"possible empty index : {nothing_index_list}\n")
    print(f"possible myOdor index : {my_odor_list}\n")


    if num_nothing_index_candidates >= 1:
        if num_nothing_index_candidates == 1:
            if_one_dir = [nothing_index_list[0][0]-currentR, nothing_index_list[0][1]-currentC]
            if_one_dir = directionHasher(if_one_dir)
            print(f"singular index : {[nothing_index_list[0][0], nothing_index_list[0][1]]}\n")
            return nothing_index_list[0][0], nothing_index_list[0][1], if_one_dir

        else:
            print("WARNING : multiple roots!\n")
            opt_r, opt_c, opt_dir = select_best_prioritized_index(currentPriority, currentDirection, nothing_index_list, currentR, currentC, currentSharkNumber)
            return opt_r, opt_c, opt_dir
            

    # 기준 2: 1이 없으면 자신의 냄새가 있는 칸으로
    num_my_odor_index_candidates = len(my_odor_list)

    if num_my_odor_index_candidates >= 1:
        if num_my_odor_index_candidates == 1:
            if_one_dir = [my_odor_list[0][0]-currentR, my_odor_list[0][1]-currentC]
            if_one_dir = directionHasher(if_one_dir)
            print(f"singular index : {[my_odor_list[0][0], my_odor_list[0][1]]}\n")
            return my_odor_list[0][0], my_odor_list[0][1], if_one_dir

        else:
            print("WARNING : multiple roots!\n")
            opt_r, opt_c, opt_dir = select_best_prioritized_index(currentPriority, currentDirection, my_odor_list, currentR, currentC, currentSharkNumber)
            return opt_r, opt_c, opt_dir

def select_best_prioritized_index(currentPriority, currentDirection, index_list, currentR, currentC, currentSharkNumber):
    """중복이 되는 인덱스가 있을 때 각 상어별 최우선순위인것을 선택함"""
    currentPriorityOrder = currentPriority[currentDirection-1]
    prioritized_indicies_inorder = []
    print(f"priority order of Shark #{currentSharkNumber}'s direction {currentDirection} is {currentPriorityOrder}\n")

    for index in index_list:
        currentIndexDirection = [index[0]-currentR, index[1]-currentC]
        hashedDirection = directionHasher(currentIndexDirection)

        prioritized_indicies_inorder.append([currentPriorityOrder.index(hashedDirection), [index, hashedDirection]])
        print(f"to be sorted... {[currentPriorityOrder.index(hashedDirection), [index, hashedDirection]]}")

    prioritized_indicies_inorder.sort(key = lambda a : a[0])
    optimal_index = prioritized_indicies_inorder[0]
    print(f"optimal_index : {optimal_index}")

    return optimal_index[1][0][0], optimal_index[1][0][1], optimal_index[1][1]
     

def get_next_index_and_direction():
    """
    상어가 가야할 다음 인덱스와 방향을 반환하는 함수
    기준1, 기준2에 따라 판별하며 중복처리가 있을 경우 각각에 대해 처리해야 한다.
    choose_optimal_index에서 반환하거나 한 하나의 인덱스와 현재의 인덱스로 방향을 찾을 수 있다.
    """

def choose_optimal_index():
    """
    get_next_index에서 중복이 나왔을 경우 상어번호별+방향별 우선순위별로 optimal index를 반환하는 함수
    """


def directionHasher(hashingIndex):
    """
    두 인덱스의 차에서 얻은 방향을 다시 1,2,3,4의 방향인덱스로 변환하여주는 함수
    """
    direction_dict = {
        (-1,0) : 1,
        (1,0) : 2,
        (0,-1) : 3,
        (0,1) : 4
    }
    return direction_dict[tuple(hashingIndex)]


if __name__ == "__main__":
    N, M, k, MAP, sharks_init_direction, sharks_priority, sharks_position, PERFUME_MAP = input_getter()
    """
    N : 전체 MAP의 한 변 길이 (크기)
    M : 전체 상어의 수
    k : 상어 냄새가 없어지기까지의 딜레이 시간
    MAP : 상어의 위치를 알려주는 MAP
    sharks_priority = [각 상어별로 구분되어 있으며, [상어별 번호-1] 접근 후에는 방향 상하좌우별  개별 우선순위가 순서대로 저장되어 있음]
    sharks_position {dict}= 상어별 번호-1 index에 각 상어의 MAP에서 위치가 explicit하게 저장되어 있음
    shark_direction {dict} = {
        sharkNum : sharkDirectionIndex
    }
    PERFUME_MAP = MAP이랑 똑같은 구조에 다음의 object들의 저장되어있음 : [냄새남긴상어의 번호, 남은 시간]
    """

    PERFUME_MAP, perfumes_position = shark_init(PERFUME_MAP, sharks_position, k, sharks_init_direction)
    time_step = 0
    answer = -1
    flag = False
    for t in range(1000):
        print("_______________________________")
        print(f"ABOVE THE LINE IS ON THE CURRENT TIME CLOCK : {time_step}\n")
        for row in MAP:
            print(row)
        print()
        for row in PERFUME_MAP:
            print(row)
        print()
        print("_______________________________")

        MAP, PERFUME_MAP, sharks_position, perfumes_position = move_shark(sharks_position, MAP, PERFUME_MAP, perfumes_position, N, k, sharks_priority)

        time_step += 1

        current_shark_left = len(sharks_position.keys())

        if current_shark_left == 1:
            flag = True
            break

    if flag:
        answer = time_step

    # for row in MAP:
    #     print(row)
    # print()
    # for row in PERFUME_MAP:
    #     print(row)
    # print()
    # print(sharks_position)
    # print()
    # print(sharks_priority)
    # print()
    
    print(answer)

"""
그래도 배운것은...
1. 디버깅... print로 인내심을 가지고 하면 어느정도는 다 할 수 있다. (한 번 할때 정성들여 쓰자)
2. dict의 유용성 -> keyvalue라는게 워낙 유용함
3. dict key로 tuple()써주면 된다. list로 input하고 싶으면
4. 
"""