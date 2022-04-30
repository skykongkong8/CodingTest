# 아기 상어 리뷰

def input_getter():
    N = int(input())
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))
    
    return N, MAP

def getSharkPos(MAP, N):
    for a in range(N):
        for b in range(N):
            if MAP[a][b] == 9:
                return [a,b]

from collections import deque

class BabyShark:
    def __init__(self, sharkPos):
        self.pos = sharkPos
        self.size = 2
        self.fishCnt = 0

    def sharkGrowChecker(self):
        if self.fishCnt == self.size:
            self.size +=1
            self.fishCnt = 0

dr = [0,0,1,-1]
dc = [1,-1,0,0]

def findEdibleFishes(MAP : list, N : int, shark : BabyShark):
    queue = deque()
    edible_fishes = []
    visited = [[0]*N for _ in range(N)]
    distanceMAP = [[0]*N for _ in range(N)]
    distance = 0
    sharkPos = shark.pos
    init_r, init_c = sharkPos[0], sharkPos[1]
    sharkSize = shark.size
    
    queue.append([init_r, init_c])
    visited[init_r][init_c] = True
    minimum_distance = float('inf')
    break_flag = False
    while queue:

        curData = queue.popleft()
        curR, curC = curData[0], curData[1]
        distance = distanceMAP[curR][curC]

        for i in range(4):
            tmp_r, tmp_c = curR+dr[i], curC+dc[i]
            if 0<= tmp_r < N and 0<= tmp_c < N:
                if not visited[tmp_r][tmp_c]:
                    visited[tmp_r][tmp_c] = True
                    distanceMAP[tmp_r][tmp_c] = distance + 1

                    
                    if MAP[tmp_r][tmp_c] < sharkSize and MAP[tmp_r][tmp_c] != 0:
                        queue.append([tmp_r, tmp_c])
                        edible_fishes.append([tmp_r, tmp_c, distanceMAP[tmp_r][tmp_c]])

                        if minimum_distance >= distanceMAP[tmp_r][tmp_c]:
                            minimum_distacne = distanceMAP[tmp_r][tmp_c]
                        elif minimum_distacne < distanceMAP[tmp_r][tmp_c]:
                            break_flag = True
                            break
                    
                        

                    elif MAP[tmp_r][tmp_c] <= sharkSize:
                        queue.append([tmp_r, tmp_c])
        if break_flag:
            break
    return edible_fishes


def pick_optimal_fish_and_eat(MAP, edibleFishes, shark):
    edibleFishes.sort(key = lambda a: (a[2], a[0], a[1]))
    opt_fish = edibleFishes[0]
    opt_r, opt_c, opt_d = opt_fish[0], opt_fish[1], opt_fish[2]
    shark_r, shark_c = shark.pos[0], shark.pos[1]
    MAP[opt_r][opt_c] = 0

    MAP[opt_r][opt_c], MAP[shark_r][shark_c] = MAP[shark_r][shark_c], MAP[opt_r][opt_c]
    shark.pos = [opt_r, opt_c]
    shark.fishCnt += 1
    shark.sharkGrowChecker()

    return shark, opt_d


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()


if __name__ == "__main__":
    N, MAP = input_getter()
    shark_init_pos = getSharkPos(MAP, N)
    shark = BabyShark(shark_init_pos)
    time_cnt = 0
    while True:
        edible_fishes = findEdibleFishes(MAP, N, shark)
        # print(f"edible fishes found : {edible_fishes}")/
        if edible_fishes:

            shark, time = pick_optimal_fish_and_eat(MAP, edible_fishes, shark)
            time_cnt += time

        else:
            break
    print(time_cnt)

"""
복습
1. distanceMAP을 하나 더만들었다.
bfs니까, distanceMAP이라는 자료 구조를 하나 더 생성하는게 그 방식의 장점을 살리는 것이라고 생각하였다.

2. 이렇게 자기 자체의 정보를 특정 조건에 따라 업데이트 해주어야 하는 경우에 한해, 클래스를 쓰는 것도 나쁘지 않겠다는 생각이 들었다.
    단, 위의 경우처럼 딱 하나의 객체가 동적으로 움직이는 경우에서... (MAP에 들어가는 자료구조일  경우에는 지양하자는 뜻)
    
    왜 그동안 사용하지 않았냐면, 메모르 주소가 꼬이는 일이 빈번하게 발생하였기 때문이다. (나 스스로의 파이썬 메모리 주소 저장 방식에 대한 이해 부족으로..)
    이제 왜 사용하려고 하냐면, 특정 경우에 따라 데이터를 업데이트 시켜주기 위해서는 이 방식이 꽤 좋기 때문이다.
    물론, 그냥 리스트나 딕셔너리처럼 구성해도 되지만,, 클래스의 장점인 직관성을 살릴 수 있다는 점도 좋다.
"""