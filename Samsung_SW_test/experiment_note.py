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

