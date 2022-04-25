# 마법사 상어와 토네이도
from math import floor
import copy
MAP = []
dr = [1,-1,0,0]
dc = [0,0,1,-1]

def input_getter(MAP):
    N = int(input())
    for i in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)
    return N

def dust_swirl(MAP, curR, curC, desR, desC):
    """모래의 움직임을 관찰하고 그때마다 빠져나간 만큼의 모래 양을 반환하는 함수"""
    # MAP = copy.deepcopy(MAP)
    dustOut = 0
    curDir = [desR - curR, desC - curC]
    index_list = dust_swirl_index(curDir, curR, curC)

    total_dust = MAP[desR][desC]
    alpha_dust = total_dust

    if total_dust == 0:
        return MAP, 0

    for index in index_list:
        r, c, dust_ratio, isAlpha = index[0], index[1], index[2], index[3]
        if not isAlpha:
        
            curSwirlingDust = int(total_dust*dust_ratio)
            alpha_dust -= curSwirlingDust

            if 0<= r < len(MAP) and 0<= c < len(MAP[0]):
                MAP[r][c] += curSwirlingDust
            else:
                dustOut += curSwirlingDust

        if isAlpha:
            alpha_r, alpha_c = r, c
            
    if 0<= alpha_r < len(MAP) and 0<= alpha_c < len(MAP[0]):
        MAP[alpha_r][alpha_c] += int(alpha_dust)
        
    else:
        dustOut += int(alpha_dust)

    MAP[desR][desC] = 0

    # for row in MAP:
    #     print(row)
    # print()

    return MAP, dustOut

def check_if_zero_idx(curRow, curCol):
    if (curRow == 0 and curCol == 0):
        return True
    else:
        return False

def dust_swirl_index(dir,curR, curC):
    idx_list = []

    if dir == [0,1] or dir == [0, -1]:
        orthogonal_dir = [[1,0],[-1,0]]
        
    elif dir == [1,0] or dir == [-1,0]:
        orthogonal_dir = [[0,1],[0,-1]]
    
    for orthDir in orthogonal_dir:
        tmp_idx1 = [curR + orthDir[0], curC + orthDir[1], 0.01, False]
        # tmp_idx2 = [curR - orthDir[0], curC - orthDir[1]]

        tmp_idx3= [curR + dir[0] + orthDir[0], curC + dir[1] + orthDir[1], 0.07, False]
        # tmp_idx4 = [curR + dir[0] - orthDir[0], curC + dir[1] - orthDir[1]]

        tmp_idx5 = [curR + dir[0] + 2*orthDir[0], curC + dir[1] + 2*orthDir[1], 0.02, False]
        # tmp_idx6 = [curR + dir[0] - 2*orthDir[0], curC + dir[1] - 2*orthDir[1]]

        tmp_idx7 = [curR + 2*dir[0] + orthDir[0], curC + 2*dir[1] + orthDir[1], 0.1, False]
        # tmp_idx8 = [curR + 2*dir[0] - orthDir[0], curC + 2*dir[1] - orthDir[1]]

        idx_list.extend([tmp_idx1, tmp_idx3, tmp_idx5, tmp_idx7])

    tmp_idx_alpha = [curR + 2*dir[0], curC + 2*dir[1], 0.55, True]
    tmp_idx9 = [curR + 3*dir[0], curC + 3*dir[1], 0.05, False]

    idx_list.append(tmp_idx_alpha)
    idx_list.append(tmp_idx9)

    return idx_list

def tornado_move(MAP, curR, curC, cnt):
    flag = False
    cummulative_dust = 0
    cnt = 0
    while not (curR == 0 and curC == 0):
        # print(f"R : {curR}, C : {curC}, cnt : {cnt}")

        if cnt % 2 == 0:
            """좌->하 * cnt+1"""
            for i in range(cnt+1):
                desC = curC -1
                desR = curR

                MAP, curDust = dust_swirl(MAP, curR, curC, desR, desC)
                cummulative_dust += curDust

                curC = desC
                if check_if_zero_idx(curR, curC):
                    flag = True
                    break
            if flag:
                break
                

            for j in range(cnt+1):
                desR = curR +1
                desC = curC

                MAP, curDust = dust_swirl(MAP, curR, curC, desR, desC)
                cummulative_dust += curDust

                curR = desR
                if check_if_zero_idx(curR, curC):
                    flag = True
                    break
            if flag:
                break
                
        elif cnt % 2 == 1:
            """우->상 * cnt+1"""
            for k in range(cnt+1):
                desC = curC +1
                desR = curR

                MAP, curDust = dust_swirl(MAP, curR, curC, desR, desC)
                cummulative_dust += curDust

                curC = desC        
                if check_if_zero_idx(curR, curC):
                    flag = True
                    break  
            if flag:
                break
                
            for l in range(cnt+1):
                desR = curR - 1
                desC = curC

                MAP, curDust = dust_swirl(MAP, curR, curC, desR, desC)
                cummulative_dust += curDust

                curR = desR
                if check_if_zero_idx(curR, curC):
                    flag = True
                    break
            
            if flag:
                break
        cnt += 1


    return cummulative_dust



if __name__ == '__main__':
    N = input_getter(MAP)
    init_r, init_c = floor(N/2), floor(N/2)
    total_dust = tornado_move(MAP, init_r, init_c, 0)

    print(total_dust)
