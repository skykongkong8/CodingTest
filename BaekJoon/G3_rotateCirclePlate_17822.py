# 원판 돌리기

"""
1. 원판 모델링 아이디어 : [] 물고 무는 1차원 리스트 (인접합 테스트할 때, 리스트 바운딩 해야함)

2. '인접'의 정의: 하드코딩
"""

def input_getter():
    N, M, T = map(int, input().split(' '))
    plate_list = []
    for _ in range(N):
        plate = list(map(int, input().split(' ')))
        plate_list.append(plate)

    rotating_strategies = []
    for _ in range(T):
        rotating_strategies.append(list(map(int, input().split(' '))))
    
    return N, M, T, plate_list, rotating_strategies

def index_bounder(j_r, M):
    # 원판 내 마지막 번째 수 다음을 첫 번째 수로, 첫번째수를 마지막 수로 인덱스 바운딩을 해주는 함수
    if j_r >= M:
        j_r -= M
    elif j_r < 0:
        j_r += M
    
    return j_r

def rotate_plate(plate, direction):
    """
    plate = [3, 1, 2, 1] 위-오른-아래-왼
    """
    if direction == 0: # Cw
        plate = [plate[-1]] + plate[:-1] # 왼-위-오른-아래

    elif direction == 1: # CCW
        plate = plate[1:] + [plate[0]] # 오른-아래-왼-위
    return plate

def rotate_x_i_multiple_plates(plate_list, x_i, k_i, d_i, N):

    for ki in range(k_i):
        tmp_plate_index = x_i
        while True:
            curPlate = plate_list[tmp_plate_index-1]
            plate_list[tmp_plate_index-1] = rotate_plate(curPlate, d_i)
            tmp_plate_index += x_i
            if tmp_plate_index > N:
                break
    return plate_list

from collections import deque

def delete_and_rotate(plate_list, rotating_strategy, N, M):
    x_i, d_i, k_i = rotating_strategy[0], rotating_strategy[1], rotating_strategy[2]
    
    global_visited = [[False]*M for _ in range(N)]
    total_plate_found_flag = False
    plate_adj_found_flag = [False]*N

    plate_list = rotate_x_i_multiple_plates(plate_list, x_i, k_i, d_i, N)
    # print(f"after rotating : ")
    # MAP_printer(plate_list)

    for i in range(N):       
        for j in range(M):
            curNum = plate_list[i][j]
            if curNum != False:
                if not global_visited[i][j]:                               
                    visited = [[False]*M for _ in range(N)]
                    queue = deque()
                    queue.append([i,j])
                    visited[i][j] = True
                    global_visited[i][j] = True

                    adj_found_flag = False
                    adjacent_connected_group = [[i,j]]
                    
                    while queue:
                        current_data = queue.pop()
                        current_i, current_j = current_data[0], current_data[1]

                        # 인덱스 +1-1 잘 점검하자.
                        if current_i == 0:
                            adj_indicies_list = [
                                [current_i, index_bounder(current_j-1, M)],
                                [current_i, index_bounder(current_j+1, M)],
                                [1, current_j]
                            ]
                        elif current_i == N-1:
                            adj_indicies_list = [
                                [current_i, index_bounder(current_j-1, M)],
                                [current_i, index_bounder(current_j+1, M)],
                                [N-2, current_j]
                            ]
                        else:
                            adj_indicies_list = [
                                [current_i, index_bounder(current_j-1, M)],
                                [current_i, index_bounder(current_j+1, M)],
                                [current_i-1, current_j],
                                [current_i+1, current_j]
                            ]
                        # print(f"adj_indicices : {adj_indicies_list}")

                        for k in range(len(adj_indicies_list)):
                            tmp_i, tmp_j = adj_indicies_list[k][0], adj_indicies_list[k][1]
                            adjNum = plate_list[tmp_i][tmp_j]

                            if not visited[tmp_i][tmp_j]:
                                visited[tmp_i][tmp_j] = True

                                if adjNum == curNum:
                                    adj_found_flag = True
                                    total_plate_found_flag = True

                                    plate_adj_found_flag[current_i] = True                                                            
                                    plate_adj_found_flag[tmp_i] = True

                                    global_visited[tmp_i][tmp_j] = True
                                    adjacent_connected_group.append([tmp_i, tmp_j])
                                    queue.append([tmp_i, tmp_j])
                        

                    if adj_found_flag:
                        for l in range(len(adjacent_connected_group)):
                            rem_i, rem_j = adjacent_connected_group[l][0], adjacent_connected_group[l][1]
                            plate_list[rem_i][rem_j] = False
                        # print(f"after adjacent POP : ")
                        # MAP_printer(plate_list)

    if not total_plate_found_flag:
        # for o in range(N):                
        #     if not plate_adj_found_flag[o]:
        #         this_plate = plate_list[o]
        #         plate_average = 0.0
        #         cnt = 0.0
        #         for m in range(len(this_plate)):
        #             if this_plate[m]:
        #                 plate_average += this_plate[m]
        #                 cnt +=1
        #         if cnt != 0:
        #             plate_average /= cnt
        #             print(f"plate_avg : {plate_average}")

        #             for m in range(len(this_plate)):
        #                 if this_plate[m]:
        #                     if this_plate[m] > plate_average:
        #                         plate_list[o][m] -= 1
        #                     elif this_plate[m] < plate_average:
        #                         plate_list[o][m] += 1
        # 설마 plate별로 하는게 아니고, 전체 plate기준으로의 평균이었던 것? -> 그런 것이었다.
        platesum, platecnt = get_total_plateSum(plate_list, N, M)
        if platecnt != 0:
            plate_average = platesum/platecnt
            for r in range(N):
                for c in range(M):
                    if plate_list[r][c]:
                        if plate_list[r][c] > plate_average:
                            plate_list[r][c] -= 1
                        elif plate_list[r][c] < plate_average:
                            plate_list[r][c] += 1

            # print(f"after non adj normalization : ")
            # MAP_printer(plate_list)
    return plate_list

def get_total_plateSum(plate_list, N, M):
    score = 0.0
    cnt = 0.0
    for i in range(N):
        for j in range(M):
            if plate_list[i][j]:
                score += plate_list[i][j]
                cnt += 1
    return score, cnt                              


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()


if __name__ == "__main__":
    N, M, T, plate_list, rotating_strategies = input_getter()
    for t in range(T):
        rotating_strategy = rotating_strategies[t]
        plate_list = delete_and_rotate(plate_list, rotating_strategy, N, M)
    ans, _ = get_total_plateSum(plate_list, N, M)

    print(int(ans))

"""
- 인덱스 바운딩 복습 : r,c 인덱싱 말고도 별도로 모델링된 형식의 인덱스도 바운딩할 수 있음
- 1차원 리스트를 circulating linked list처럼 다루는 방법: [] + [] 꼴로 재생성하기
- 별도의 neighboring 기준을 세운 dfs로 connected component찾기 : 아쉬운점: 이걸 곧이 곧대로 받아들이지 말고 2차원행렬에서는 어떻게
    적용되는 것인지에 대한 의미를 미리 파악했더라면 더욱 용이했을 듯
- 디버깅:
    테스트 케이스 답이 맞을지라도 MAP_printer로 확인해볼 것. 진행 상황이 다를 수 있다.

- 문제의 시뮬레이션 진행예시가 나와있다면 먼저보는 것도 좋을듯. 혼자 이해한대로 하다가 틀렸다.

"""