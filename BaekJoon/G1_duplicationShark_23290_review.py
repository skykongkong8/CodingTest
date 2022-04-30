# 복제 상어 리뷰
N = 4
STINK = -3
dr = [None, 0,-1,-1,-1,0,1,1,1] # 인덱스 0 < 1 ~ 8 < 9
dc = [None, -1,-1,0,1,1,1,0,-1]

shark_dr = [None, -1,0,1,0]
shark_dc = [None, 0,-1,0,1]

def input_getter():
    global N
    M, S = map(int, input().split(' '))
    MAP = [[[] for i in range(N)] for j in range(N)]
    linear_fishList = []
    stinkMAP = [[0]*N for _ in range(N)]
    for _ in range(M):
        r, c, d = map(int, input().split(' '))
        r -= 1
        c -= 1
        # d -= 1
        MAP[r][c].append(d)
        linear_fishList.append([r,c,d])
    s_r, s_c = map(int, input().split(' '))
    s_r -= 1
    s_c -= 1
    """
    1 ~ 8 : 물고기의 방향
    0 : 비어있음
    -3, -2, -1 : 물고기 냄새 (STINK) 어쨌든 음수

    """
    sharkPos = [s_r, s_c]
    return M, S, MAP, sharkPos, linear_fishList, stinkMAP

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

import copy
def cast_duplication(MAP):
    rememberMAP = copy.deepcopy(MAP)

    return rememberMAP

def direction_bounder(direction):
    if direction < 1:
        direction += 8
    elif direction >8:
        direction -= 8
    return direction

def fishMove(MAP, sharkPos, linear_fishList, stinkMAP):
    for lf in range(len(linear_fishList)):
        fishData = linear_fishList[lf]
        cur_r, cur_c, cur_d = fishData[0], fishData[1], fishData[2]
        for i in range(8):
            cur_d = direction_bounder(cur_d + 1)
            tmp_r, tmp_c = cur_r + dr[cur_d], cur_c + dc[cur_d]
            if 0 <= tmp_r < N and 0 <= tmp_c < N:
                if stinkMAP[tmp_r][tmp_c] >= 0:
                    if (tmp_r, tmp_c) != (sharkPos[0], sharkPos[1]):
                        linear_fishList[lf] = [tmp_r, tmp_c, cur_d]
    # print(f"sharkPos : {sharkPos}")
    # print(f"linear_fishList : {linear_fishList}")
    MAP = [[[] for i in range(N)] for j in range(N)]

    for lf in range(len(linear_fishList)):
        fishData = linear_fishList[lf]
        cur_r, cur_c, cur_d = fishData[0], fishData[1], fishData[2]
        
        MAP[cur_r][cur_c].append(cur_d)

    return MAP, linear_fishList

def stink_fadeAway(stinkMAP):
    for a in range(N):
        for b in range(N):
            if stinkMAP[a][b] < 0:
                stinkMAP[a][b] += 1
    return stinkMAP

def sharkMove(sharkPos, MAP, stinkMAP):
    possible_routes = []
    maximum_fishOut = 0
    # visited = [[0]*N for _ in range(4)]
    cur_r, cur_c = sharkPos[0], sharkPos[1] 

    for i in range(1,5):
        tmp_r, tmp_c = cur_r + shark_dr[i], cur_c + shark_dc[i]
        if 0 <= tmp_r < N and 0<= tmp_c < N:
            # curfish와 같을 수가 없음
            first_fish = len(MAP[tmp_r][tmp_c])

            for j in range(1,5):
                tmp_tmp_r, tmp_tmp_c = tmp_r + shark_dr[j], tmp_c + shark_dc[j]
                if 0 <= tmp_tmp_r < N and 0 <= tmp_tmp_c < N:
                    # curRC와 같을 수 있음
                    if (tmp_tmp_r == tmp_r) and (tmp_tmp_c == tmp_c):
                        second_fish = 0
                    else:
                        second_fish = len(MAP[tmp_tmp_r][tmp_tmp_c])

                        for k in range(1,5):
                            tmp_tmp_tmp_r, tmp_tmp_tmp_c = tmp_tmp_r + shark_dr[k], tmp_tmp_c + shark_dc[k]
                            if 0 <= tmp_tmp_tmp_r < N and 0 <= tmp_tmp_tmp_c < N:
                                # curRC 또는 tmpRC와 같을 수 있음
                                if ((tmp_r == tmp_tmp_tmp_r) and (tmp_c == tmp_tmp_tmp_c)) or ((tmp_tmp_r == tmp_tmp_tmp_r) and (tmp_tmp_c == tmp_tmp_tmp_c)):
                                    third_fish = 0
                                else:
                                    third_fish = len(MAP[tmp_tmp_tmp_r][tmp_tmp_tmp_c])

                                thisPathFishOut = first_fish + second_fish + third_fish

                                if thisPathFishOut > maximum_fishOut:
                                    maximum_fishOut = thisPathFishOut
                                    possible_routes = []
                                    possible_routes.append([i, j, k])
                                
                                elif thisPathFishOut == maximum_fishOut:
                                    possible_routes.append([i, j ,k])
    # print(f"possible_routes : {possible_routes}")
    if len(possible_routes) > 1:
        possible_routes.sort(key = lambda a : 100*a[0]+10*a[1]+a[2])

    optimal_route = possible_routes[0]

    for t in range(3):
        cur_r, cur_c = cur_r + shark_dr[optimal_route[t]], cur_c + shark_dc[optimal_route[t]]
        if MAP[cur_r][cur_c]:
            stinkMAP[cur_r][cur_c] = -3

        MAP[cur_r][cur_c].clear()
        

    sharkPos = [cur_r, cur_c]

    return sharkPos, MAP, stinkMAP

def makeLinearList_fromMAP(MAP):
    linear_fishList = []
    for i in range(N):
        for j in range(N):
            if MAP[i][j]:
                for d in MAP[i][j]:
                    linear_fishList.append([i,j,d])
    return linear_fishList

def duplicate_cast_appear(MAP, duplicatedMAP):
    for i in range(N):
        for j in range(N):
            if duplicatedMAP[i][j] and duplicatedMAP[i][j] != []:
                for d in duplicatedMAP[i][j]:
                    MAP[i][j].append(d)
    linear_fishList = makeLinearList_fromMAP(MAP)
    return MAP, linear_fishList

def answerGetter(MAP):
    ans = 0
    for r in range(N):
        for c in range(N):
            if MAP[r][c]:
                ans += len(MAP[r][c])
    return ans
    

if __name__ == "__main__":
    M, S, MAP, sharkPos, linear_fishList, stinkMAP = input_getter()
    # print("initMAP")
    # MAP_printer(MAP)
    for s in range(S):
        duplicatedMAP = cast_duplication(MAP)
        
        MAP, linear_fishList = fishMove(MAP, sharkPos, linear_fishList, stinkMAP)
        # print("after fishMove")
        # MAP_printer(MAP)

        sharkPos, MAP, stinkMAP = sharkMove(sharkPos, MAP, stinkMAP)
        # print(f"after sharkMove sharkPos : {sharkPos}")
        # print("MAP")
        # MAP_printer(MAP)

        stinkMAP = stink_fadeAway(stinkMAP)
        # print("stinkMAP")
        # MAP_printer(stinkMAP)

        MAP, linear_fishList = duplicate_cast_appear(MAP, duplicatedMAP)
        # print("after duplication")
        # MAP_printer(MAP)

    answer = answerGetter(MAP)
    # print("finalMAP")
    # MAP_printer(MAP)

    print(answer)

"""
배운점

1. 3차원 리스트 초기화하는 법 대박!
2. linearList와 MAP 사이의 조화, MAP2LL 과 LL2MAP에 대한 생각 꼭 하기
3. 속도인덱스를 0부터 말고 1부터 하는 방식 -> 0, -1 등을 특수 상태로 놓고 쓸 수 있음
4. 지속적으로 변하는 값일 경우 서로 다른 MAP 구조를 생성하여 저장해두기
    특히, main MAP이 3차원으로 되어있으면, 생각할 것도 없이 다른 맵에 자료 저장하자.

5. sort를 a끼리의 연산으로도 할 수 있다는 것. 지식이 늘었다.
6. 3 중 반복문 세련되게 쓰면 열 DFS 부럽지 않다! 진짜야..

7. 엣지케이스 같은 곳에서 막혔다면, if else 등 이후의 코드 인덴테이션를 꼭 확인하자!!! 오늘 많이 얻어가네...
"""