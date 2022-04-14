# 마법사 상어와 비바라기
import sys
dr = [0,-1,-1,-1,0,1,1,1]
dc = [-1,-1,0,1,1,1,0,-1]

diag_dr = [-1,-1,1,1]
diag_dc = [-1,1,1,-1]

def input_getter():
    # N, M = map(int, input().split(' '))
    N, M = map(int, sys.stdin.readline().split(' '))

    MAP = []
    ds_list = []

    for _ in range(N):
        # this_row = list(map(int, input().split(' ')))
        this_row = list(map(int, sys.stdin.readline().split(' ')))

        MAP.append(this_row)

    for _ in range(M):
        # ds = list(map(int, input().split(' ')))
        ds = list(map(int, sys.stdin.readline().split(' ')))
        ds_list.append(ds)

    return N, M, MAP, ds_list


def index_bounder(current_R, current_C, N):
    """인덱스가 빠져나가지 않도록 연결해주는 함수"""
    if current_R < 0:
        current_R += N
    elif current_R >= N:
        current_R -= N

    if current_C < 0:
        current_C += N
    elif current_C >= N:
        current_C -= N

    return current_R, current_C

def move_clouds(MAP, ds, N, cloud_indicies):
    """비구름을 이동시킨 후, 비를 내리는 함수"""
    #1 모든 비구름의 ds 적힌 대로 이동, 물의 양 += 1
    curD, curS = ds[0], ds[1]
    cur_dr, cur_dc = dr[curD-1], dc[curD-1]

    new_cloud_indicies = []

    for index in cloud_indicies:
        curR, curC = index[0], index[1]
        desR, desC = curR, curC
        for s in range(curS):
            desR, desC = desR + cur_dr, desC + cur_dc
            desR, desC = index_bounder(desR, desC, N)

        new_cloud_indicies.append([desR, desC])
    
    for newIndex in new_cloud_indicies:
        r, c = newIndex[0], newIndex[1]
        MAP[r][c] += 1

    
    #2 구름이 모두 사라지고, 이때의 인덱스를 기억해야함
    # 사라진 구름의 인덱스가 new_cloud_indicies에 저장되어있다.
    cloud_indicies = []

    #3 물복사 버그 : 대각선 방향 으로 탐색하여 물이 있는 대각선 칸만큼 물증가
    for newIndex in new_cloud_indicies:
        moreThanTwoWaterCnt = 0
        r, c = newIndex[0], newIndex[1]
        for k in range(4):
            tmp_r, tmp_c = r + diag_dr[k], c + diag_dc[k]
            if 0 <= tmp_r < N and 0 <= tmp_c < N:
                if MAP[tmp_r][tmp_c] > 0:
                    moreThanTwoWaterCnt += 1
        MAP[r][c] += moreThanTwoWaterCnt


    #4 물 감소 : 2에서 얻은 인덱스를 제외하고 물의 양이 2 이상인 모든 칸에 구름 생성 및 물의 양 -=2
    for i in range(N):
        for j in range(N):
            if MAP[i][j] >= 2:
                if [i, j] not in new_cloud_indicies:
                    MAP[i][j] = max(0, MAP[i][j] - 2)                
                    cloud_indicies.append([i,j])
    
    # cloud_indicies와 MAP을 반환하고 밖에서 indicies를 받아 업데이트하면서 반복문을 돌려주자.

    return MAP, cloud_indicies


def total_water(MAP, N):
    """모든 이동이 끝난 후 모든 물의 양을 구하는 함수"""
    total_water = 0
    for i in range(N):
        for j in range(N):
            total_water += MAP[i][j]
    return total_water

if __name__ == "__main__":
    N, M, MAP, ds_list = input_getter()
    cloud_indicies = [[N-1, 0], [N-1, 1], [N-2, 0], [N-2, 1]]
    for m in range(M):
        MAP, cloud_indicies = move_clouds(MAP, ds_list[m], N, cloud_indicies)

        # for row in MAP:
        #     print(row)
        # print()

    answer = total_water(MAP, N)

    print(answer)
