# 인구 이동
from collections import deque

def input_getter():
    N, L, R = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))

    return N, L, R, MAP

"""
국경선 공유 여부를 담고 있는 MAP을..

dataMAP = [
    ...
    [ [ population, [False, False, False, False] ], ... ]
    ...
]


아니면,
그냥 dfs를 하면서 형성하기? -> 이렇게 해도 될 것 같은데?
"""

dr = [0,0,1,-1]
dc = [1,-1,0,0]

def make_union(MAP, L, R, N):
    # global_visited_MAP = [[False]*N for _ in range(N)]

    total_unions = [] # total connectedComponents
    visited = [[False]*N for _ in range(N)]
    
    for r in range(N):
        for c in range(N):
            
            if not visited[r][c]:
                curCountry = [[r,c], MAP[r][c]] # 이것도 선별해서 뽑아야하지 않나..

                we_are_the_unions = [curCountry]

                # print(f"start dfs for {r, c}")

                visited[r][c] = True
                # print("visited : ")
                # MAP_printer(visited)

                queue = deque()
                queue.append(curCountry)
                while queue:
                    curCountry = queue.pop()
                    curR, curC, curNum = curCountry[0][0], curCountry[0][1], curCountry[1]
                    # visited[curR][curC] = True

                    for i in range(4):
                        tmp_r, tmp_c = curR + dr[i], curC + dc[i]
                        if 0<= tmp_r < N and 0 <= tmp_c < N:
                            # print(f"check for {tmp_r, tmp_c}")
                            if visited[tmp_r][tmp_c] == False:

                                tmpNum = MAP[tmp_r][tmp_c]
                                if L <= abs(tmpNum - curNum) <= R:
                                    visited[tmp_r][tmp_c] = True # 이게 중요한게, 다른 쪽으로 와서 방문하면 이게 또 될 수도 있으니까 아예 방문을 안해버리는 건 별로 안좋지 않을까?
                                    # 그러니까 확실히 우리 union임이 판명 났을 때만 방문처리해주면 어떨까?
                                    # print("visited : ")
                                    # MAP_printer(visited)

                                    we_are_the_unions.append([[tmp_r,tmp_c], MAP[tmp_r][tmp_c]])
                                    queue.append([[tmp_r,tmp_c], MAP[tmp_r][tmp_c]])

                if len(we_are_the_unions) > 1:
                    total_unions.append(we_are_the_unions)
                else:
                    visited[r][c] = False
                    # print("visited : ")
                    # MAP_printer(visited)

    # 어쩌면 visitedMAP이 나중에 필요할 수 도 있음 (별로 안필요할수도있긴한데)
    return total_unions

from math import floor

def move_populations(MAP, total_unions):
    for unions in total_unions:
        union_cnt = 0
        union_population = 0
        
        for union in unions: # union = [r,c], cnt
            union_cnt +=1
            union_population += union[1]
        
        population_distribution = floor(union_population/union_cnt)

        for union in unions:
            r, c = union[0][0], union[0][1]
            MAP[r][c] = population_distribution
    return MAP


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()



if __name__ == "__main__":
    N, L, R, MAP = input_getter()
    cnt = 0
    while True:
        unions = make_union(MAP, L, R, N) 
        if unions == []:
            break

        # MAP_printer(unions)

        MAP = move_populations(MAP, unions)
        # print("after population distribution")
        # MAP_printer(MAP)
        cnt+=1

    print(cnt)



