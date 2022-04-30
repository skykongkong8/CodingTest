# 파이어볼 리뷰

def input_getter():
    N, M, K = map(int, input().split(' '))
    fireballs = []
    for _ in range(M):
        r, c, m, s, d = map(int, input().split(' '))
        r -= 1
        c -= 1
        # d -= 1/
        fireballs.append([r, c, m, s, d])
    
    MAP = [[0]*N for _ in range(N)]

    for r in range(N):
        for c in range(N):
            MAP[r][c] = list()

    for fireball in fireballs:
        r, c, m, s, d = fireball[0], fireball[1], fireball[2], fireball[3], fireball[4]
        MAP[r][c].append([m,s,d])

    return N, M, K, fireballs, MAP

dr = [-1,-1,0,1,1,1,0,-1]
dc = [0,1,1,1,0,-1,-1,-1]

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

def index_bounder(r,c, N):
    if r <0:
        r += N
    elif r >= N:
        r -= N

    if c < 0:
        c += N
    elif c >= N:
        c -= N

    return r, c

def moveFireballs(MAP, fireballs, N):
    for fb in range(len(fireballs)):
        fireball = fireballs[fb]
        """
        fireball = [ r, c, m, s, d]
        """
        curR, curC, curM, curS, curD = fireball[0], fireball[1], fireball[2], fireball[3], fireball[4]
        MAP[curR][curC].remove([curM, curS, curD])       

        tmp_r, tmp_c = curR, curC
        for s in range(curS):
            tmp_r, tmp_c = tmp_r + dr[curD], tmp_c + dc[curD]
            tmp_r, tmp_c = index_bounder(tmp_r, tmp_c, N)
        
        fireballs[fb] = [tmp_r, tmp_c, curM, curS, curD]  
        MAP[tmp_r][tmp_c].append([curM, curS, curD]) 



    # 디버깅을 위한 MAP 반영 ? 혹은, 나중에 fireball은 정말 많이 생길 수도 있으니까 속도를 잡기 위한 MAP 반영

    
    

    return fireballs, MAP

def get_divided_fireballs_directions(isAllEvenOrOdd):
    if isAllEvenOrOdd:
        return [0,2,4,6]
    else:
        return [1,3,5,7]
        
from math import floor
def fireBallProcessing(MAP, fireballs):

    for row in range(N):
        for col in range(N):
            # print(f"num of fireballs in this index : {len(MAP[row][col])}")
            if len(MAP[row][col]) >= 2:
                fireballSeries = MAP[row][col]
                massSum = 0
                speedSum = 0
                count = 0
                isAllEvenOrAllOdd = True
                evenOrOddComparingNum = fireballSeries[0][2]

                for individ_fireball in fireballSeries:
                    m, s, d = individ_fireball[0], individ_fireball[1], individ_fireball[2]
                    # fireballs.remove([row, col, m, s, d])
                    massSum += m
                    speedSum += s
                    count += 1
                    if isAllEvenOrAllOdd:
                        if evenOrOddComparingNum%2 != d%2:
                            isAllEvenOrAllOdd = False
                
                seriesMass = floor(massSum/5)
                if seriesMass != 0:
                    seriesSpeed = floor(speedSum/count)
                    seriesDirectionList = get_divided_fireballs_directions(isAllEvenOrAllOdd)

                    new_series = []
                    for newDir in seriesDirectionList:
                        new_series.append([seriesMass, seriesSpeed, newDir])
                        fireballs.append([row, col, seriesMass, seriesSpeed, newDir])
                    


                    MAP[row][col] = new_series
                else:
                    MAP[row][col] = list()
    fireballs = get_fireballs_from_MAP(MAP)
    return MAP, fireballs
                

def get_fireballs_from_MAP(MAP):
    fireballs= []
    for a in range(N):
        for b in range(N):
            if MAP[a][b]:
                for c in range(len(MAP[a][b])):
                    fireball = [a,b]
                    fireball.extend(MAP[a][b][c])
                    fireballs.append(fireball)
    return fireballs

            


def getFinalMass(MAP):
    ans = 0
    for r in range(N):
        for c in range(N):
            if MAP[r][c]:
                for l in range(len(MAP[r][c])):
                    ans += MAP[r][c][l][0]
    return ans






if __name__ == "__main__":
    N, M, K, fireballs, MAP = input_getter()
    # print(f"init MAP:")
    # MAP_printer(MAP)
    # print(f"init fireballs : {fireballs}")

    for k in range(K):

        fireballs, MAP = moveFireballs(MAP, fireballs, N)
        # print("after fireball move:")
        # MAP_printer(MAP)
        # print(f"fireballs : {fireballs}")


        MAP, fireballs = fireBallProcessing(MAP, fireballs)
        # print("after fireball processing")
        # MAP_printer(MAP)

    ans = getFinalMass(MAP)
    print(ans)

"""
파이어볼 리뷰
1. 확실히 '삭제'는 굉장히 까다로운 것인데, 그래서 'remove'는 지양하는 것이 좋다. 대신:
    -아예 초기화하고 다시 받아오기
    - 이중 반복문을 돌면서 MAP에서 아예 처음부터 받아오기

    이게 훨씬 빠르다!

    특히, fireball 처럼 계속해서 4개씩 불어나는 친구일 경우에는, 눈치껏, remove 등 보다는,
    아예 제로로 초기화한 뒤, 새로 업데이트 된 MAP에서 데이터를 재생성하는 것이 좋다.
"""