import copy

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]



def food(array, x ,y):
    """
    상어가 먹을 수 있는 위치의 후보 반환
    """
    positions = []
    direction = array[x][y][1] # 상어의 현재 위치에서 1, 즉 방향을 불러옴
    for i in range(1,4):
        nx,ny = x+dx[direction], y + dy[direction] # 방향만큼 더해보면서
        if 0 <= nx < 4 and 0 <= ny < 4 and 1 <- array[nx][ny][0] <= 16: # 벗어나지 않는다면
            positions.append([nx, ny]) # 가능!
        x, y = nx, ny
    return positions # 갈 수 있는 좌표들을 담은 리스트의 반환


def find_fish(array, index):
    # 현재 배열의 특정 물고기 위치를 알려주는 함수
    # 없으면 None
    for i in range(4):
        for j in range(4):
            if array[i][j] == index:
                return (i,j)
    return None

def move_fish(array, now_x, now_y): # 한 턴마다 물고기의 전반적인 이동을 담당
    flag = False
    position = []
    for i in range(1,17):
        position = find_fish(array, i) # 이번 번호의 물고기의 위치 반환
        if position is None: # 물고기 없으면 다음으로 넘어간다
            continue
        x,y = position[0], position[1]
        dir = array[x][y][1] # 위치를 알면, 빠른 방향 탐색이 가능하다
        for j in range(8): # 모든 회전 방향이 가능한지 해본다.
            nx, ny = x + dx[dir], y + dy[dir]
            if not (nx == now_x and ny == now_y): # 상어의 위치와 비교해서 상어의 위치만 아니라면,
                array[x][y][0], array[nx][ny][0] = array[nx][ny][0], array[x][y][0]  # 그 위치의 물고기와 바꾸어줌!
                """
                엄청 간단하게 바꿀 수 있는 한줄 파이썬 코드!
                """
                array[x][y][1], array[nx][ny][1] = array[nx][ny][1], dir # 방향도 바꾸어줌!
                break
            dir = (dir+1)%8 # 방향의 overflow처리

def dfs(array, x, y, total):
    # MAP과 상어위치, 현재 점수를 input
    global answer
    # 글로벌 변수 answer로 재귀 함수의 init조건을 가능하게 할 수 있음 대박!

    array = copy.deepcopy(array) # 이건 왜한것임?
    
    number = array[x][y][0] # 현재위치의 물고기 먹기 
    array[x][y][0] = -1

    move_fish(array, x, y) # 물고기의 이동

    result = food(array,x,y) # 이동가능한 물고기들의 이치를 가져옴

    answer = max(answer, total+number) # 우선 아까 먹은 물고기 먹음처리 해주는데, 전체적인 상황에서 최댓값만을 answer로 기억함 global 변수선언이 확실히 유용하네
    # 그래서 그냥 모든 탐색을 해본 뒤 그 최댓값을 answer에 저장하게 됨.
    # return하지 않고도 값을 빼낼 수 있는, 재귀함수에서의 좋은 기술이라고 생각이 된다.
    
    for next_x, next_y in result:# 물고기들 중 뭐를 먹는 것이 우리의 목표인 누적 물고기 번호를 최대화해줄지 dfs함
        dfs(array, next_x, next_y, total + number) # 다음  dfs는 이번 물고기에서 먹었다는 것을 전제로 탐색을 해줌

if __name__ == "__main__":
    tmp = [list(map(int, input().split())) for _ in range(4)]
    array = [[None]*4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            array[i][j] = [tmp[i][j*2], tmp[i][j*2+1]-1] # array compment (value, direction)

    answer = 0
    dfs(array, 0,0,0)
    print(answer)

    



