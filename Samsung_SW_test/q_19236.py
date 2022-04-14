# 청소년 상어

import copy

dr = [-1,-1,0,1,1,1,0,-1]
dc = [0,-1,-1,-1,0,1,1,1]
MAP = []

def input_getter(MAP):
    for i in range(4):
        this_input = list(map(int, input().split(' ')))
        this_row = []
        for j in range(4):
            fish = [this_input[2*j], this_input[2*j+1]-1]
            this_row.append(fish)
        MAP.append(this_row)
    return MAP

def find_fish_with_fishnum(MAP, fishnum):
    for r in range(len(MAP)):
        for c in range(len(MAP[0])):
            if MAP[r][c][0] == fishnum:
                return [r, c]
    return None

def move_fish(MAP, shark_r, shark_c):
    for i in range(1, 17):
        curRC = find_fish_with_fishnum(MAP, i)
        if curRC == None:
            continue

        curR, curC = curRC[0], curRC[1]
        curFish = MAP[curR][curC]
        curDir = curFish[1]
        for _ in range(8):            
            tmp_r, tmp_c = curR + dr[curDir], curC + dc[curDir]

            if 0<= tmp_r < 4 and 0 <= tmp_c < 4:
                if not (tmp_r == shark_r and  tmp_c == shark_c):
                    MAP[curR][curC][0], MAP[tmp_r][tmp_c][0] = MAP[tmp_r][tmp_c][0], MAP[curR][curC][0]
                    MAP[curR][curC][1], MAP[tmp_r][tmp_c][1] = MAP[tmp_r][tmp_c][1], curDir

                    break
            
            curDir = (curDir + 1)%8

def  get_edible_fishes(MAP, shark_r, shark_c, shark_direction):
    # shark_dir = shark_direction
    shark_dir = MAP[shark_r][shark_c][1]
    fish_rc_list = []
    for i in range(1,4):
        tmp_r, tmp_c = shark_r + dr[shark_dir], shark_c + dc[shark_dir]
        if 0<= tmp_r < 4 and 0<=tmp_c < 4 and (1 <= MAP[tmp_r][tmp_c][0] <= 16):
            fish_rc_list.append([tmp_r, tmp_c])
        shark_r, shark_c = tmp_r, tmp_c
    return fish_rc_list

def dfs(MAP, shark_r, shark_c, fishNum):
    MAP = copy.deepcopy(MAP)
    
    number = MAP[shark_r][shark_c][0]
    direction =  MAP[shark_r][shark_c][1]
    MAP[shark_r][shark_c][0] = -1
    
    move_fish(MAP, shark_r, shark_c)

    edible_fishes = get_edible_fishes(MAP, shark_r, shark_c, direction)

    global answer
    answer = max(answer, fishNum + number)

    for fishrc in edible_fishes:
        fish_r, fish_c = fishrc[0], fishrc[1]
        dfs(MAP, fish_r, fish_c, fishNum + number)




if __name__ == "__main__":
    MAP = input_getter(MAP)
    # game init
    answer = 0
    dfs(MAP, 0,0,0)

    print(answer)

"""
이번 문제에서 배운 점
1. deepcopy의 재귀적 사용
2. global 변수의 재귀적 사용 : 특히, max함수로 지속적으로 업데이트하면서 관리하면 자동으로 백트래킹이 된다는 점이 매우 인상깊음
3. python에서의 간단한 swap구현
4. class를 쓴다는게 생각보다 좋지 않다는 것
5. drdc 8개로도 인덱싱할 수 있다는 것
6. find_fish_with_fishnum과 같은 강력한 함수 참 좋다.
7. input_getter에서 홀수짝수인덱싱
"""


# TRY 1
# # 청소년 상어
# from collections import deque
# import sys

# dr = [-1, -1, 0, 1, 1, 1, 0, -1] # 번호순서 1~8 (인덱스 - 1)
# dc = [0, -1, -1, -1, 0, 1, 1, 1]

# class Shark():
#     def __init__(self):
#         self.curPos = None
#         self.curDir = None
#         self.totalNum = 0

#         self.home = False


# class Fish():
#     def __init__(self):
#         self.curPos = None
#         self.curDir = None
#         self.num = 0

#         self.eaten = False #?

# MAP = [[0]*4 for _ in range(4)]
# total_fish_list = []

# def input_getter():
#     for i in range(4):
#         mixed_row = list(map(int, sys.stdin.readline().split(' ')))
#         for j in range(4):
#             fish_idx = 2*j
#             fish_num = mixed_row[fish_idx]

#             dir_idx = 2*j + 1
#             dir_idx = mixed_row[dir_idx]

#             new_fish = Fish()
#             new_fish.num = fish_num
#             # new_fish.curDir = [dr[dir_idx-1], dc[dir_idx-1]]
#             new_fish.curDir = dir_idx - 1
#             new_fish.curPos = [i,j]

#             MAP[i][j] = new_fish                        # 전체 맵의 상황
#             total_fish_list.append(new_fish)            # 물고기 추적을 쉽게 하기 위한 자료구조+
#     total_fish_list.sort(key = lambda x : x.num)        # 물고기 번호 오름차순으로 정렬

# def fish_map_printer():
#     tmp_map = [[0]*4 for _ in range(4)]
#     for i in range(4):
#         for j in range(4):
#             tmp_map[i][j] = MAP[i][j].num
#     for i in range(4):
#         print(tmp_map[i])
#     print()


# def game():
#     #1 init : 상어가 0,0에 들어가서 먹는다.
#     shark = Shark()
#     first_fish = MAP[0][0]
#     shark.curPos = first_fish.curPos
#     shark.curDir = first_fish.curDir
#     shark.totalNum += first_fish.num
#     MAP[0][0] = 0

#     while True:
#         #2 물고기가 이동한다.
#         # 주의: 현재 MAP과 List 두 가지의 자료형을 사용하고 있으므로 양쪽 모두를 업데이트해주어야 함
#         for fish in total_fish_list: # 작은 순서대로의 물고기 대입
#             # 모든 방향을 돌며 이동이 가능한지 확인한다.
#             for i in range(8):
#                 # 현재 방향으로 부터 반시계방향으로 돌기 시작하며 확인한다.
#                 dir_index = (fish.curDir + i)%8
#                 tmp_dr = fish.curPos[0] + dr[dir_index]
#                 tmp_dc = fish.curPos[1] + dc[dir_index]

#                 # 이동이 불가능한 경우 :  범위 안이 아님 OR 상어칸임
#                 if (not (0 <= tmp_dr < 4 and 0 <= tmp_dc <4)) or (tmp_dr == shark.curPos[0] and tmp_dc == shark.curPos[1]):
#                     continue

#                 # 이동이 가능한 경우1 : 빈칸 - 그 칸으로 이동
#                 if not MAP[tmp_dr][tmp_dc]:
#                     MAP[fish.curPos[0]][fish.curPos[1]] = 0 # map에서의 원래 위치 없애기
#                     fish.curPos = [tmp_dr, tmp_dr] # 물고기 내장 정보 변경 : 위치
#                     fish.curDir = dir_index # 물고기 내장 정보 변경 : 방향
#                     for f in total_fish_list:
#                         if f.num == fish.num:
#                             f.curPos = [tmp_dr, tmp_dc]
#                             f.curDir = dir_index
#                     MAP[tmp_dr][tmp_dc] = fish # map에서의 정보 업데이트


#                 # 이동이 가능한 경우2 다른 물고기칸 - switch
#                 elif MAP[tmp_dr][tmp_dc].num:
#                     # fish의 정보를 바꿔준 후, MAP에 새로 fish를 집어넣는다.
#                     # tmp r,c : 이번 물고기가 가야할 위치
#                     # r,c : 이번 물고기의 기존 위치 = 상대 물고기가 와야할 위치

#                     tmp_fish = MAP[tmp_dr][tmp_dc]
#                     r = fish.curPos[0]
#                     c = fish.curPos[1]

#                     tmp_fish.curPos = [r,c] # fish 바꾸고
#                     for f in total_fish_list:
#                         if f.num == tmp_fish.num:
#                             f.curPos = [r,c]
#                     MAP[r][c] = tmp_fish # map에

#                     fish.curPos = [tmp_dr, tmp_dc] # fish 바꾸고
#                     fish.curDir = dir_index
#                     for f in total_fish_list:
#                         if f.num == fish.num:
#                             f.curPos = [tmp_dr, tmp_dc]
#                             f.curDir = dir_index
#                     MAP[tmp_dr][tmp_dc] = fish # map에

#         #3 상어가 이동한다.
#         death_cnt = 0
#         for i in range(8):
#             death_cnt += 1
#             shark_dir_idx = (shark.curDir + i)%8
#             shark_tmp_r = shark.curPos[0] + dr[shark_dir_idx]
#             shark_tmp_c = shark.curPos[1] + dc[shark_dir_idx]

#             # 상어가 이동하는 경우: 물고기가 있는 경우
#             # 이동하는 경우 중 선택의 순간이 찾아온다 : 이번 방향에 여러 마리의 물고기가 있는 경우 -> 누구를 먹어야 추후의 최대 번호를 먹을 수 있을까?
#             # 최댓값 optimizing 방법... 아이디어1 : BruteForce? 아이디어2: 무지성Greedy? 아이디어3: 가장 가장자리부터?
#             # 4x4인 이유가 설마 Brute Force라서? -> dfs 사용해야함!!!
#             if (0 <= shark_tmp_r < 4 and 0 <= shark_tmp_c < 4):
#                 if MAP[shark_tmp_r][shark_tmp_c]: # 이쪽 방향으로 이동이 가능하다면,
                    
#                     # 이쪽 방향으로 가능한 모든 인덱스를 찾는다.
#                     possible_idxes = []
#                     for j in range(4):
#                         tmp_tmp_r = shark_tmp_r + dr[shark_dir_idx]*(j)
#                         tmp_tmp_c = shark_tmp_c + dc[shark_dir_idx]*(j)
#                         if (0 <= tmp_tmp_r < 4 and 0 <= tmp_tmp_c < 4) and MAP[tmp_tmp_r][tmp_tmp_c]:
#                             possible_idxes.append([tmp_tmp_r, tmp_tmp_c])

#                         else: # 한번이라도 이쪽 방향으로 없으면 더이상 안찾아도 된다
#                             break

#                     # 이제 가능한 물고기 후보군들 중 최댓값을 줄 물고기를 선택하면 된다.
#                     # 이거 어떻게 함..??? (거의 minimax급 아님?)
#                     if possible_idxes:
#                         if len(possible_idxes) >=2:
#                             optimal_fish_idx = dfs(possible_idxes)
#                         else:
#                             optimal_fish_idx = possible_idxes[0]

#                         optimal_fish = MAP[optimal_fish_idx[0]][optimal_fish_idx[1]]

#                         # 정보 먹기
#                         shark.curDir = optimal_fish.curDir
#                         shark.curPos = optimal_fish.curPos
#                         shark.totalNum += optimal_fish.num
                        
#                         # total_fish_list 에서 삭제
#                         for delete_candidate in total_fish_list:
#                             if delete_candidate.num == optimal_fish.num:
#                                 total_fish_list.remove(delete_candidate)
#                                 break
                        
#                         # map에서 삭제
#                         MAP[optimal_fish.curDir[0]][optimal_fish.curDir[1]] = 0
#                         break

#             if death_cnt == 8:
#                 shark.home = True
#             # 모든 방향으로 물고기가 없으면, 이동이 불가하므로 집에 게임을 종료한다.
#         if shark.home == True:
#             break
#     print(shark.totalNum)

# def dfs(possible_indicies):
#     value_list = []
    
#     for fish_index in possible_indicies:
#         score = 0
#         stack = deque()
#         stack.append(MAP[fish_index[0]][fish_index[1]])
#         tmp_map = MAP.copy()
#         while stack:
#             curfish = stack.pop()
#             score+= curfish.num
#             tmp_map[curfish.curPos[0]][curfish.curPos[1]] = 0

#             for i in range(8):
#                 curDir = (curfish.curDir + i)%8
#                 r = curfish.curPos[0] + dr[curDir]
#                 c = curfish.curPos[1] + dc[curDir]

#                 if (0<=r<4 and 0<=c <4) and tmp_map[r][c]:
#                     stack.append(tmp_map[r][c])
            
            
#         value_list.append([score, fish_index])
#     value_list.sort(key = lambda x: x[0], reverse = True) # 내림차순 정렬

#     return value_list[0][1]
            




# # 실행 부분
# if __name__ == "__main__":
#     input_getter()
#     fish_map_printer()
#     game()
