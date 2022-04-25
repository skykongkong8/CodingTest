# 스타트 택시
def input_getter():
    N, M, oil = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))

    r_taxi, c_taxi = map(int, input().split(' '))
    r_taxi -= 1
    c_taxi -=1
    
    passengers = []
    for _ in range(M):
        this_row = list(map(int, input().split(' ')))
        for i in range(len(this_row)):
            this_row[i] -=1
        passengers.append(this_row)
        """
        passengers = [
            ...
            [ r_0, c_0, r_f, c_f ],
            ...
        ]
        """    
    return N, M, oil, MAP, r_taxi, c_taxi, passengers

dr = [1,-1,0,0]
dc = [0,0,1,-1]

from collections import deque

impossible_destination_flag = False

def get_shortest_path(MAP, r_taxi, c_taxi, r_dest, c_dest, N):
    global impossible_destination_flag
    queue = deque()

    visited = [[False]*N for _ in range(N)]
    costMAP = [[0]*N for _ in range(N)]

    visited[r_taxi][c_taxi] = True
    found_flag = False

    queue.append([r_taxi, c_taxi])
    while queue:
        curPos = queue.popleft()
        curR, curC = curPos[0], curPos[1]

        visited[curR][curC] = True

        

        for i in range(4):
            tmp_r, tmp_c = curR + dr[i], curC + dc[i]
            if 0<= tmp_r < N and 0<= tmp_c < N:
                if visited[tmp_r][tmp_c] == False:
                    visited[tmp_r][tmp_c] = True
                    if MAP[tmp_r][tmp_c] != 1:
                        costMAP[tmp_r][tmp_c] = costMAP[curR][curC] + 1
                        if (tmp_r, tmp_c) == (r_dest, c_dest):
                            found_flag = True # 이렇게하면 시간복잡도는 거의 같지 않나?
                            break
                        queue.append([tmp_r, tmp_c])
        if found_flag:
            break

    costMAP[r_taxi][c_taxi] = 0
    shortest_length = costMAP[r_dest][c_dest]

    # print(f"cost MAP!")
    # MAP_printer(costMAP)
    """
    문제 발생 : 벽으로 완전히 가로막혔을 때를 고려하지 못한다. MAP과 비교하여, 벽으로 완전히 가로막혔을 경우 아예 갈 수 없다면 바로 -1을 내놓자.
    백트래킹으로 정석적으로 했으면 이런 일이 생기진 않았을 텐데..
    """

    if costMAP[r_dest][c_dest] == 0:
        if (r_taxi, c_taxi) != (r_dest, c_dest):
            impossible_destination_flag = True # 이렇게하면 될지도


    

    return shortest_length


def get_costMAP(MAP, r_taxi, c_taxi, N):
    global impossible_destination_flag
    queue = deque()

    visited = [[False]*N for _ in range(N)]
    costMAP = [[0]*N for _ in range(N)]

    visited[r_taxi][c_taxi] = True
    queue.append([r_taxi, c_taxi])
    while queue:
        curPos = queue.popleft()
        curR, curC = curPos[0], curPos[1]

        visited[curR][curC] = True

        for i in range(4):
            tmp_r, tmp_c = curR + dr[i], curC + dc[i]
            if 0<= tmp_r < N and 0<= tmp_c < N:
                if visited[tmp_r][tmp_c] == False:
                    visited[tmp_r][tmp_c] = True
                    if MAP[tmp_r][tmp_c] != 1:
                        costMAP[tmp_r][tmp_c] = costMAP[curR][curC] + 1
                        queue.append([tmp_r, tmp_c])


    costMAP[r_taxi][c_taxi] = 0

    # print(f"cost MAP!")
    # MAP_printer(costMAP)
    """
    문제 발생 : 벽으로 완전히 가로막혔을 때를 고려하지 못한다. MAP과 비교하여, 벽으로 완전히 가로막혔을 경우 아예 갈 수 없다면 바로 -1을 내놓자.
    백트래킹으로 정석적으로 했으면 이런 일이 생기진 않았을 텐데..
    """

    return costMAP
"""
시간초과가 떴다.
아무래도 backtracking해서 찾았을 때 바로 break이 아니라서?
근데 지금이랑 다를게 있나?

******* 이유 : 손님별로 하나하나 다 BFS를 돌았기 때문! BFS한번만 돌아도 손님별 위치 다 나오기 때문에 한번만 해도 된다! 

"""

def oilChecker(oil):
    if oil < 0:
        return False
    return True

def getNextPassenger(passengerList, r_taxi, c_taxi, N, MAP):
    global impossible_destination_flag
    passenger_data = []
    """
    passenger_data = [
        ...
        [ distance, [passengers[i]] ]
        ...

    ]
    """
    costMAP = get_costMAP(MAP, r_taxi, c_taxi, N)
    for p_index in passengerList:
        passengerR, passengerC = p_index[0], p_index[1]
        passengerD = costMAP[passengerR][passengerC]
        passenger_data.append([passengerD, [passengerR, passengerC,p_index[2],p_index[3]]])
    if passenger_data:
        passenger_data.sort(key = lambda a: (a[0], a[1][0], a[1][1]))
        
        return passenger_data

    else:
        impossible_destination_flag = True
        return False


def taxiMove(passengers, MAP, oil, r_taxi, c_taxi, N):
    global impossible_destination_flag
    """
        passengers = [
            ...
            [ r_0, c_0, r_f, c_f ],
            ...
        ]
        """    
    missionCompleteFlag = True

    while True:
        curSchedulings = getNextPassenger(passengers, r_taxi, c_taxi, N, MAP)
        if curSchedulings:
            curScheduling = curSchedulings[0]
            fuel_to_passenger, r_0, c_0, r_f, c_f = curScheduling[0], curScheduling[1][0], curScheduling[1][1], curScheduling[1][2], curScheduling[1][3]
            oil -= fuel_to_passenger
            # print(f"oil left1 : {oil}")
            r_taxi, c_taxi = r_0, c_0

            if oil <= 0:
                missionCompleteFlag = False
                break
                
            fuel_to_destination = get_shortest_path(MAP, r_taxi, c_taxi, r_f, c_f, N)
            if impossible_destination_flag:
                missionCompleteFlag = False
                break

            oil -= fuel_to_destination
            # print(f"oil left2 : {oil}")

            r_taxi, c_taxi = r_f, c_f

            if not oilChecker(oil):
                missionCompleteFlag = False
                break

            oil += 2*(fuel_to_destination) #+ fuel_to_passenger)
            # print(f"oil charged : {oil}")


            passengers = []
            for i in range(1, len(curSchedulings)):
                passengers.append(curSchedulings[i][1])
        else:
            break

    return missionCompleteFlag, oil

    
def print_answer(missionCompleteFlag, oil):
    if missionCompleteFlag:
        print(oil)
    else:
        print(-1)


    

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

if __name__ =='__main__':
    N, M, oil, MAP, r_taxi, c_taxi, passengers = input_getter()

    missionCompleteFlag, oil = taxiMove(passengers, MAP, oil, r_taxi, c_taxi, N)

    print_answer(missionCompleteFlag, oil)


"""
배운점

1. 쉬운 문제라고 얕보다가 엄청난 시간을 잡아먹은 문제 (...)
    쉬운 문제를 얕잡아보지 말자.

2. BFS를 사용하는 상황에 대해 인지하자. 현 고객별로 BFS를 계속해서 하는 것 때문에 시간초과가 났다.
    현 상황에서 RADAR로 BFS 한번만 돌려서 distance transformation을 한 후, 그에 맞게 행동하면됨.

3. 위처럼 생각하게 된 이유는 함수를 한가지로만 사용하려고 고집하다보니..
    최단 '거리' 만을 받아오는 함수를 짜려다 보니 costMAP이라는 좋은 자료 구조를 만들고도 못쓰는 상황이었다.
    그냥 리턴만 해서 써도 되니까, 좋은 구조가 있으면 쓰도록 하고, 어떤 컨텍스트에서 사용하는지 이해하고 쓰자.

4. 인풋을 
    for _ in range(M):
    sy, sx, ey, ex = map(int, input().split())
    passenger_start.append([sy - 1, sx - 1])
    passenger_end.append([ey - 1, ex - 1])
    이렇게 나눠서 받을 수 있다는 것도 인지하자. 사실 쉬운 것이지만 순간적으로 생각 못했다. 이러면 훨씬 수월했을 것.

5. 찾는 대상에서 지우기 스킬:
    직접 지우는 방법도 있지만 비교상의 대상에서 제외되는 값으로 설정하는 방법도 있다.
    여기서의 경우,
    passengers[idx] = [-1,-1] 등으로 있을수없는 수를 넣어줘도 된다.


"""