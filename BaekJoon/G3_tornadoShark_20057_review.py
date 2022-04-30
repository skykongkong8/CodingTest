# 토네이도 상어 리뷰

def input_getter():
    N = int(input())
    MAP = [] # 모래의 양 MAP
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))
    return N, MAP



dr = [0,1,0,-1]
dc = [1,0,-1,0]

def spiral_index(N):
    MAP = [[0]*N for _ in range(N)]
    linearized_indicies = []
    r = c = 0

    right = N -1
    down = N-1
    left = 0
    up = 1

    direction = 0
    # index = 0
    for n in range(N*N):
        # index += 1
        # MAP[r][c] = index
        linearized_indicies.append([r,c])
        if (direction%4) == 0 and c == right:
            direction += 1
            right -= 1
        elif (direction%4) == 1 and r == down:
            direction += 1
            down -= 1
        elif (direction%4) == 2 and c == left:
            direction += 1
            left += 1
        elif (direction%4) == 3 and r == up:
            direction += 1
            up += 1
        
        r += dr[direction%4]
        c += dc[direction%4]

    linearized_indicies.reverse()
    return linearized_indicies

def getDirection(r_1, c_1, r_2, c_2):
    direction = [r_2 - r_1, c_2 - c_1]
    return direction

def isThisIndexInMAP(N, idxR, idxC):
    if 0<= idxR < N and 0<= idxC <N:
        return True
    return False

# dr = [0,1,0,-1]
# dc = [1,0,-1,0]

directionIndexFormToNumberFormHasher = {
    (0,1) : 0,
    (1,0) : 1,
    (0,-1) : 2,
    (-1, 0) : 3
}

orthogonal_direction_hasher = {
    (0,1) : [1,0],
    (1,0) : [0,1],
    (0,-1) : [1,0],
    (-1, 0) : [0,1]
}

def orthogonal_direction(d):
    if d == 0 or 2:
        return [1,0]
    elif d == 1 or 3:
        return [0,1]

def get_dust_mask_indicies(tornado_r, tornado_c, direction):
    """토네이도의 이동 방향에 따라 모래가 튀기는 곳의 인덱스(와 모래의양? 비율?)들을 반환하는 함수"""
    #tornado_r, c는 '현재 위치'이다.
    d = directionIndexFormToNumberFormHasher[tuple(direction)]
    """
    dust_indicies = [
        ...,
        [ r, c, x% ]
        ...
    ]
    """
    

    # d_d = orthogonal_direction(d)
    d_d = orthogonal_direction_hasher[tuple(direction)]
    # print(f"orth dir : {d_d}")
    dust_indicies = []
    r = tornado_r
    c = tornado_c
    dust_indicies.append([r+d_d[0], c+d_d[1], 0.01])
    dust_indicies.append([r-d_d[0], c-d_d[1], 0.01])

    dust_indicies.append([r+dr[d]+d_d[0], c+dc[d]+d_d[1], 0.07])
    dust_indicies.append([r+dr[d]-d_d[0], c+dc[d]-d_d[1], 0.07])

    dust_indicies.append([r+dr[d]+2*d_d[0], c+dc[d]+2*d_d[1], 0.02])
    dust_indicies.append([r+dr[d]-2*d_d[0], c+dc[d]-2*d_d[1], 0.02])

    dust_indicies.append([r+2*dr[d], c+2*dc[d], "alpha"])

    dust_indicies.append([r+2*dr[d]+d_d[0], c+2*dc[d]+d_d[1], 0.1])
    dust_indicies.append([r+2*dr[d]-d_d[0], c+2*dc[d]-d_d[1], 0.1])

    dust_indicies.append([r+3*dr[d], c+3*dc[d], 0.05])


    return dust_indicies

from math import floor
total_dust_out = 0
def moveTornado(MAP, tornado_index_scenario):
    global total_dust_out
    for i in range(1,len(tornado_index_scenario)):
        curR, curC = tornado_index_scenario[i-1][0], tornado_index_scenario[i-1][1]
        nextR, nextC = tornado_index_scenario[i][0], tornado_index_scenario[i][1]
        DustInNextIdx = MAP[nextR][nextC]

        MAP[nextR][nextC] = 0

        direction = getDirection(curR, curC, nextR, nextC)
        dust_indicies = get_dust_mask_indicies(curR, curC, direction)
        # print(f"{curR, curC} with direction {direction} dust_indicies : {dust_indicies}\n")

        alpha = DustInNextIdx
        rememberAlphaIndex = None
        for d in range(len(dust_indicies)):
            dust = dust_indicies[d]
            dust_r, dust_c, dust_ratio = dust[0], dust[1], dust[2]
            if dust_ratio != "alpha":
                this_dustAmount = floor(DustInNextIdx*dust_ratio)
                # print(f"cur dustAmount for {dust_ratio} is {this_dustAmount}")
                alpha -= this_dustAmount

                if isThisIndexInMAP(N, dust_r, dust_c):
                    MAP[dust_r][dust_c] += this_dustAmount
                else:
                    total_dust_out += this_dustAmount

            elif dust_ratio == "alpha":
                rememberAlphaIndex = [dust_r, dust_c]

        alpha_r, alpha_c = rememberAlphaIndex[0], rememberAlphaIndex[1]
        # print(f"alphaIdx : {rememberAlphaIndex}\n")
        # print(f"alpha : {alpha}")

        if isThisIndexInMAP(N, alpha_r, alpha_c):
            MAP[alpha_r][alpha_c] += alpha
        else:
            total_dust_out += alpha


        







if __name__ == "__main__":
    N, MAP = input_getter()
    tornado_index_scenario = spiral_index(N)
    # print(f"tornado scenario : {tornado_index_scenario}\n")
    moveTornado(MAP, tornado_index_scenario)
    print(total_dust_out)

"""
토네이도 상어 리뷰
1. 노가다를 두려워 말라.. 결국 규칙이 있어서요령이 생긴다.
2. orthogonal한 벡터를 생성하는 마인드, spiral indexing 연습
"""