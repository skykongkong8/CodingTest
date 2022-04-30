# 낚시왕
import sys
sys.setrecursionlimit(10**6)

def input_getter():
    R, C, M = map(int, input().split(' '))
    sharks_data = []
    MAP = [[0]*C for _ in range(R)]

    for _ in range(M):
        r, c, s, d, z = map(int, input().split(' '))
        r -= 1
        c -= 1
        d -= 1
    
        sharks_data.append([r,c,s,d,z])
        MAP[r][c] = [s,d,z]
        """
        MAP = [
            ...
            [ ... [ [s,d,z] ], ... ] -> shark = MAP[r][c][0]
            ...
        ]
        """


    return R, C, M, sharks_data, MAP
    
dr = [-1,1,0,0]
dc = [0,0,1,-1]

def directionChanger(direction):
    if direction == 0:
        direction = 1
    elif direction == 1:
        direction = 0
    elif direction == 2:
        direction = 3
    elif direction == 3:
        direction = 2
    return direction

"""
런타임 에러 : ValueError가 발생하였다. 아마, remove하려고 했는데 remove의 대상이 없어서 생긴 것일 것이다.
"""
from collections import deque
def sharkMove(MAP, sharks_data, R, C):
    global total_combinations_list

    """sharkmoving for 1 timestep"""
    if sharks_data:
        for sh in range(len(sharks_data)):
            shark = sharks_data[sh]
            # r, c, 속력크기, 방향, 상어크기
            r, c, s, d, z = shark[0], shark[1], shark[2], shark[3], shark[4]
            # print(f"r, c, s, d, z = {r, c, s, d, z}")
            tmp_r, tmp_c = r, c

            if d == 0 or d == 1:
                if tmp_r+dr[d] == -1 or tmp_r+dr[d] == R:
                    d = directionChanger(d)
            elif d == 2 or d==3:
                if tmp_c+dc[d] == -1 or tmp_c+dc[d] == C:
                    d = directionChanger(d)

            for t in range(s):
                tmp_r, tmp_c = tmp_r + dr[d], tmp_c + dc[d]
                if d== 0 or d==1:
                    if tmp_r == 0 or tmp_r == R-1:
                        d = directionChanger(d)
                elif d == 2 or d == 3:        
                    if tmp_c == 0 or tmp_c == C-1:
                        d = directionChanger(d)
            sharks_data[sh] = [tmp_r, tmp_c, s, d, z]

        goodbye_sharks_list = []
        # # Q : 상어가 다 잡힌 경우는??
        # for i in range(0,len(sharks_data)-1):
        #     shark_one = sharks_data[i]
        #     for j in range(i+1, len(sharks_data)):
        #         shark_two = sharks_data[j]
        #         if (shark_one[0] == shark_two[0]) and (shark_one[1] == shark_two[1]):
        #             if shark_one[4] > shark_two[4]:
        #                 goodbye_sharks_list.append(shark_two)
        #             elif shark_one[4] < shark_two[4]:
        #                 goodbye_sharks_list.append(shark_one)
        
        total_combinations_list = []
        combinations(deque(), 0, 2, sharks_data)
        for shark_comb in total_combinations_list:
            shark_one, shark_two = shark_comb[0], shark_comb[1]
            if (shark_one[0] == shark_two[0]) and (shark_one[1] == shark_two[1]):
                    if shark_one[4] > shark_two[4]:
                        goodbye_sharks_list.append(shark_two)
                    elif shark_one[4] < shark_two[4]:
                        goodbye_sharks_list.append(shark_one)

        new_sharks_data = sharks_data[:]
        # print(f"sharks_data : {sharks_data}")
        # print(f"goodbye sharks! {goodbye_sharks_list}\n")
        if new_sharks_data:
            if goodbye_sharks_list:
                for gbyeSharks in goodbye_sharks_list:
                    # old_r, old_c = tmp_sharks_data[idx]

                    # MAP[old_r][old_c] = 0

                    new_sharks_data.remove(gbyeSharks)

        MAP = [[0]*C for _ in range(R)] # 지울 필요 없이 초기화
        # print(f"shark moved! before updating MAP: {sharks_data}")
        for sh in range(len(new_sharks_data)):
            shark = new_sharks_data[sh]
            r, c, s, d, z = shark[0], shark[1], shark[2], shark[3], shark[4]
            MAP[r][c] = [s, d, z]
        new_sharks_data = sharks_data

    return MAP, sharks_data

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

total_combinations_list = []
def combinations(queue, depth, r, target_list):
    global total_combinations_list
    n = len(target_list)
    if len(queue)==r:
        total_combinations_list.append(list(queue))
        return

    elif depth == n:
        return
    
    queue.append(target_list[depth])
    combinations(queue, depth+1, r, target_list)

    queue.pop()
    combinations(queue, depth+1, r, target_list)

def rotatedMAPIndexTransformer(fishingKingPos, C):
    fishingKingPos = C -1 - fishingKingPos
    return fishingKingPos

# def fishingKing(MAP, sharks_data, R, C):
#     fishingKingPos = -1
#     totalSharksWeight = 0
#     for f in range(C):
#         fishingKingPos += 1
#         rotatedMAP = [list(row) for row in list(zip(*MAP))[::-1]]
#         # print("rotatedMAP")
#         # MAP_printer(rotatedMAP)
#         rotatedFishingKingPos = rotatedMAPIndexTransformer(fishingKingPos, C)

#         fishingKingRow = rotatedMAP[rotatedFishingKingPos]
#         # print(f"fishingKingRow : {fishingKingRow}\n")
#         for fkr in range(len(fishingKingRow)):
#             if fishingKingRow[fkr] != 0:
#                 myFish = fishingKingRow[fkr]
#                 my_r, my_c, my_s, my_d, my_z = fkr, fishingKingPos, myFish[0], myFish[1], myFish[2]
#                 totalSharksWeight += myFish[2]
#                 # print(f"fish caught : {[my_r, my_c, my_s, my_d, my_z]}")

#                 sharks_data.remove([my_r, my_c, my_s, my_d, my_z])
#                 MAP[my_r][my_c] = 0
#                 break

#         # print(f"after fishingKing {sharks_data}")
#         # MAP_printer(MAP)

#         MAP, sharks_data = sharkMove(MAP, sharks_data, R, C)
#         # print(f"after sharkMove {sharks_data}")
#         # MAP_printer(MAP)
#     return totalSharksWeight

def fishingKing(MAP, sharks_data, R, C, fishingKingPos):
    if sharks_data:
        totalSharksWeight = 0
        
        fishingKingPos += 1
        rotatedMAP = [list(row) for row in list(zip(*MAP))[::-1]]
        # print("rotatedMAP")
        # MAP_printer(rotatedMAP)
        rotatedFishingKingPos = rotatedMAPIndexTransformer(fishingKingPos, C)

        fishingKingRow = rotatedMAP[rotatedFishingKingPos]
        # print(f"fishingKingRow : {fishingKingRow}\n")
        for fkr in range(len(fishingKingRow)):
            if fishingKingRow[fkr] != 0:
                myFish = fishingKingRow[fkr]
                my_r, my_c, my_s, my_d, my_z = fkr, fishingKingPos, myFish[0], myFish[1], myFish[2]
                totalSharksWeight += myFish[2]
                # print(f"fish caught : {[my_r, my_c, my_s, my_d, my_z]}")
                # print(f"sharks_data : {sharks_data}")
                # print(f"goodbye sharks! {[my_r, my_c, my_s, my_d, my_z]}\n")
                if sharks_data:
                    sharks_data.remove([my_r, my_c, my_s, my_d, my_z])
                MAP[my_r][my_c] = 0
                break

        # print(f"after fishingKing {sharks_data}")
        # MAP_printer(MAP)

        MAP, sharks_data = sharkMove(MAP, sharks_data, R, C)
        # print(f"after sharkMove {sharks_data}")
        # MAP_printer(MAP)
    return MAP, sharks_data, totalSharksWeight, fishingKingPos
            

if __name__ == "__main__":
    R, C, M, sharks_data, MAP = input_getter()
    ans = 0
  
    if M != 0:
        # print("INIT")
        # print(f"sharks_data : {sharks_data}")
        # MAP_printer(MAP)
        fishingKingPos = -1
        for time_lapse in range(C):
            MAP, sharks_data, totalSharksWeight, fishingKingPos = fishingKing(MAP, sharks_data, R, C, fishingKingPos)

            ans += totalSharksWeight



    print(ans)

"""
배운점

1. 3차원 자료구조를 다루는 연습이 되었다.
2. 인덱스 바운딩의 새로운 방식 : 계속 연속되는 방식이 아니라 되돌아오는 방식
    한 다른 아이디어에 의하면, 만약에 -1이 된 경우 거꾸로 방향으로 2를 더해주는 방식으로 했다고 한다.
    또 다른 아이디어에 의하면, 최종적으로 그래서 어떻게 되는지만 따져서 했다고 한다.
    그러나 공통점은, 시작할 때 처리를 해주어야 한다는 것이다.

3. iteration 돌리는 것은 함수 밖에서 하는 버릇을 들이자.
4. r,c 등을 애초에 input에서 받아올 때 1씩 빼놓는 버릇을 들이자.
5. 0에 대한 예외 처리 조건이 필요한지 반드시 확인하자.
"""