# 마법사 상어와 파이어볼
dr = [-1,-1,0,1,1,1,0,-1]
dc = [0,1,1,1,0,-1,-1,-1]

def input_getter():
    N, M, K = map(int, input().split(' '))
    MAP = [[False]*N for _ in range(N)] # MAP은 N*N의 공간의 한 칸 당 파이어볼 리스트를 저장하고 있는 자료 구조
    for i in range(N):
        for j in range(N):
            MAP[i][j] = []

    
    for i in range(M):
        r, c, m, s, d = map(int, input().split(' '))
        r -= 1
        c -= 1
        fireball = [m, s, d, False] # 파이어볼 리스트에는 파이어볼 오브젝트가 저장되어 있으며, mass, speed, direction, isMovedBool 로 구성

        MAP[r][c].append(fireball)
    return MAP, N, M, K

def move_initializer(MAP, N):
    for m in range(N):
        for n in range(N):
            if MAP[m][n]:
                for fireball in MAP[m][n]:
                    fireball[-1] = False
    return MAP

def index_bounder(r, c, N):
    """0번 인덱스와 마지막 인덱스(N-1)를 계속해서 이어주기 위한 함수"""

    if r < 0:
        r += N
    elif r >=N:
        r -= N

    if c < 0:
        c += N
    elif c >=N:
        c -= N

    return r, c

def move_fireball(MAP, N, K):
    """규칙에 맞게 파이어볼을 이동시키는 함수 -> 함수 밖에서 K번 루프해주자."""
    for a in range(K):
        for i in range(N):
            for j in range(N):
                if MAP[i][j]:
                    for fireball in MAP[i][j][:]: # 이렇게 [:]를 통해서 복사본의 리스트를 주면 remove와 이동을 함께 쓸수있음!
                        if fireball[-1] == False:
                            curFireball = fireball
                            
                            curR, curC, curS, curD = i, j, curFireball[1], curFireball[2]
                            curDirection = [dr[curD], dc[curD]]

                            desR, desC = curR, curC

                            for l in range(curS):
                                desR = desR + curDirection[0]
                                desC = desC + curDirection[1]

                                desR, desC = index_bounder(desR, desC, N)

                            curFireball[-1] = True
                            MAP[desR][desC].append(curFireball)
                            MAP[curR][curC].remove(curFireball)
                            
                            # for row in MAP:
                            #     print(row)
                            # print()
                    
        MAP = move_initializer(MAP, N)

        # 이동 끝: 합치기/나누기 시작
        MAP = create_one_big_fireball_and_divide(MAP, N)

    return MAP


def create_one_big_fireball_and_divide(MAP, N):
    """같은 칸에 있는 파이어볼을 모두 합쳐서 하나의 큰 파이어볼[m,s,d]을 만드는 함수"""
    for z in range(N):
        for x in range(N):
            if MAP[z][x]:
                if len(MAP[z][x]) >= 2:

                    oddOrEvenBoolean = check_if_all_fireballSpeeds_in_fireballList_are_even_or_odd(MAP[z][x])
                    
                    totalMass = 0
                    totalSpeed = 0
                    totalNum = 0
                    
                    for fireball in MAP[z][x]:
                        totalMass += fireball[0]
                        totalSpeed += fireball[1]
                        totalNum +=1

                    segmentMass = int(totalMass/5)
                    
                    MAP[z][x] = []
                    if segmentMass > 0:
                        if oddOrEvenBoolean:
                            direction_list = [0,2,4,6]
                        else:
                            direction_list = [1,3,5,7]

                        
                        for v in range(len(direction_list)):
                            MAP[z][x].append([segmentMass, int(totalSpeed/totalNum), direction_list[v], False])

    return MAP


def check_if_all_fireballSpeeds_in_fireballList_are_even_or_odd(fireballList):
    criterion = (fireballList[0][2] % 2)
    for fireball in fireballList:
        if fireball[2] % 2 != criterion:
            return False
    return True

        
def get_total_fireball_mass(MAP, N):
    """MAP을 1회 순환하여 남아있는 fireball들의 총합 질량을 계산하는 함수"""
    totalMass = 0
    for i in range(N):
        for j in range(N):
            if MAP[i][j] is not None or MAP[i][j]:
                for fireball in MAP[i][j]:
                    totalMass += fireball[0]
    return totalMass

    

if __name__ == "__main__":
    MAP, N, M, K = input_getter()

    # for row in MAP:
    #     print(row)
    # print()
    
    MAP = move_fireball(MAP, N, K)

    answer = get_total_fireball_mass(MAP, N)

    print(answer)

