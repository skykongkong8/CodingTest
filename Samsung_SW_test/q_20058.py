# 마법사 상어와 파이어스톰
from collections import deque

dr = [1,-1,0,0]
dc = [0,0,1,-1]

def input_getter():
    N, Q = map(int, input().split(' '))
    mapLength = 2 ** N
    MAP = []
    
    for i in range(mapLength):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)
    

    L = list(map(int, input().split(' ')))

    return MAP, N, Q, mapLength, L

def cast_firestorm(MAP, mapLength, l):
    """파이어스톰의 규모대로 격자로 분해 후 시계방향 회전"""
    pieceLength = 2 ** l
    if pieceLength != 1:
        for r in range(0, mapLength, pieceLength):
            for c in range(0, mapLength, pieceLength):
                curPiece = [row[c:c+pieceLength] for row in MAP[r:r+pieceLength]] # 리스트에서 2차원 추출하는 방법!!!
                curR, curC = r, c
                
                rotatedPiece = list(zip(*curPiece[::-1])) # 2차원 리스트를 시계 방향 회전하는 방법!!!
                
                for j in range(curR, curR + pieceLength):
                    for k in range(curC, curC + pieceLength):
                        MAP[j][k] = rotatedPiece[j-curR][k-curC]

    # 녹는 것이 순차적이 아니라 한 번에 진행되므로
    melting_ice_idx_list = []

    for r in range(mapLength):
        for c in range(mapLength):
            adjacent_ice_cnt = 0

            for l in range(4):
                tmp_r, tmp_c = r+dr[l], c+dc[l]

                if 0<= tmp_r < mapLength and 0 <= tmp_c < mapLength:
                    if MAP[tmp_r][tmp_c] != 0:
                        adjacent_ice_cnt += 1

            if adjacent_ice_cnt < 3:
                melting_ice_idx_list.append([r,c])

    if melting_ice_idx_list:
        for index in melting_ice_idx_list:
            melt_r, melt_c = index[0], index[1]
            MAP[melt_r][melt_c] = max(MAP[melt_r][melt_c] -1, 0)

    return MAP

def compute_biggest_group(MAP, mapLength):
    """가장 큰 덩어리의 사이즈 (덩아리 자체까지)"""
    visited_MAP = [[False]*mapLength for _ in range(mapLength)]
    maxSize = 1
    zero_cnt = 0
    for m in range(mapLength):
        for n in range(mapLength):
            if MAP[m][n] == 0:
                zero_cnt += 1
                visited_MAP[m][n] = True
            if visited_MAP[m][n] == False and MAP[m][n] != 0: # 새로운 덩어리 init을 찾음

                queue = deque()
                queue.append([m,n])
                visited_MAP[m][n] = True
                tmpSize = 1

                while queue: # 덩어리 init당 dfs (최댓값이 아니라 덩어리 자체를 형성하기 위한)
                    curPos = queue.popleft()
                    for o in range(4):
                        tmp_m, tmp_n = curPos[0] + dr[o], curPos[1] + dc[o]
                        if 0 <= tmp_m < mapLength and 0 <= tmp_n < mapLength:
                            if visited_MAP[tmp_m][tmp_n] == False and  MAP[tmp_m][tmp_n] != 0:
                                visited_MAP[tmp_m][tmp_n] = True
                                queue.append([tmp_m, tmp_n])
                                tmpSize += 1
                
                maxSize = max(maxSize, tmpSize)

    if zero_cnt == mapLength * mapLength:
        return 0

    return maxSize

def count_total_ice(MAP, mapLength):
    """최종으로 남아있는 얼음의 양을 계산 후 리턴"""
    total_ice = 0
    for i in range(mapLength):
        for j in range(mapLength):
            total_ice += MAP[i][j]
    return total_ice


if __name__ == "__main__":
    MAP, N, Q, mapLength, L = input_getter()
    for q in range(Q):
        l = L[q]
        MAP = cast_firestorm(MAP, mapLength, l)

        # for row in MAP:
        #     print(row)
        # print()

    total_ice = count_total_ice(MAP, mapLength)
    maxSize = compute_biggest_group(MAP, mapLength)

    print(total_ice)
    print(maxSize)
    

"""
교훈
1. 2차원 리스트에서 2차원 배열을 numpy를 사용하지 않고 추출하는 법:
for r in range(0, mapLength, pieceLength):
    for c in range(0, mapLength, pieceLength):
        piece = [subRow[c:c+pieceLength] for subRow in MAP[r:r+pieceLength]]

2. 2차원 리스트를 회전시키는 법
CWrotatedPiece = list(zip(*piece[::-1]))
CCWrotatedPiece = list(zip(*piece))[::-1]

3. 예외처리말고 그냥 표준 쓰는 input으로 단수/중복 input 다 받을 수 있다는 것
4. r,c -1인덱싱 신경쓰자
5. 회전시킨 리스트를 다시 타일 맞추듯이 끼워넣는 법
6. range 인덱스 증강 카운트는 마지막이라는 것 (중간인 줄 알았음) 
7. dfs를 스스로 해내다니 감격스럽다.
"""