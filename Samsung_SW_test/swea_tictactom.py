# 틱택톰

def input_getter():
    N = int(input())
    test_cases = []
    cnt = 0
    for _ in range(N):
        tictactom = []
        if cnt != N-1:
            for i in range(5):
                this_row = list(input())
                if i != 4:
                    tictactom.append(this_row)
        if cnt == N-1:
            for j in range(4):
                this_row = list(input())
                tictactom.append(this_row)
        cnt+=1
        test_cases.append(tictactom)
    return N, test_cases



def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()



def total_row_checker(row):
    """row를 검사하는 방법"""
    first_cell = row[0]
    
    EmptyCnt = 0
    flag = True
    if first_cell == 'T':
        first_cell = row[1]

    if first_cell == '.':
        flag = False

    for j in range(len(row)):
        if row[j] == '.':
            EmptyCnt +=1
            flag = False

        if row[j] != first_cell:
            if row[j] != 'T':
                flag = False

    return flag, first_cell, EmptyCnt



def diagnoal_checker(MAP):
    """좌하단 대각선 방향 체커"""
    r, c = 0,0
    flag = True
    initial_value = MAP[r][c]

    if initial_value == 'T':
        initial_value = MAP[r+1][c+1]

    if initial_value == '.':
        flag = False
        return flag, initial_value

    for k in range(3):
        r, c = r+1, c+1
        
        if MAP[r][c] != initial_value:
            if MAP[r][c] != 'T':
                flag = False
                return flag, initial_value

    return flag, initial_value



def GameState_checker(MAP):
    rotated_MAP = list(zip(*MAP[::-1]))
    rotated_MAP = [list(row) for row in rotated_MAP]
    total_empty_count = 0

    for i in range(4):
        flag1, winner1, EmptyCnt = total_row_checker(MAP[i])
        total_empty_count += EmptyCnt
        if flag1:
            # print("row win!")
            return True, winner1

        flag2, winner2, not_in_use = total_row_checker(rotated_MAP[i])
        if flag2:
            # print("column win!")
            return True, winner2
    
    flag3, winner3 = diagnoal_checker(MAP)
    if flag3:
        # print("leftdown diag win!")
        return True, winner3

    flag4, winner4 = diagnoal_checker(rotated_MAP)
    if flag4:
        # print("rightdown diag win!")
        return True, winner4

    if total_empty_count == 0:
        winner5 = 'Draw'
        return True, winner5

    return False, False
        
if __name__ == '__main__':
    N, test_cases = input_getter()

    for l in range(N):
        tictactom = test_cases[l]
        isitEnded, winner = GameState_checker(tictactom)

        if isitEnded:
            if winner == 'Draw':
                print(f"#{l+1} {winner}")
            else:
                print(f"#{l+1} {winner} won")
        else:
            print(f"#{l+1} Game has not completed")

"""
배운점

1. str을 바로 받아서 리스트로 다 분할시키고 싶으면 그냥 list(string) 하면 된다.
2. 대각선/가로세로를 체킹할 때, 맵 자체를 회전에서 체킹하는 아이디어를 떠올려냈다. 이거 진짜 대박인 듯!
3. 괜히 인덱싱 하나 아낀다고 하다가, 엣지케이스 커버 못해서 그거때매 한시간 날린듯; 굳이 그런거 하지말자.
4. 삼성식 입출력에 익숙해지자. 약간 전체 데이터를 저장을 따로 해놓고 거기에서 하나씩 꺼내서 돌리는 마인드.. 그리고 fstring을 겁나게 유용하게 쓴다.
5. 
"""