# BFS를 레이더망처럼 사용하는 방법
from collections import deque

n = 10
MAP = [[0]*n for _ in range(n)]

dx = [1,-1,0,0]
dy = [0,0,1,-1]

def bfs(x,y,board):
    q = deque([(x,y)])
    cost = 1
    board[x][y] = cost
    while q:
        cur = q.popleft()
        
        for i in range(4):
            xx = dx[i] + cur[0]
            yy = dy[i] + cur[1]
            if 0 <= xx < n and 0 <= yy < n and not board[xx][yy]:

                board[xx][yy] = board[cur[0]][cur[1]] +1
                q.append((xx,yy))
        
bfs(5,5, MAP)

for _ in MAP:
    print(_)


# 2차원 리스트에서 2차원 추출하고, 회전시키는 인덱싱

MAP = [[i*j for i in range(8)] for j in range(8)]
for row in MAP:
    print(row)
print()

for r in range(0,len(MAP),2):
    for c in range(0, len(MAP), 2):
        piece = [indexed_row[c:c+2] for indexed_row in MAP[r:r+2]] # 이거진짜 유용함
        
        for row in piece:
            print(row)
        print()

        # rotated_piece = [[None]*len(piece) for _ in range(len(piece))]

        # for i in range(len(rotated_piece)):
        #     for j in range(len(rotated_piece)-1, -1, -1):
        #         rotated_piece[len(piece) - i - 1][j] = piece[j][i]

        # CCW
        rotated_piece = list(zip(*piece))[::-1]
        rotated_piece = [list(row) for row in rotated_piece]

        # CW
        rotated_piece = list(zip(*piece[::-1]))
        rotated_piece = [list(row) for row in rotated_piece]



        final_piece = [[None]*len(rotated_piece) for _ in range(len(rotated_piece))]

        for j in range(len(rotated_piece)):
            for k in range(len(rotated_piece)):
                final_piece[j][k] = rotated_piece[j][k]

        for row in final_piece:
            print(row)
        print()

# 3. 1차원 리스트가 꼬리에 꼬리를 물고 회전하도록 하기
MAP = [i for i in range(10)]
MAP = [MAP[-1]] + MAP[:-1]

# 4. dice 모델링 아이디어
"""
dice = [
    TOP,
    동,
    서,
    남,
    북,
    BOTTOM
]
동쪽(X)으로 가면 -> 동(X)이 curTOP (= 서(X')가 curBOTTOM), 남and북 유지, TOP이 cur서 (= BOTTOM이 cur동),  
YAW 회전:
CW -> TOP/BOTTOM유지, 남이 cur동(= 북이 cur서), 동이 cur북 (= 서가 cur남)
CCW -> TOP/BOTTOM유지, 남이 cur서(= 북이 cur동), 동이 cur남 (= 서가 cur북) 
"""

# 5. index bounding

# 6.  spiral indexing transformation

"""
골뱅이 모양 나선형 인덱스를 이해하는 방법 :
회전이라는 요소를 위아래방향, 좌우 방향으로 분해하여서 생각하면 뭔가 느낌이 온다.
"""

def spiral_matrix(N):
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]

    direction = 0

    cnt = 0

    r = 0
    c = 0

    right = N-1
    down = N -1
    left = 0
    up = 1

    MAP = [[0]*N for _ in range(N)]
    for _ in range(N**2):
        # MAP[r][c] = cnt
        MAP[r][c] = (cnt - (N**2))*(-1)
        cnt +=1

        if direction %4 == 0 and c == right:
            direction += 1
            right -=1
        elif direction %4 == 1 and r == down:
            direction += 1
            down -=1
        elif direction%4 == 2 and c == left:
            direction +=1
            left +=1
        elif direction%4 == 3 and r == up:
            direction +=1
            up +=1
        r += dr[direction%4]
        c += dc[direction%4]
    return MAP

sprialMAP = spiral_matrix(5)
for row in sprialMAP:
    print(row)
print()

"""
나머지는 cnt를 연산을 통해서 조절하거나,
dr dc의 방향 순서를 조절하거나,
rot = [list(row) for row in list(zip(*matrix[::-1]))] 을 통해서 해결할 수 있다.
"""
# spiralIndexing을 다시 한번 연습하자:

N = 5
dr = [0,1,0,-1]
dc = [1,0,-1,0]

example_matrix = [[i*j for i in range(1,7)] for j in range(4, 0,-1)]

def matrix_linearization(linearIndicies, matrix):
    linearized_matrix = []
    for i in range(len(linearIndicies)):
        r, c = linearIndicies[i][0], linearIndicies[i][1]
        linearized_matrix.append(matrix[r][c])

    return linearized_matrix


def spiral_matrix(N):
    N = 4
    M = 6

    MAP = [[0]*M for _ in range(N)] # Spiral Form of Indicies
    linearized_MAPindex = [] # Linear Form of Indicies
    cnt = 0
    direction = 0


    # 만약 N X M 의 직사각행렬이면 어떻게 될까?
    

    right = M-1
    down = N-1
    left = 0
    up = 1
    r = c = 0

    for i in range(N*M):
        MAP[r][c] = cnt
        cnt += 1
        linearized_MAPindex.append([r,c])

        if direction%4 == 0 and c == right:
            direction += 1
            right -= 1
        elif direction%4 == 1 and r == down:
            direction +=1
            down -= 1
        elif direction%4 == 2 and c == left:
            direction += 1
            left += 1
        elif direction%4 == 3 and r == up:
            direction += 1
            up += 1

        r += dr[direction%4]
        c += dc[direction%4]

    return MAP, linearized_MAPindex


MAP, linearized_MAPindex = spiral_matrix(N)

linearized_matrix = matrix_linearization(linearized_MAPindex, example_matrix)

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()


print('matrix indicies - spiral form')
MAP_printer(MAP)

print("linearized Indicies")
print(linearized_MAPindex)

print('matrix : ')
MAP_printer(example_matrix)

print("linearized matrix")
print(linearized_matrix)





