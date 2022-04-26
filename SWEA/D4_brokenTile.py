# 부서진 타일

def input_getter():
    TC = int(input())
    TC_LIST = []
    for __ in range(TC):
        N, M = map(int, input().split(' '))
        MAP = []
        for _ in range(N):
            MAP.append(list(input()))
        TC_LIST.append(MAP)

    return TC, TC_LIST
from collections import deque

dr = [0,0,-1,1]
dc = [1,-1,0,0]

# def masking2D(MAP):
#     R = len(MAP)
#     C = len(MAP[0])
#     global_visited_map = [[False]*len(C) for _ in range(R)]

#     for r in range(R):
#         for c in range(C):
            
#             this_init = MAP[r][c]
#             if this_init == '.':
#                 continue

#             visited = [[False]*len(C) for _ in range(R)]
#             visited[r][c] = True # 이거 맞냐?

#             queue.append([MAP[r][c], [r,c]])

#             queue = deque()
#             while queue:
#                 curData = queue.pop()
#                 curVal = curData[0]
#                 curR, curC = curData[1][0], curData[1][1]
#                 tile_indicies = [
#                     [curR, curC],
#                     [curR+1, curC],
#                     [curR, curC+1],
#                     [curR+1, curC+1]
#                 ]

#                 isit_2x2BrokenTile = True

#                 for index in tile_indicies:
#                     tmp_r, tmp_c = index[0], index[1]
#                     if 0<= tmp_r < R and 0 <= tmp_c < C:
#                         if MAP[tmp_r][tmp_c] != '#':
#                             isit_2x2BrokenTile = False
#                             break
#                     else:
#                         isit_2x2BrokenTile = False
#                         break

#                 if isit_2x2BrokenTile:
#                     for index in tile_indicies:
#                         tile_r, tile_c = index[0], index[1]
#                         visited[tile_r][tile_c] = True

def greedilyMasking(MAP):
    R = len(MAP)
    C = len(MAP[0])
    tmpMAP = MAP[:]
    for r in range(R):
        for c in range(C):
            curVal = tmpMAP[r][c]
            if curVal == '#':
                masking_indicies = [
                    [r,c],
                    [r+1, c],
                    [r, c+1],
                    [r+1, c+1]
                ]
                isit_maskable = True
                for index in masking_indicies[1:]:
                    tmp_r, tmp_c = index[0], index[1]
                    if 0 <= tmp_r < R and 0<= tmp_c < C:
                        if tmpMAP[tmp_r][tmp_c] == '.':
                            isit_maskable = False
                            break
                    else:
                        isit_maskable = False
                        break

                if isit_maskable:
                    for index in masking_indicies:
                        tmp_r, tmp_c = index[0], index[1]
                        tmpMAP[tmp_r][tmp_c] = '.'
    # MAP_printer(tmpMAP)
    isit_done = True
    for r in range(R):
        this_row = MAP[r]
        if '#' in this_row:
            isit_done = False
            break
    
    if isit_done:
        res = "YES"
    elif not isit_done:
        res = "NO"

    return res

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()
                    







if __name__ == "__main__":
    TC, TC_LIST = input_getter()
    for tc in range(TC):
        this_TC = TC_LIST[tc]
        res = greedilyMasking(this_TC)

        print(f"#{tc+1} {res}")

"""
배운점

1. 때로는 너무 복잡하게 생각하지 않아도 될 때가 있다. DFS도 좋지만, 여기서 하려면 코드를 많이 더 써야할 것 같다.
    그리디 알고리즘으로 문제가 단순히 풀릴 수도 있다는 것을 기억하자.

2. 사실 매번 문제를 보고 이것이 그리디 알고리즘으로 해결될지 안될지를 단번에 파악하는 것은 개인적으로 지금으로서는 역부족이라고 생각한다.
    따라서 우선 이러한 개별적인 케이스를 모아보자. (그리디 알고리즘으로 쉽게 풀리는)
    이것이 쌓이다 보면 특별한 인사이트가 생길 수도 있다.

3. 본 문제의 경우 2x2마스킹으로 특정 영역을 1회씩만 마스킹할 수 있을지 없을지를 판별하는 문제였다.
"""