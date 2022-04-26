# 주사위 굴리기

def input_getter():
    N, M, x, y, K = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))
    dice_roll_direction = list(map(int, input().split(' ')))
    return MAP, N, M, x, y, K, dice_roll_direction


def new_dice():
    newdice = [
    0, # TOP : 0
    0, # 동 : 1
    0, # 서 : 2
    0, # 남 : 3
    0, # 북 : 4
    0 # BOTTOM : 5
]
    return newdice

def roll_dice(dice, direction):
    newdice = new_dice()
    if direction == 1:
        # 동쪽 roll = 남북은 안바뀌고, next동 1 = curTop 0, nextTop 0이 cur서 2, next서 2 가 curBottom 5, nextBottom 5 이 cur동 1
        newdice[0] = dice[2]
        newdice[1] = dice[0]
        newdice[2] = dice[5]
        newdice[3] = dice[3]
        newdice[4] = dice[4]
        newdice[5] = dice[1]

        return newdice
    elif direction == 2:
        # 서쪽 roll = 남북은 안바뀌고, next서 2 = curTop 0, nextTop 0 = cur동 1, next동 1 = curBottom 5, nextBottom 5 = cur서 2
        newdice[0] = dice[1]
        newdice[1] = dice[5]
        newdice[2] = dice[0]
        newdice[3] = dice[3]
        newdice[4] = dice[4]
        newdice[5] = dice[2]

    elif direction == 3:
        # 북쪽 roll = 동서 안바뀌고, nextTop 0 = cur남 3, next 남 3 = curBottom 5 , nextBottom 5 = cur북 4 , cur북 4  = curTop 0
        newdice[0] = dice[3]
        newdice[1] = dice[1]
        newdice[2] = dice[2]
        newdice[3] = dice[5]
        newdice[4] = dice[0]
        newdice[5] = dice[4]

    elif direction == 4:
        # 남쪽 roll = 동서 안바뀌고, nextTop 0 = cur북 4 , next북 4 = curBottom 5 , nextBottom 5 = cur남 3 , next남 3  = curTop 0 
        newdice[0] = dice[4]
        newdice[1] = dice[1]
        newdice[2] = dice[2]
        newdice[3] = dice[0]
        newdice[4] = dice[5]
        newdice[5] = dice[3]
        
    return newdice

dice_roll_direction_index_hash = {
    1 : [0,1],
    2 : [0, -1],
    3 : [-1,0],
    4 : [1,0]
}

dsnb_korean_hash = {
    1 : '동',
    2 : '서',
    3 : '북',
    4 : '남'

}
def game(MAP, dice, dice_roll_direction, x, y, N, M):
    r, c = x, y
    for i in range(len(dice_roll_direction)):
        dsnb = dice_roll_direction[i]
        dr, dc = dice_roll_direction_index_hash[dsnb][0], dice_roll_direction_index_hash[dsnb][1]
        tmp_r, tmp_c = r + dr, c + dc

        if 0 <= tmp_r < N and 0<= tmp_c < M:
            r, c = tmp_r, tmp_c
            # print(f"dice roll to {dsnb_korean_hash[dsnb]} move to {r, c}")


            dice = roll_dice(dice, dsnb)
            # print(f"dice rolled to {dsnb}")

            if MAP[r][c] == 0:
                MAP[r][c] = dice[5]
            elif MAP[r][c] != 0:
                dice[5] = MAP[r][c]
                MAP[r][c] = 0

            # MAP_printer(MAP)

            print(dice[0])
        else:
            pass

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

if __name__ == "__main__":
    MAP, N, M, x, y, K, dice_roll_direction = input_getter()

    init_dice = new_dice()
    game(MAP, init_dice, dice_roll_direction, x, y, N, M)


"""
배운점

1. 주사위를 코드상에서 모델링하는 테크닉 복습.
    일차원 리스트로 구상한 뒤, rolldice 메소드를 생성해주면 된다.

    rolldice메소드는 newdice를 생성한 후 각각의 주사위눈을 받아오는데 이때, 무엇으로 <- 무엇이 바뀌는지
    기술하면서 코드를 작성하면 (그리고 안변하는것도 있으므로) 코드 짤 때 실수할 확률이 적고, 하더라도 디버깅하기 편해진다.

2. 말고는 특별할 것 없었음. 
"""