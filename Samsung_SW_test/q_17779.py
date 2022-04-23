# 게리맨더링2
from collections import deque

"""
connected component를 구하는 것 까지는 좋은데, 선거구 5를 구하면 나머지는 deterministic하게 정해지는 상황을 보자.
따라서 x, y, d_1, d_2를 정하면 자동적으로 모든 것이 정해진다. 그러한 x,y,d_1,d_2를 잘 구해보아야 하는 것인데:

1. 최솟값인 상황을 정해서 찾기 : 최적화가 되지 않을 문제가 발생할 수 있다 -> 왜냐하면 '인구'니까. 인구는 매번 바뀐다. 기하적으로 해결할수X
2. 최솟값을 탐색 알고리즘으로 찾기 : DFS BFS로 이걸 어떻게 해야할지 감이 안온다...
3. 전부다 해본 후 비교하기 : 코스트가 폭발할 것이다.

다해볼수밖에 없지 않을까? 인구가 랜덤하게 주어지는 경우에 따라 완전히 다를 것이다.
"""
dr = [0,0,-1,1]
dc = [1,-1,0,0]

leftDown = [1,-1]
rightDown = [1,1]

def make_groupFive(BLANK_MAP, x, y, d_1, d_2, N):
    """선거구 5를 형성하는 함수: 이후 선거구 5의 모든 칸 인덱스 정보를 담고 있는 GroupIndexList를 반환"""
    """
    GroupIndexList= [[edgeIndicies], [ALLIndicies] ]
    """
    x -=1
    y -=1
    
    edgeIndicies = [
        [x,y], # UP -> 1
        [x+d_1, y-d_1], # LEFT -> 3
        [x+d_2, y+d_2], # RIGHT -> 2
        [x+d_1+d_2, y+d_2-d_1] # DOWN -> 4
    ]
    # x,y에서부터 :
    curR, curC = x,y
    ALLIndicies = [[x,y]]

    #1 좌하단
    for d in range(d_1):
        curR, curC = curR+leftDown[0], curC+leftDown[1]
        ALLIndicies.append([curR, curC])

    #2 우하단
    curR, curC = x,y
    for d in range(d_2):
        curR, curC = curR+rightDown[0], curC+rightDown[1]
        ALLIndicies.append([curR, curC])

    # 좌하단으로부터:
    #3 우하단
    curR, curC = edgeIndicies[1][0], edgeIndicies[1][1]
    for d in range(d_2):
        curR, curC = curR + rightDown[0], curC + rightDown[1]
        ALLIndicies.append([curR, curC])

    # 우하단으로부터:
    #4 좌하단
    curR, curC = edgeIndicies[2][0], edgeIndicies[2][1]
    for d in range(d_1-1): # 마지막 하나가 중복됨
        curR, curC = curR + leftDown[0], curC + leftDown[1]
        ALLIndicies.append([curR, curC])

    # print(f"ALLIndicies : {ALLIndicies}\n")

    # 이렇게 각 선분을 형성한 뒤 내부를 DFS로 채워서 정해주고,
    # 나머지는 꼭짓점으로부터 각각의 방향 직선으로 그어준 다음 그 안에서 DFS하면 구획선정이 다 될 듯!
    # 아이디어 2 : 여기서는 경계만 칠해주고,  DFS를 돌면서 인구를 세면 훨씬 효율적이다.
    GroupFiveIndexList = [edgeIndicies, ALLIndicies]

    for index in ALLIndicies:
        r, c = index[0], index[1]
        BLANK_MAP[r][c] = 5


    # 하드코딩하자:
    #Group1 up from edge[0], + right from x+d1,0
    upAndLeft = edgeIndicies[0]
    up_r, up_c = upAndLeft[0], upAndLeft[1]
    left_r, left_c = edgeIndicies[1][0]-1, edgeIndicies[1][1]+1
    while True:
        up_r, up_c = up_r - 1, up_c
        if isInLine(up_r, up_c, N):
            BLANK_MAP[up_r][up_c] = 1
        else:
            break

    while True:      
        left_r, left_c = left_r, left_c - 1  
        if isInLine(left_r, left_c, N) and BLANK_MAP[left_r][left_c] != 5:
            BLANK_MAP[left_r][left_c] = 1
        else:
            break
        

     # Group 3 :        
    leftAndUP = edgeIndicies[1]
    left_r, left_c = leftAndUP[0], leftAndUP[1]
    down_r, down_c = edgeIndicies[3][0] -1 , edgeIndicies[3][1] -1 

    while True:
        down_r, down_c = down_r + 1, down_c
        if isInLine(down_r, down_c, N) and BLANK_MAP[down_r][down_c] != 5:
            BLANK_MAP[down_r][down_c] = 3
        else:
            break
        
    while True:
        left_r, left_c = left_r, left_c - 1
        if isInLine(left_r, left_c, N) and BLANK_MAP[left_r][left_c] != 5:
            BLANK_MAP[left_r][left_c] = 3
        else:
            break
    
    # Group 4
    rightAndDown = edgeIndicies[3]
    down_r, down_c = rightAndDown[0], rightAndDown[1]
    right_r, right_c = edgeIndicies[2][0]+1 ,edgeIndicies[2][1] -1
    while True:
        down_r, down_c = down_r + 1, down_c
        if isInLine(down_r, down_c, N):
            BLANK_MAP[down_r][down_c] = 4
        else:
            break
    while True:
        right_r, right_c = right_r, right_c + 1
        if isInLine(right_r, right_c, N) and BLANK_MAP[right_r][right_c] != 5:
            BLANK_MAP[right_r][right_c] = 4
        else:
            break
        
    # Group 2
    rightAndUp = edgeIndicies[2]
    up_r, up_c = edgeIndicies[0][0] + 1, edgeIndicies[0][1]+1
    right_r, right_c = rightAndUp[0], rightAndUp[1]
    while True:
        up_r, up_c = up_r - 1, up_c
        if isInLine(up_r, up_c, N) and BLANK_MAP[up_r][up_c] != 5:
            BLANK_MAP[up_r][up_c] = 2
        else:
            break
    while True:
        right_r, right_c = right_r, right_c +1
        if isInLine(right_r, right_c, N):
            BLANK_MAP[right_r][right_c] = 2
        else:
            break
        # 완벽하진 않은데, 이대로 DFS해도 될듯 -> 아니었다.
    # 각 1,2,3,4의 initPOS는 기억할 필요가 없는게, 전체 MAP의 각 꼭짓점이 순서대로 각각의 1,2,3,4이다.

    return BLANK_MAP, GroupFiveIndexList

def countPeoplePerGroup(BLANK_MAP, MAP, x,y,N):
    """dfs"""
    x-=1
    y-=1
    GroupInitList = [[0,0], [0,N-1], [N-1, 0], [N-1,N-1], [x,y]] # 1,2,3,4,5
    GroupPeopleList = [] # [[GroupNum, PeopleCnt]]
    
    for i in range(len(GroupInitList)):
        visited = [[False]*N for _ in range(N)]
        Group = GroupInitList[i]
        GroupNum = i+1
        queue = deque()
        queue.append(Group)
        thisGroupPeople = MAP[Group[0]][Group[1]]

        while queue:
            curIndex = queue.pop()
            curR, curC = curIndex[0], curIndex[1]
            visited[curR][curC] = True

            for j in range(4):
                tmp_r, tmp_c = curR + dr[j], curC + dc[j]
                if isInLine(tmp_r, tmp_c, N):
                    if visited[tmp_r][tmp_c] == False:
                        if BLANK_MAP[tmp_r][tmp_c] ==0 or BLANK_MAP[tmp_r][tmp_c] == GroupNum:

                            BLANK_MAP[tmp_r][tmp_c] = GroupNum

                            queue.append([tmp_r, tmp_c])
                            visited[tmp_r][tmp_c] = True
                            thisGroupPeople += MAP[tmp_r][tmp_c]

        GroupPeopleList.append(thisGroupPeople)


    return GroupPeopleList, BLANK_MAP

def MinMaxCalculator(GroupPeopleList):

    GroupPeopleList.sort()
    Maximum = GroupPeopleList[-1]
    Minimum = GroupPeopleList[0]

    difference = Maximum - Minimum

    return abs(difference)

def main(MAP, N):
    difference = float('inf')
    optimal_MAP = None
    tmp_difference = N
    for d_1 in range(1, N):
        for d_2 in range(1,N):
            for x in range(1, N):
                if x + d_1 + d_2 <= N:
                    for y in range(1, N):
                        if 1 <= y - d_1 and y+d_2 <= N:
                            BLANK_MAP = [[0]*N for _ in range(N)]
                            BLANK_MAP[0][0] = 1
                            BLANK_MAP[N-1][0] = 3
                            BLANK_MAP[N-1][N-1] = 4
                            BLANK_MAP[0][N-1] = 2
                            BLANK_MAP, GroveFiveIndexList = make_groupFive(BLANK_MAP, x, y, d_1, d_2, N)

                            # print(f"connected components:")
                            # MAP_printer(BLANK_MAP)

                            GroupPeopleList, BLANK_MAP = countPeoplePerGroup(BLANK_MAP, MAP, x, y, N)

                            # print(f"connected components:")
                            # MAP_printer(BLANK_MAP)

                            # print(f"Group people List : {GroupPeopleList}")

                            tmp_difference = MinMaxCalculator(GroupPeopleList)
                            # print(f"tmp_difference : {tmp_difference}")

                            difference = min(tmp_difference, difference)

                            if tmp_difference != difference:
                                optimal_MAP = BLANK_MAP[:]
                                tmp_difference = difference
    return difference, optimal_MAP



def isInLine(R,C,N):
    if 0<= R < N and 0 <= C < N:
        return True

    return False

def input_getter():
    N = int(input())
    MAP = []
    for _ in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)


    return N, MAP

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

def internal_debug_checker(MAP, BLANK_MAP, N, x, y, d_1, d_2):
    BLANK_MAP, GroveFiveIndexList = make_groupFive(BLANK_MAP, x, y, d_1, d_2, N)

    GroupPeopleList = countPeoplePerGroup(BLANK_MAP, MAP, x, y, N)

    tmp_difference = MinMaxCalculator(GroupPeopleList)

    # MAP_printer(BLANK_MAP)
    # print(f"Group People List : {GroupPeopleList}")

    return tmp_difference


if __name__ == "__main__":
    N, MAP = input_getter()

    # difference = internal_debug_checker(MAP, BLANK_MAP, N, 2,4,2,2)

    difference, optimal_MAP = main(MAP, N)

    # print(f"optimal_map : ")
    # MAP_printer(optimal_MAP)

    # print(f"population : ")    
    # MAP_printer(MAP)

    print(difference)
