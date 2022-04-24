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

# 6.  