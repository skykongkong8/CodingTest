# 청소년 상어

dr = [None, -1,-1,0,1,1,1,0,-1]
dc = [None, 0,-1,-1,-1,0,1,1,1]
N = 4
remaining_fishNums = [i+1 for i in range(16)]

def input_getter():
    MAP = [[0]*N for _ in range(N)]
    for r in range(N):
        row = list(map(int, input().split(' ')))
        for c in range(N):
            curfish = [row[2*c], row[2*c+1]] # fish = [ num, dir ]
            MAP[r][c] = curfish

    return MAP

class Shark:
    def __init__(self):
        self.pos = [0,0]
        self.dir = None
        self.fishNum = 0

EMPTY= [0,0] # 0,0 인덱스랑 헷갈릴까봐..

def initiation(shark, MAP):
    global EMPTY
    init_fish = MAP[shark.pos[0]][shark.pos[1]]
    init_fishNum, init_fishDir = init_fish[0], init_fish[1]

    shark.fishNum += init_fishNum
    shark.dir = init_fishDir

    MAP[0][0] = EMPTY

    return shark, MAP

def find_fishData_with_fishNum(MAP, fishNum):
    for fr in range(N):
        for fc in range(N):
            if MAP[fr][fc][0] == fishNum:
                return [fr, fc, MAP[fr][fc][1]]

    # raise NoOptionError
    return False


def direction_bounder(direction):
    if direction > 8:
        direction -=8
    elif direction <= 0:
        direction += 8
    return direction

def moveFish(MAP, shark):
    global remaining_fishNums, EMPTY

    for n in remaining_fishNums:
        curNum = n
        curData = find_fishData_with_fishNum(MAP, curNum)
        if curData:

            curR, curC, curD = curData[0], curData[1], curData[2]
            tmp_r, tmp_c = curR, curC

            for i in range(8):
                curD = direction_bounder(curD + i)
                
                tmp_r, tmp_c = tmp_r+dr[curD], tmp_c + dc[curD]
                if 0 <= tmp_r < N and 0 <= tmp_c < N:
                    #1 빈칸
                    if MAP[tmp_r][tmp_c] == EMPTY:
                        MAP[curR][curC][1] = curD
                        MAP[tmp_r][tmp_c], MAP[curR][curC] = MAP[curR][curC], MAP[tmp_r][tmp_c]
                        break

                    #2 다른 물고기가 있는 경우
                    elif (tmp_r == shark.pos[0]) and (tmp_c == shark.pos[1]):
                        MAP[curR][curC][1] = curD
                        MAP[tmp_r][tmp_c], MAP[curR][curC] = MAP[curR][curC], MAP[tmp_r][tmp_c] # 처리가 똑같다? 아마 그럴 것이다..
                        break

                    #3 상어 칸
                    else:
                        continue

    return MAP
from collections import deque

def getEdibleFishes(MAP, shark):
    global EMPTY
    sharkPos = shark.pos
    sharkR, sharkC = sharkPos[0], sharkPos[1]

    sharkDir = shark.dir
    fish_candidates = []
    tmp_r, tmp_c = sharkR, sharkC
    while True:
        tmp_r, tmp_c = tmp_r + dr[sharkDir], tmp_c + dc[sharkDir]
        if 0<= tmp_r < N and 0<= tmp_c < N:
            if MAP[tmp_r][tmp_c] != EMPTY:
                fish_candidates.append([tmp_r, tmp_c])
        else:
            break
    return fish_candidates

maximum_fish_eaten = -1
from copy import deepcopy
def moveShark(MAP, shark, fishNum):
    global maximum_fish_eaten
    """
    주어진 인덱스로 움직이는 것만 하자? -> 그런것은 애초에 의미가 없다.
    """
    MAP = deepcopy(MAP)
    shark_row, shark_col = shark.pos[0], shark.pos[1]
    number = MAP[shark_row][shark_col][0]
    direction = MAP[shark_row][shark_col][1]
    MAP[shark_row][shark_col] = EMPTY
    

    maximum_fish_eaten = max(maximum_fish_eaten, fishNum + number)


    MAP = moveFish(MAP, shark)

    edibleFishes = getEdibleFishes(MAP, shark)


    for fishrc in edibleFishes:
        fishR, fishC = fishrc[0], fishrc[1]
        shark.pos = [fishR, fishC]
        moveShark(MAP, shark, fishNum + number)

    



   




    



            
            


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

if __name__ == "__main__":
    MAP= input_getter()
    print(f"init MAP:")
    MAP_printer(MAP)

    shark = Shark()
    shark, MAP = initiation(shark, MAP)
    maximum_fish_eaten = shark.fishNum

    moveShark(MAP, shark, 0)

    print(maximum_fish_eaten)



