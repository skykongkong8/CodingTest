# 마법사 상어와 블리자드


def input_getter():
    N, M = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)

    BLIZZARD = []
    for _ in range(M):
        BLIZZARD.append(list(map(int, input().split(' '))))
    
    return N, M, MAP, BLIZZARD

Explode_One = 0
Explode_Two = 0
Explode_Three = 0

"""
아이디어 
- 우선 골뱅이처럼 돌아가면서 인덱싱을 자유자재로 할 수 있어야 되겠고,
- 이거를 일차원식처럼 펴서 생각을 하면서 변환하면서 인덱싱을 할 수 있어야 하겠다. (땡기고 늘이고 없애는 과정에서 이런게 필요함)

인덱싱변환이라함은! :
(일반 인덱스 : 0, 1, 2, 3 ...) -> [transformation function] -> (회전인덱스 : ((N+1)/2 -1,(N+1)/2 -1),((N+1)/2 -1,(N+1)/2 -2), ... )
"""

def formulate_circulating_MAP(N):
    """
    방금전까지 sprial MAP에 대해 따로 공부하고 왔다. 테크닉을 적용하여 보자.
    """
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    cnt = 0
    # spiralMAP = [[0]*N for _ in range(N)]
    linearized_spiralMAP = [] # 왠지 이런게 필요할 것 같지 않아? 
    r = 0
    c = 0

    right = N-1
    down = N-1
    left = 0
    up = 1

    direction = 0
    for _ in range(N**2):
        
        linearized_spiralMAP.append([r,c])

        # spiralMAP[r][c] = (cnt - (N**2 -1))*(-1)
        cnt += 1

        if direction%4 == 0 and c == right:
            direction += 1
            right -= 1
        elif direction%4 == 1 and r == down:
            direction +=1
            down -= 1
        elif direction %4 == 2 and c == left:
            direction +=1
            left += 1
        elif direction %4 == 3 and r == up:
            direction += 1
            up += 1

        r += dr[direction%4]
        c += dc[direction%4]

    linearized_spiralMAP.reverse()
    """
    이러한 data를 가지고, 현재 문제 상황에 적용하여 보자.
    """
    return linearized_spiralMAP #,spiralMAP

def collect_crushedMarbles(marbleColor):
    global Explode_One
    global Explode_Two
    global Explode_Three
    # print(f"{marbleColor} Marble Crushed!")
    if marbleColor == 1:
        Explode_One +=1
    elif marbleColor == 2:
        Explode_Two +=1
    elif marbleColor == 3:
        Explode_Three += 1

def cast_blizzard(MAP, d, s, N):
    d -= 1
    b_dr = [-1,1,0,0]
    b_dc = [0,0,-1,1]

    sharkR, sharkC = int((N+1)/2 -1), int((N+1)/2 -1)
    for _ in range(s):
        castR, castC = sharkR + b_dr[d] * (_+1), sharkC + b_dc[d] * (_+1)
        marbleColor = MAP[castR][castC]

        # 구슬 깨짐 유형 1 : 블리자드 마법에 의해
        # collect_crushedMarbles(marbleColor)
        # 설마 블리자드 말고 폭발만 한 것?
        MAP[castR][castC] = 0


    return MAP

def get_linearizedMAP(MAP, linearized_spiralMAP, N):
    linearizedMAP = [0]*(N**2)
    for g in range(N*N):
        r, c = linearized_spiralMAP[g][0], linearized_spiralMAP[g][1]
        linearizedMAP[g] = MAP[r][c]
    return linearizedMAP

def formulate_MAP_from_linearMAP(linearizedMAP, linearized_spiralMAP, N):
    """
    linearizedMAP : MAP의 구슬 정보가 1차원으로 저장되어 있는 자료구조
    linearizedSpiralMAP : MAP의 spiralIndex가 순서대로 1차원으로 저장되어 있는 자료구조
    MAP : MAP의 구슬 정보가 2차원으로 저장되어 있는 원 자료구조

    각각 다 모두 필요한게, spiral한 판단을 할 때도 있고(블리자드 마법 등), linear한 판단을 할 때도 있다. 
    """
    MAP = [[0]*N for _ in range(N)]
    for f in range(N*N):
        index = linearized_spiralMAP[f]

        lin_r, lin_c = index[0], index[1]

        MAP[lin_r][lin_c] = linearizedMAP[f]

    return MAP

def strech_crushedMarbles(MAP, linearized_spiralMAP, N):
    # recall : 리스트 더하기로 편집하기
    zeroFoundFlag = False
    linearizedMAP = get_linearizedMAP(MAP, linearized_spiralMAP, N)
    zeroStartEndIndicies = []

    # 상어가 있는 칸은 0이라서 오히려 헷갈리므로 빼고 생각
    for i in range(1, N*N): 
        r, c = linearized_spiralMAP[i][0], linearized_spiralMAP[i][1]
        
        if zeroFoundFlag == False:
            if MAP[r][c] == 0:
                zeroFoundFlag = True
                firstZeroIndex = i
        
        if zeroFoundFlag == True:
            if MAP[r][c] != 0:
                """
                linearizedMAP = linearizedMAP[:firstZeroIndex] + linearizedMAP[i:] + linearizedMAP[firstZeroIndex:i]
                # 여기서 MAP도 다시 수정해주어야하나? 그럴 것 같다. 인덱스 호환이 맞지 않기 때문에
                print(f"linearizedMAP : {linearizedMAP}")

                MAP = formulate_MAP_from_linearMAP(linearizedMAP, linearized_spiralMAP, N)
                

                -> 애초에 반복문 돌 동안 전반적으로 인덱스가 꼬이기 때문에 나중에 한번에 해주기로 했다.
                """
                zeroStartEndIndicies.append([firstZeroIndex, i])

                zeroFoundFlag = False
                # 이렇게하면 마지막에 zeroTail은 어떻게 되는거지?
                # -> ZeroFoundFlag가 켜진 후에, MAP[r][c]가 0이 아닌 구간이 없기 때문에, 그냥 넘어갈듯..?
    # print(f"l map : {linearizedMAP}")
    if zeroStartEndIndicies:
        # print(f"zero indicies : {zeroStartEndIndicies}")
        tmp_linearMAP = linearizedMAP[:zeroStartEndIndicies[0][0]]
        # print(f"{tmp_linearMAP}")
        remember = None
        for z in range(len(zeroStartEndIndicies)):
            start, end = zeroStartEndIndicies[z][0], zeroStartEndIndicies[z][1]

            if remember is not None:
                tmp_linearMAP.extend(linearizedMAP[remember:start])
            remember = end
            # print(f"{tmp_linearMAP}")

        tmp_linearMAP.extend(linearizedMAP[zeroStartEndIndicies[-1][1]:])

        zeroNeeded = N*N - len(tmp_linearMAP)

        linearizedMAP = tmp_linearMAP + [0]*zeroNeeded
        # print(f"updated l map : {linearizedMAP}")
    MAP = formulate_MAP_from_linearMAP(linearizedMAP, linearized_spiralMAP, N)
    return MAP, linearizedMAP

def MarbleExplosion(MAP, linearizedMAP, linearized_spiralMAP, N):
    numCnt = 1
    connected_flag = False
    comparing_marble = linearizedMAP[1]
    indicies_to_explode = [1]
    for i in range(2, N**2):
        this_marble = linearizedMAP[i]

        if this_marble ==  comparing_marble and this_marble != 0:
            numCnt+=1
            indicies_to_explode.append(i)
            # print(f"indicies_to_explode : {indicies_to_explode}")

        if numCnt == 4:
            connected_flag = True

        if this_marble != comparing_marble:

            if connected_flag == True:
                # collect_crushedMarbles(linearizedMAP[indicies_to_explode[0]])
                for idx in indicies_to_explode:
                    collect_crushedMarbles(linearizedMAP[idx])
                    linearizedMAP[idx] = 0

            comparing_marble = this_marble
            indicies_to_explode = [i]
            numCnt = 1
            connected_flag = False
    
    MAP = formulate_MAP_from_linearMAP(linearizedMAP, linearized_spiralMAP, N)

    return MAP, linearizedMAP

def MarbleTransformation(linearizedMAP, linearized_spiralMAP, N):
    group_information = []
    """
    group_information = [
        ...
        [ groupStartingLinearIndex, #marbles, #marbleNum ],
        ...
    ]
    """
    groupStartingLinearIndex = 1
    marbles = 1
    marbleNum = linearizedMAP[1]
    for i in range(2, len(linearizedMAP)):
        curMarbleNum = linearizedMAP[i]

        if curMarbleNum != marbleNum:
            group_information.append([groupStartingLinearIndex, marbles, marbleNum])

            marbles = 1
            groupStartingLinearIndex = i
            marbleNum = curMarbleNum
        elif curMarbleNum == marbleNum:
            marbles += 1
    
    newLinearMAP = [0]
    for i in range(len(group_information)):
        marbles, marbleNum = group_information[i][1], group_information[i][2]
        newLinearMAP.extend([marbles, marbleNum])

    if len(newLinearMAP) > N*N:
        newLinearMAP = newLinearMAP[:N*N]
    elif len(newLinearMAP) < N*N:
        newLinearMAP.extend([0]* (N*N - len(newLinearMAP)))

    linearizedMAP = newLinearMAP

    MAP = formulate_MAP_from_linearMAP(linearizedMAP, linearized_spiralMAP, N)

    return MAP, linearizedMAP


        
        
        


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

def get_answer():
    global Explode_One
    global Explode_Two
    global Explode_Three
    answer = Explode_One + 2*Explode_Two + 3*Explode_Three
    return answer 

if __name__ == "__main__":
    N, M, MAP, BLIZZARD = input_getter()
    linearized_spiralMAP = formulate_circulating_MAP(N) # spiralMAP, 

    # print("linearized spiralMAP = LinearizedIndexMAP")
    # MAP_printer(linearized_spiralMAP)
    
    for blizzard in range(M):

    
        d, s = BLIZZARD[blizzard][0], BLIZZARD[blizzard][1]

        MAP = cast_blizzard(MAP, d, s, N)

        # print("after blizzard")
        # MAP_printer(MAP)
        while True:
            

            MAP, linearizedMAP = strech_crushedMarbles(MAP, linearized_spiralMAP, N)


            # print("After zeroFill")
            # MAP_printer(MAP)
            # print(f"linearizedMAP : {linearizedMAP}")

            prevMAP = MAP[:]
            MAP, linearizedMAP = MarbleExplosion(MAP, linearizedMAP, linearized_spiralMAP, N)

            # print("After MarbleExplosion")
            # MAP_printer(MAP)
            if MAP == prevMAP:
                break

        MAP, linearizedMAP = MarbleTransformation(linearizedMAP, linearized_spiralMAP, N)
        # print("After MarbleTransformation")
        # MAP_printer(MAP)


    answer = get_answer()
    print(answer)


"""
배운점

1. spiral Indexing에 대해 이해하였다. 회전 순서를 정하고, 회전이 전횐되는 지점의 인덱스를 한계를 정해 놓은 후, 그 다음이 +1/-1씩
    변한다는 점을 활용하여 direction을 회전해가면서 쓰는 함수였다. 특히, x방향과 y방향 전환의 합으로 회전을 구현한 점이 인상 깊다.

2. 회전 spiralIndexing의 아이디어를 차용하여 linearTransfomration을 할 수 있었다. 
    각각 회전 MAP, linearization된 맵, 인덱스가 linearization 되어 있는 맵 이렇게 세 가지 자료를 통해 서로가 서로를 영향 주면서
    각각의 연산을 수행하기 수월하였다.

3. 리스트 더하기 인덱싱 기술 감을 조금 더 잡았다. 원래는 단순히 리스트끼리 인덱싱 한 것의 연산으로 생각하였다가,
    당연하지만 이가 인덱스 반복문 도중에 수정이 될 경우 인덱스가 꼬이는 현상이 발생한다.
    따라서 이를 미리 저장해 두었다가, head와 tail만 따로 해주고 중간은 반복문에서 한 자료를 다음 자료로 넘겨 가며 그 중간 부분에
    인덱싱 더하기를 통한 업데이트를 하면 된다.

4. 또 이럴 경우 ConnectedComponent를 구하고자 할 때, linear한 View로 보면 dfs 등의 다소 귀찮은 구현을 하지 않아도 쉽게 구현할 수 있다
    는 점을 알게 되었다.
    따라서, spiral한 문제가 나오면 다음과 같이 자동으로 행동하자.

    - spiralMAP, spiralIndexLinearMap, LinearMAP 세가지를 모두 형성한다.
    - component간의 연산을 이러한 방식을 통해 주고받자.
"""