# 상어 중학교
from collections import deque

dr = [0,0,1,-1]
dc = [1,-1,0,0]

def input_getter():
    MAP = []
    N, M = map(int, input().split(' '))
    for _ in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)
    
    return N, M, MAP

"""
MAP = [
    ...
    [[r, c, color(?) ], ...]
    ...
]

component_DataList = [
    ...
    [#normalBlocks, #RainbowBlocks, #TotalBlocks, #기준블록Pos, [각 블록 인덱스 리스트]]
    ...
]
"""

def find_connected_component(MAP, N, M):
    """N_4 Connected Component with Manhattan Distance Adjacency with special criterions"""
    component_DataList = []
    visited = [[False]*N for _ in range(N)]
    sentinel = make_sentinel(M)

    for r in range(N):
        for c in range(N):
        
            queue = deque()

            initial = MAP[r][c]


            if visited[r][c]:
                continue
            
            if MAP[r][c] == 0: # 무지개색을 이니시로 잡으면 의미가 없다.
                continue
            
            if MAP[r][c] == sentinel:
                continue

            if MAP[r][c] == -1: # 검은색은 component에 포함될 수 없다.
                visited[r][c] = True
                continue
            
            queue.append([[r,c], initial])   
            """
            queue = [
                ...
                [ [r, c], color]
                ...
            ]
            """
            blockColor = MAP[r][c]
            blockInfoList = [] # [#normalBlocks, #RainbowBlocks, #TotalBlocks (#normalBlocks+#RainbowBlocks), #기준불록Pos, [개별블록위치리스트]]
            eachBlockPosList = [[[r,c], blockColor]] # [[[r, c], color], ...]
            normalBlocks = 1
            RainbowBlocks = 0
            StdBlockPos = [r, c] # 이미 발생한 init값
            rainbowPosList= []
            
            while queue:
                curData = queue.pop()
                curR, curC = curData[0][0], curData[0][1]
                visited[curR][curC] = True

                curColor = curData[1]
                # print(f"With blockColor {blockColor}, data : {curData}")

                # if curColor == 0:
                #     visited[curR][curC] = False

                for i in range(4):
                    tmp_r, tmp_c = curR + dr[i], curC + dc[i]
                    """
                    검정 : -1
                    무지개 : 0
                    일반 : 그 외
                    """
                    if 0 <= tmp_r < N and 0 <= tmp_c < N: # 격자 내 존재
                        
                        if MAP[tmp_r][tmp_c] != -1 and MAP[r][c] != sentinel: # 검정 블록이 아님
                            if visited[tmp_r][tmp_c] == False: # 방문하지 않은 위치 
                                # -> 이후 방문 표시할 때, 확실하게 블록그룹으로 포함된 위치만 방문 표시하여야함!
                                # 추후 완결지어지면, 그 때 개별블록위치리스트에서 참조하여 visited표현을 하자.
                                # 아니면, 지금은 True 표시를 하고, component created flag를 만들어서 그게 False 뜨면 False 처리로 바꿔주자!

                                # 무지개색 블록
                                if MAP[tmp_r][tmp_c] == 0:
                                    RainbowBlocks += 1
                                    eachBlockPosList.append([[tmp_r, tmp_c], 0])
                                    queue.append([[tmp_r, tmp_c], 0])
                                    rainbowPosList.append([tmp_r, tmp_c])
                                    # print(f"rainbowPosList : {rainbowPosList}")
                                    visited[tmp_r][tmp_c] = True
                                    # 무지개색 블록은 어디든 포함될 수 있어서 visited로 고려하지 않는다.
                                
                                # 일반 블록
                                elif MAP[tmp_r][tmp_c] == blockColor: # 하나의 색만 가질 수 있음
                                    normalBlocks += 1
                                    eachBlockPosList.append([[tmp_r, tmp_c], blockColor])
                                    queue.append([[tmp_r, tmp_c], blockColor])
                                    
                                    # 나중에 한꺼번에 소팅하면 시간복잡도 엄청 상승하므로 지금 업데이트 해주는 방식으로 가자.
                                    std_list = [StdBlockPos, [tmp_r, tmp_c]]
                                    std_list.sort(key = lambda a: (a[0], a[1]))

                                    StdBlockPos = std_list[0]

                                
                                    visited[tmp_r][tmp_c] = True
                        # MAP_printer(visited)

            # 하나의 connected component 탐사가 끝났다.
            # 현재 가지고 있는 정보들이 실제로 BlockGroup인지 판별하여 보자.
            #[#normalBlocks, #RainbowBlocks, #TotalBlocks (#normalBlocks+#RainbowBlocks), #기준불록Pos, [개별블록위치리스트]]
        
            componentCreatedFlag = False
            blockInfoList = [normalBlocks, RainbowBlocks, normalBlocks+RainbowBlocks, StdBlockPos, eachBlockPosList] 
            # print(f"[normalBlocks, RainbowBlocks, normalBlocks+RainbowBlocks, StdBlockPos, eachBlockPosList]\n{blockInfoList}\n")
            

            if normalBlocks >= 1 and normalBlocks+RainbowBlocks >=2:
                componentCreatedFlag = True
                component_DataList.append(blockInfoList)
            
            for rainbowIndex in rainbowPosList:
                # print(f"rainbowIndicies {rainbowPosList}\n")
                rainR, rainC = rainbowIndex[0], rainbowIndex[1]
                visited[rainR][rainC] = False

            if not componentCreatedFlag:
                for index in eachBlockPosList: # [[r, c, color], ...]
                    falseR, falseC = index[0][0], index[0][1]
                    # print(f"not your component : {eachBlockPosList}")

                    visited[falseR][falseC] = False

    
    return component_DataList
# 중복이 하나 뜬게 쪼금 수상하지만 우선 넘어가자.

                                
def make_sentinel(M):
    return M+1

def AutoPlay(component_DataList, MAP, N, M):
    """자동 모드"""
    #1 biggest 
    """
    component_DataList = [
    ...
    [#normalBlocks, #RainbowBlocks, #TotalBlocks, #기준블록Pos, [각 블록 인덱스 리스트]]
    ...
]
    """
    sentinel = make_sentinel(M)
    # sentinel = float('inf')

    component_DataList.sort(key = lambda a : (-a[2],-a[1], -a[3][0], -a[3][1])) # 기준 : 크기가 가장 큰/무지개/행열큰
    biggest_component = component_DataList[0]

    score = biggest_component[2] **2
    indicies = biggest_component[4]
    for index in indicies:
        r, c = index[0][0], index[0][1]
        MAP[r][c] =  sentinel # 0이거나 -1이면 무지개/검정색 -> 절대 있을 수 없는 숫자 M+1
    
    MAP = setGravity(MAP, N, sentinel)
    # print(f"after fisrt gravitation")
    # MAP_printer(MAP)

    tupleMAP = list(zip(*MAP))[::-1]
    MAP = []
    for row in tupleMAP:
        MAP.append(list(row))
    
    # print(f"after Rotation : ")
    # MAP_printer(MAP)

    MAP = setGravity(MAP, N, sentinel)
    # print(f"after second gravitation")

    return MAP, score



def setGravity(MAP, N, sentinel):
    """중력 작용을 활성화시키는 함수 : 블록이 중력 방향으로 움직이지 못할 때까지 이동함!"""
    for r in range(N-2, -1, -1): # 맨아래 바로 위에서부터 시작
        for c in range(N-1, -1, -1):
            
            curVal = MAP[r][c]

            if curVal == -1:
                continue
            elif curVal == sentinel:
                continue
            # print(f"start with : {curVal}")
            # MAP_printer(MAP)

            curR, curC = r, c
            for n in range(N):
                tmpR, tmpC = curR, curC
                tmpR += 1
                if 0 <= tmpR < N:
                    if MAP[tmpR][tmpC] != -1:
                        if MAP[tmpR][tmpC] == sentinel:
                            curR, curC = tmpR, tmpC
                            # print(f"row updated! {curR}")
                        else:
                            break
                    else:
                        break
                else:
                    break

            MAP[curR][curC] = curVal
            if curR != r:
                MAP[r][c] = sentinel
            
    return MAP
            

def MAP_printer(matrix):
    for row in matrix:
        print(row)
    print()



if __name__ == "__main__":
    N, M, MAP =input_getter()
    # print(f"init MAP :")
    # MAP_printer(MAP)
    answer = 0
    cnt = 0
    while True:
        component_DataList = find_connected_component(MAP, N, M)
        if len(component_DataList) < 1:
            break

        # print("Grouping : ")
        # MAP_printer(component_DataList)

        MAP, score= AutoPlay(component_DataList, MAP, N, M)
        # print(f"score gotten : {score}")
        answer += score
        # MAP_printer(MAP)
        cnt+=1

    print(answer)

"""
배운점
1. dr, dc만을 사용하다 보니 개별 인덱싱으로 r,c 방향주는 것에 무뎌졌다. 아래 방향+...
2. 갑자기 헷갈렸었는데, DFS는 Stack이고 BFS가 Queue이다.
3. Connected Component를 특수한 조건과 함께 탐색하는 방법에 대해 좋은 연습을 할 수 있었다.
4. 회전하는 함수 잘 써먹고 있다.

처음으로 별로 어렵지 않다고 느껴진 문제.
"""