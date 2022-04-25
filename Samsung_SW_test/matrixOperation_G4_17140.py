# 이차원 배열과 연산

def input_getter():
    r, c, k = map(int, input().split(' '))
    N = 3
    A = []
    for _ in range(N):
        A.append(list(map(int, input().split(' '))))

    return r, c, k, N, A


"""
R연산과 C연산은 같다. 행렬을 회전 한 번 시켜서 정렬해주고 다시 같은 방향으로 3회전시켜서 정렬시키자.
    회전 방향은 CCW로 하자.
    이 때, 그럼 CCW된 행렬의 R을 기존기준과 반대 (내림차순)으로 정렬해야 한다? -> 아니었다... 하지만 trivial(?)함! (아 어쨌든 trivial 하다고...)
"""

def row_sort(MAP, column = False):
    newMAP = []
    max_row_length = -1

    for r in range(len(MAP)):
        row_info = []
        """
        row_info = [
            ...
            [ num, cnt ]
            ...
        ]
        """
        visited_num = []
        this_row = MAP[r]
        for c in range(len(MAP[0])):
            curNum = this_row[c]
            if curNum == 0:
                continue

            elif curNum not in visited_num:
                visited_num.append(curNum)
                row_info.append([curNum, this_row.count(curNum)])

        if column == False:
            row_info.sort(key = lambda a : (a[1], a[0]))

            # print해보고 사실 두개 똑같이 소팅해도 된다는 것을 알았다. 이왜진?
        elif column == True:
            row_info.sort(key = lambda a: (a[1], a[0]))

        # print(f"row info : {row_info}")
        # new_row_num = []
        # new_row_cnt = []
        new_row = []

        # for z in range(len(row_info)):
        #     new_row_num.append(row_info[z][0])
        #     new_row_cnt.append(row_info[z][1])
        # max_row_length = max(max_row_length, len(new_row_num)+ len(new_row_cnt))
        for z in range(len(row_info)):
            new_row.append(row_info[z][0])
            new_row.append(row_info[z][1])


        max_row_length = max(max_row_length, len(new_row))

        newMAP.append(new_row)

    max_row_length = min(max_row_length, 100)

    for r in range(len(newMAP)):
        if max_row_length < len(newMAP[r]): # 이건 오직 100이 넘는 경우만 가능함
            newMAP[r] = newMAP[r][:max_row_length]

        else:
            newMAP[r] = newMAP[r] + [0]*(max_row_length-len(newMAP[r]))
    

    return newMAP

def column_sort(MAP):
    rotatedMAP = [list(row) for row in list(zip(*MAP))[::-1]]

    rotatedMAP = row_sort(rotatedMAP, column = True)

    # 반대로 1바퀴만 돌려서 원상 복구
    rotatedMAP = [list(row) for row in list(zip(*rotatedMAP[::-1]))]

    return rotatedMAP



"""
최소시간..? 그냥 하다보면 처음으로 도달하게 되는 순간을 말하는 건가 아니면 따로 최소시간을 구하는 방법이 있나?

-> ㅇㅇ 그말이었다.
"""

            


def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

if __name__ == '__main__':
    time_step = 0
    tartget_r, target_c, target_k, N, MAP = input_getter()

    # MAP = row_sort(MAP)
    # print("after row sort")
    # MAP_printer(MAP)
    break_flag = False
    while True:
        rowLength = len(MAP)
        columnLength = len(MAP[0])

        if rowLength > 100:
            pass
        if columnLength > 100:
            pass
        try:
            if MAP[tartget_r-1][target_c-1] == target_k:
                break
        except:
            pass

        time_step += 1
        if time_step > 100:
            break_flag = True
            break
        

        if rowLength >= columnLength:
            MAP = row_sort(MAP)
            # print("after row sort")
            # MAP_printer(MAP)

        elif rowLength < columnLength:
            MAP = column_sort(MAP)
            # print("after column sort")
            # MAP_printer(MAP)

        
    if break_flag:
        print(-1)

    else:
        print(time_step)

"""
배운점

1. MAP을 회전해서 사용하고 다시 반대로 회전시켜서 돌려놓는 방법에 대한 아이디어를 생각해냈다. 앞으로 다른 곳에도 적용하면, 코드를 훨씬 짧게 쓸 수 있다! (시간 단축 + 실수가능성 감축)

2. 문제를 잘 읽자. [num, num, ... , cnt, cnt, ...] 인줄 알았는데, [num, cnt, num, cnt, ...] 였다. 정신차려...

3. 본격적으로 처음 코테 공부시작하고 나서, try-except문을 처음 써본 것 같다. 그렇게 특별할 것은 없긴 한데,
    '혹시' 다른 문제 풀다가 도저히 이해가 잘 안가는 테스트 케이스 있으면 try-except문을 고려해 볼 수도 있을 것 같다는 생각이 들었다.
    (지금의 경우야 중간 중간 MAP_printer로 확인할 수 있고, 예시 케이스도 주어져서 망정이지..)

4. 테스트 케이스를 직접 만들어서 테스트 해볼 수는 없는지에 대해 고려해보게 되었다. 다들 어케하는거지..... 결과를 생각하는게 너무 힘들거나 하더라도 시간 너무 오래 걸릴 것 같다. (시험 시 사용 불가능)

5. 이제 슬슬 150줄대 코드는 짧아보이기 시작했다.

"""