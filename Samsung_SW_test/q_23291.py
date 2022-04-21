# 어항 정리
from collections import deque
def input_getter():
    N, K = map(int, input().split(' '))
    fish_list = list(map(int, input().split(' ')))
    MAP = [[0]*N for _ in range(N)]
    MAP[-1] = fish_list
    return N, K, fish_list, MAP

dr = [0,0,1,-1]
dc = [1,-1,0,0]

def regulate_fishNum():
    """물고기 수를 조절하는 함수"""

def linearize_fishes():
    """기준에 맞게 물고기들을 다시 일렬로 만들어주는 함수"""

# 고민1 : 어항을 2차원 리스트로 아예 만들어놓을 것인가? -> 그럼 NXN으로 한변의 길이가 N을 절대 넘지 못할 것이므로
# 고민2 : MAP 자료구조는 어떻게 구성할 것인가? 그냥 fishNum 만으로?
# 고민3 : 

"""
MAP = [
    [0,0,0,0...],
    ...
    [3,2,3,8,5,6,7,...]
]
"""
def step_1(MAP, N):
    """가장 적은 어항에 한 마리씩 넣는 함수"""
    fish_list = MAP[-1]
    fishNum = min(fish_list)
    
    for i in range(len(fish_list)):
        if fishNum == fish_list[i]:
            MAP[-1][i] +=1


    return MAP

def stick_to_zero(MAP, N, find_from_here = 0):
    """
    회전이나 어항 옮기기 이후에 왼쪽으로 붙여주는 함수 : 2차원 리스트에 대한 식이어야 한다.
    
    + 최소한 어느 row부터 찾을지까지는 알려줘야하는 거 아닌가..?
    """
    for z in range(find_from_here, N):
        row = MAP[z]
        for x in range(len(row)):
            if row[x] != 0:
                nonZeroRow = row[x:]
                leftoverLength = len(row)-len(nonZeroRow)
                new_row = nonZeroRow + [0]*leftoverLength

                MAP[z] = new_row

                break
    return MAP

def step_2(MAP, N):
    """
    가장 왼쪽의 어항을 그것의 오른쪽에 놓는 함수
    즉, N-1, 0을 N-2,1에 주고, stick to zero하면 된다
    """
    MAP[N-2][1], MAP[N-1][0] = MAP[N-1][0], MAP[N-2][1]
    MAP = stick_to_zero(MAP, N, find_from_here=N-2)

    return MAP

def step_3(MAP, N):
    """
    공중 부양 후 90도 회전시키는 함수
    1차원 함수를 어떻게 회전 후 갖다붙일 수 있을까?
    - 의견1 : 억지로 2차원함수로 만들어서 회전 후, 0을 제거하는 방법 -> 그냥 해도 되는거였다..
    - 의견2 : 기가막힌 인덱싱 테크닉이 있을 것이다.
    """
    stop_flag = False

    # 공중부양 중인 column들을 받아온다.
    while not stop_flag:

        list_for_checking_floatingFishes = MAP[-2]
        floating_columns = []
        nonZeroFoundFlag = False
        for i in range(N):
            if list_for_checking_floatingFishes[i] != 0:
                nonZeroFoundFlag = True
                floating_columns.append(i)

            if nonZeroFoundFlag and list_for_checking_floatingFishes[i] == 0:
                break
            

        if len(floating_columns) > N - len(floating_columns):
            stop_flag = True
            break
        
        # 의견1을 채택해보자.
        floating_component = []
        height = 0
        for j in range(N-1, -1, -1):
            if MAP[j][0] == 0:
                floating_component_height = height
                break
            height +=1

        
        for c in range(N-floating_component_height, N):
            this_row = MAP[c][:len(floating_columns)]
            MAP[c][:len(floating_columns)] = [0]*len(floating_columns)
            floating_component.append(this_row)

        MAP = stick_to_zero(MAP, N, N-1) # 마지막 줄만 당기면 된다.
        
        rotated_floating_component = list(zip(*floating_component[::-1])) # CW
        
        for k in range(len(rotated_floating_component)):
            rotated_floating_component[k] = list(rotated_floating_component[k])


        # print(f"hieght = {floating_component_height}")
        # print(f"floating : {floating_component}")
        # print(f"rotated : {rotated_floating_component}")

        for a in range(len(rotated_floating_component)):
            for b in range(len(rotated_floating_component[0])):
                MAP[N-1 - len(rotated_floating_component) + a][b] = rotated_floating_component[a][b]


        current_zero_index = MAP[-1].index(0)
        nonrotatable_length = current_zero_index - len(rotated_floating_component)
        zeroRow = [curRow[0] for curRow in MAP]
        zeroRow.reverse()
        currentZeroRowHeight = zeroRow.index(0)
        if currentZeroRowHeight > nonrotatable_length:
            break
        # print("during step 3:")
        # print_matrix(MAP)

    return MAP, currentZeroRowHeight, current_zero_index

def step_4(MAP, N, currentZeroRowHeight, current_zero_index):
    one_for_all = []
    """
    one_for_all = [
        ...
        [[r,c], [[r',c', difference], ...]]
        ...
    ]
    """
    visited_map = []
    r = N-1
    c = 0
    queue = deque()
    queue.append([r,c])
    visited_map.append([r,c])

    # DFS 로 하니 발생한 문제: 이미 전에 방문한 애는 다른 애에서 관계형성이 카운트가 안됨 
    # (딱 1회씩 모든 애들이 combinations 되어야 하는데 각각에 대한 최단 경로로까지만 관계가 맺어짐)

    # while queue:
    #     curRC = queue.popleft()
        
    #     # visited_map.append([curRC[0], curRC[1]])
    #     curR, curC = curRC[0], curRC[1]
    #     curNum = MAP[curR][curC]

    #     if curNum == 0:
    #         continue

    #     neighbor_indicies_information = []
    #     for k in range(4):
    #         tmp_r, tmp_c = curR+dr[k], curC+dc[k]

    #         if 0<= tmp_r <N and 0 <= tmp_c < N:
                
    #             if MAP[tmp_r][tmp_c] != 0 and ([tmp_r, tmp_c] not in visited_map):
    #                 visited_map.append([tmp_r, tmp_c])
    #                 queue.append([tmp_r, tmp_c])
    #                 difference = curNum - MAP[tmp_r][tmp_c]
    #                 neighbor_indicies_information.append([tmp_r, tmp_c, difference])
    #     one_for_all.append([[curR, curC],neighbor_indicies_information])    

    
    # 아이디어 2: 우선 모든 위치/값을 받아온 다음에 개별적으로 하나씩 짝찌어주자. 이게 Brute Force지만 어쩔수 없음...
    Nonzero_Indicies_and_Values = []
    """
    Nonzero_Indicies_and_Values = [
        '''
        [[r,c], value]
        '''
    ]
    """
    for r in range(N-currentZeroRowHeight, N):
        for c in range(current_zero_index):
            if MAP[r][c] != 0:
                Nonzero_Indicies_and_Values.append([[r,c], MAP[r][c]])
    """
    one_for_all = [
        ...
        [[r,c], [[[r',c'], difference], ...]] # difference = [r,c] - [r',c'] 따라서 difference > 0이면 [r,c]가 큰것
        ...
    ]
    """
    for q in range(len(Nonzero_Indicies_and_Values)-1):
        Index_1 = Nonzero_Indicies_and_Values[q][0]
        Value_1 = Nonzero_Indicies_and_Values[q][1]
        neighboring_list = []
        for w in range(q+1, len(Nonzero_Indicies_and_Values)):
            Index_2 = Nonzero_Indicies_and_Values[w][0]
            Value_2 = Nonzero_Indicies_and_Values[w][1]
            if is_neighbor(Index_1, Index_2):

                difference = Value_1 - Value_2

                neighboring_list.append([Index_2, difference])
        if neighboring_list:
            one_for_all.append([Index_1, neighboring_list])
            
    # print_matrix(one_for_all)

    for info in one_for_all:
        r_1, c_1 = info[0][0],  info[0][1]
        for index_and_difference in info[1]:
            r_2, c_2, difference = index_and_difference[0][0], index_and_difference[0][1], index_and_difference[1]

            plus_this = int(abs(difference) / 5)
            
            if plus_this > 0:
                
                if difference > 0: # r_1, c_1 is bigger
                    MAP[r_1][c_1] -= plus_this
                    MAP[r_2][c_2] += plus_this

                elif difference < 0: # r_2, c_2 is bigger
                    MAP[r_1][c_1] += plus_this
                    MAP[r_2][c_2] -= plus_this

    return MAP, Nonzero_Indicies_and_Values

def is_neighbor(idx1, idx2):
    r1, c1 = idx1[0], idx1[1]
    r2, c2 = idx2[0], idx2[1]

    total_diff = abs(r1-r2) + abs(c1-c2)
    if total_diff == 1:
        return True
    return False

def step_5(MAP, N, Nonzero_Indicies_and_Values = None):
    """
    일렬로 만드는 함수
    """
    
    """
    Nonzero_Indicies_and_Values = [
        '''
        [[r,c], value]
        '''
    ]
    """
    if Nonzero_Indicies_and_Values is not None:
        Nonzero_Indicies_and_Values.sort(key = lambda a: (a[0][1], -a[0][0]))
        # print(Nonzero_Indicies_and_Values)

        newMAP = [[0]*N for _ in range(N)]  
        cnt = 0
        for info in Nonzero_Indicies_and_Values:
            r,c = info[0][0], info[0][1]
            newMAP[-1][cnt] = MAP[r][c]
            cnt+=1
        MAP = newMAP
    else:
        indexing_idx = int(N/2)
        upper_part = MAP[-2][:indexing_idx]
        lower_part = MAP[-1][:indexing_idx]

        MAP[-2][:indexing_idx]= [0]*indexing_idx
        MAP[-1][:indexing_idx] = upper_part
        MAP[-1][indexing_idx:] = lower_part
    return MAP        


def step_6(MAP, N):
    upper_part = MAP[-1][:int(N/2)]
    upper_part.reverse()
    MAP[-1][:int(N/2)] = [0]*(int(N/2))

    MAP = stick_to_zero(MAP, N, find_from_here=N-1)
    # lower_part = MAP[-1][N/2:]

    MAP[-2][:int(N/2)] = upper_part

    # print("during step 6")
    # print_matrix(MAP)


    """
    [part1, part2]
    [part3, part4] 라 하자
    """
    partLength = int(N/4)
    part1 = MAP[-2][:partLength]
    part2 = MAP[-2][partLength:]
    part3 = MAP[-1][:partLength]
    part4 = MAP[-1][partLength:]

    part1.reverse()
    part3.reverse()
    
    MAP[-3][:partLength] = part1
    MAP[-2][:partLength] = part2
    MAP[-4][:partLength] = part3
    MAP[-1][:partLength] = part4

    MAP[-1][partLength:] = [0]*(int(N/2)+partLength)
    MAP[-2][partLength:] = [0]*(int(N/2) + partLength)

    height = 4
    
    return MAP, height, len(part1)




        
def print_matrix(every_2D_matrix):
    for every_row in every_2D_matrix:
        print(every_row)
    print()

def last_linearization(MAP, N, currentZeroRowHeight):
    row_list = []
    current_zero_index = MAP[-1].index(0)
    for c in range(current_zero_index):
        for r in range(N-1, N - currentZeroRowHeight -1, -1):
            row_list.append(MAP[r][c])
        # print(row_list)
        

    MAP = [[0]*N for _ in range(N)]
    MAP[-1] = row_list
    # print(row_list)

    return MAP
        

def total_sequence(MAP, N, K):
    # print("init :")
    # print_matrix(MAP)
    
    MAP = step_1(MAP, N)
    # print("after step1")
    # print_matrix(MAP)

    MAP = step_2(MAP, N)
    # print("after step 2")
    # print_matrix(MAP)

    MAP, currentZeroRowHeight, current_zero_index = step_3(MAP, N)
    # print("after step 3")
    # print_matrix(MAP)

    MAP, Nonzero_Indicies_and_Values = step_4(MAP, N, currentZeroRowHeight, current_zero_index)
    # print("after step 4")
    # print_matrix(MAP)

    MAP = step_5(MAP, N, Nonzero_Indicies_and_Values=Nonzero_Indicies_and_Values)
    # print("after step 5")
    # print_matrix(MAP)

    MAP, currentZeroRowHeight, current_zero_index = step_6(MAP, N)
    # print(f"curHeight : {currentZeroRowHeight}, curLength  : {current_zero_index}")
    # print("after step 6")
    # print_matrix(MAP)

    MAP, Nonzero_Indicies_and_Values = step_4(MAP, N, currentZeroRowHeight, current_zero_index)
    # print("after step 7")
    # print_matrix(MAP)

    MAP = last_linearization(MAP, N, currentZeroRowHeight) # 마지막 linearization
    # print("after step 8")
    # print_matrix(MAP)

    final_row = MAP[-1]
    maxVal = max(final_row)
    minVal = min(final_row)
    
    if maxVal - minVal <= K:
        return MAP, True

    return MAP, False

if __name__ == "__main__":
    N, K, fish_list, MAP = input_getter()
    # MAP =total_sequence(MAP, N, K)

    cnt = 0

    while True:
        cnt += 1
        MAP, flag = total_sequence(MAP, N, K)
        if flag:
            break
    print(cnt)

"""
배운점

1. 행렬을 꺼내서 같다 붙이기 테크닉 거의 마스터 : row별로 받아오기, column별로 받아오기, 복잡한 인덱싱하기
2. 행렬 회전시킬 때 테크닉 기억하기 : list(zip(*piece[::-1])) : CW 아니면 list(zip(*piece))[::-1] : CCW
3. 가끔씩은 그냥 구조상 하드코딩이 훨씬 편할 수도 있다.
4. 어짜피 디버깅은 해야함 -> 단계별로 하나씩 print 해보면서 진행하자
5. 임의로 만든 자료구조를 계속해서 써주는 습관은 매우 좋은 것 같다. 인덱싱이나, 알고리즘 구현 실수를 막아준다.
6. 하나씩 모두를 짝찌을 때, DFS/BFS는 각각에 대한 최단 경로 edge만을 형성하므로 모두에 대한 하나짝찟기는 안된다.
    +  따라서 BubbleSort형식으로 그냥 BruteForce하게 구현하자. 게다가, 여기서는 이웃하여야하는 부분이 있어서 is_neighbor까지 점검해주었다.
        dr, dc를 쓰지 않고도 neighbor를 이렇게 접근할 수 있다. cost는 좀 높아지겠지만..
7. r-c인덱싱을 하지 않고, c-r인덱싱을 통해 세로로 다닐 수 있다. 거기에, N에서부터 작아지는 인덱싱 방향을 설정하여 다양한 방향으로 갈 수 있다.
    (2중 for문 사용하여)
    a. 아래로 가면서 왼쪽부터 훑기
    for r in range(N):
        for c in range(N):
            MAP[r][c]
    b. 아래로 가면서 오른쪽부터 훑기
        for r in range(N):
            for c in range(N-1, -1, -1):
                MAP[r][c]
    c. 왼쪽으로가면서 아래부터 훑기
    for c in range(N-1, -1, -1):
        for r in range(N-1, -1, -1):
            MAP[r][c]

    d. 오른쪽으로 가면서 위부터 훑기
        for c in range(N):
            for r in range(N):
                MAP[r][c]
    등등

8. 순차적으로 일어나는 것과 한번에 일어나는 것을 구분지어서 처리할 수 있다.
9. 리스트 가공하기 테크닉 : 단순한 리스트의 덧셈으로 쉽고 빠르게 리스트를 가공할 수 있다.
"""