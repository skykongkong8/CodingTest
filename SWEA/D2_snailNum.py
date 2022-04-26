# 달팽이 숫자

def input_getter():
    N = int(input())
    num_list = []
    for _ in range(N):
        num_list.append(int(input()))

    return N, num_list

def snailMatric(curNum):
    cnt = 1
    
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    right = curNum - 1
    down = curNum-1
    left = 0
    up = 1
    direction = 0

    matrix = [[0]*curNum for _ in range(curNum)]
    r = c = 0

    for i in range(curNum*curNum):
        matrix[r][c] = cnt    
        cnt += 1

        if direction%4 == 0 and c == right:
            direction += 1
            right -= 1
            
        elif direction%4 == 1 and r == down:
            direction += 1
            down -= 1
        
        elif direction %4 == 2 and c == left:
            direction += 1
            left += 1

        elif direction %4 == 3 and r == up:
            direction +=1
            up += 1

        r += dr[direction%4]
        c += dc[direction%4]

    return matrix

def matrix_printer(matrix, curNum):
    for r in range(curNum):
        res = ""
        for c in range(curNum):
            res += str(matrix[r][c])
            res += " "
        res= res[:-1]
        print(res)




if __name__ == '__main__':
    N, num_list = input_getter()
    # print(f"numlist = {num_list}")

    for n in range(N):
        curNum = num_list[n]
        matrix = snailMatric(curNum)
        print(f"#{n+1}")
        matrix_printer(matrix, curNum)
        
"""
배운점

1. spiral인덱싱의 기본 개념이 홀수 말고도 짝수에도 먹힌다는 사실을 확인하였다.

2. matrix printer의 아이디어를 생각해냈다. 백준에서는 str처리하는 문제를 그렇게 많이 풀어보지 않아서
    어쩌면 시험장에 가서 기본적인 str 테크닉 때문에 막힐 수도 있다는 생각을 했다.
    res 를 이용한 str 덧셈과 str인덱싱에 대해 기억하자.
"""