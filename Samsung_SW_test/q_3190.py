import sys
from collections import deque

APPLE = 1

class Snake:
    def __init__(self):
        self.size = 1
        
        self.snake = 2
        self.curPos = (0,0)
        self.history = deque()

        self.curDir = (1,0)      
        self.timer = 0
        self.alive = True
        

def input_getter():
    N = int(sys.stdin.readline())
    K = int(sys.stdin.readline())
    MAP = [[0]*N for _ in range(N)]
    if K != 0:
        for _ in range(K):
            i, j = map(int, sys.stdin.readline().split(' '))
            MAP[i-1][j-1] = APPLE
    L = int(sys.stdin.readline())

    turning_point = []
    for _ in range(L):
        X, C = sys.stdin.readline().split(' ')
        X = int(X)
        C = C[0]
        turning_point.append((X,C))
        
    return N, K, MAP, turning_point

def turn(snake, C):
    if C == 'L':
        turnLeft(snake)
    elif C == 'D':
        turnRight(snake)
    else:
        pass

def turnLeft(snake):
    dir = snake.curDir
    # 4 가지 경우의 수
    if dir == (0,1):
        snake.curDir = (1,0)
    elif dir == (-1,0):
        snake.curDir = (0,1)
    elif dir == (0,-1):
        snake.curDir = (-1,0)
    elif dir == (1,0):
        snake.curDir = (0,-1)

def turnRight(snake):
    dir = snake.curDir
    # 4 가지 경우의 수
    if dir == (0,1):
        snake.curDir = (-1,0)
    elif dir == (-1,0):
        snake.curDir = (0,-1)
    elif dir == (0,-1):
        snake.curDir = (1,0)
    elif dir == (1,0):
        snake.curDir = (0,1)

def game(N, MAP, turning_point):
    #1 game init
    snake = Snake()
    snake.history.append(snake.curPos)
    MAP[snake.curPos[1]][snake.curPos[0]] = snake.snake
    time_bf = 0
    turning_point.append((123456789, 'C')) # 마지막에 쭉 가주기 위한 가상 phase 생성

    #2 move along the rule
    for phase in turning_point:
        time = phase[0]
        next_dir = phase[1]
        
        curtime = time - time_bf

        for t in range(curtime):
            # 2-1 방향을 틀기 전까지 현재 머리를 방향을 따라 우선 직진 
            snake.curPos = (snake.curPos[0]+snake.curDir[0], snake.curPos[1]+snake.curDir[1])
            # print(f"curPos : {snake.curPos}")
            snake.timer += 1
            # snake.history.append(snake.curPos)
            
            #2-2 만나는 경우의 수 : 벽이나 자기 자신과 만나면 게임이 종료된다. / 사과이면 그대로 늘린다. / 빈 칸이면 꼬리를 빈칸으로 한다.
            if not (0 <= snake.curPos[0] <= N-1) or not (0 <= snake.curPos[1] <= N-1): # 벽과 만날 경우
                snake.alive = False
                snake.size += 1
                # print('벽과 충돌')
                break
            elif (snake.curPos in snake.history): # 자기 자신과 만날 경우
                snake.alive = False
                snake.size += 1
                # print('자신과 만남!')
                break
            elif MAP[snake.curPos[1]][snake.curPos[0]] == APPLE: # 사과를 만날 경우
                MAP[snake.curPos[1]][snake.curPos[0]] = snake.snake # 사과 먹음
                snake.history.append(snake.curPos)
                snake.size += 1

            elif MAP[snake.curPos[1]][snake.curPos[0]] == 0: # 빈 칸을 만날 경우
                snake.history.append(snake.curPos)
                MAP[snake.history[0][1]][snake.history[0][0]] = 0 #꼬리 자르기
                snake.history.popleft()
            MAP[snake.curPos[1]][snake.curPos[0]] = snake.snake
            
            # 게임 상황 관찰
            # for i in range(len(MAP)):
            #     print(MAP[i])
            # print()
        # 3 이번 방향의 루프 끝 머리 방향 바꾸기 처리

        # 3-1 죽었는지 확인
        if snake.alive == False:
            break

        # 3-2 다음 방향으로 머리 방향 : curDir을 틀어 놓는다. 경우의 수 = 'L': 좌회전  or 'D' : 우회전
        time_bf = time
        turn(snake, next_dir)
        # print(f"snake size : {snake.size}")
        # print(f"curDir : {snake.curDir} \n")


    return snake.timer
            

if __name__ == "__main__":
    N, K, MAP, turning_point = input_getter()
    # print(N)
    
    time = game(N, MAP, turning_point)
    # for i in range(len(MAP)):
    #     print(MAP[i])
    print(time)