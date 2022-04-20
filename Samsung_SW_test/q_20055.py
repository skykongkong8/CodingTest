# 컨베이어 벨트 위의 로봇
"""
MAP = [[로봇순서, 내구도] : 1번째 칸(올리는 곳), [2, 1], ..., [1, 1] : N번째 칸 (내리는 곳) ,... , [False, 0]] 2N개
"""

def input_getter():
    N, K = map(int, input().split(' '))
    ng_MAP = list(map(int, input().split()))
    MAP = []
    for ng in ng_MAP:
        MAP.append([-1, ng])

    return N, K, MAP

def move(MAP, N, K, nextRobotNum):
    # 1. 벨트의 회전
    tail_of_belt = MAP[-1]

    nextMap = MAP[:]
    for i in range(1,2*N):
        nextMap[i] = MAP[i-1]
        
        # nextMap[i][1] -= 1

    nextMap = [MAP[-1]] + MAP[:-1]

    nextMap[N][0] = -1 # N-1이었던 것이 N으로 옮겨갔을 것이므로 로봇 떨어짐
    nextMap[N-1][0] = -1 # 로봇 즉시 떨어짐

    # nextMap[0] = tail_of_belt
    # print(f"After Belt Rotation : {nextMap}")

    # 2. 로봇의 이동
    robot_order = get_robot_order(nextMap, N)
    # print(f"robot_order : {robot_order}")
    for robot in robot_order:
        curRobotNum, curIndex = robot[0], robot[1]
        if curIndex != N-1:
            tmp_nextIndex = curIndex+1
            
            if nextMap[tmp_nextIndex][0] == -1 and nextMap[tmp_nextIndex][1] >= 1:
                if tmp_nextIndex != N-1 :
                    nextMap[tmp_nextIndex] = [curRobotNum, nextMap[tmp_nextIndex][1] - 1]
                else:
                    nextMap[tmp_nextIndex] = [-1, nextMap[tmp_nextIndex][1] - 1]
                nextMap[curIndex][0] = -1

        if curIndex == N-1:
            nextMap[curIndex][0] = -1 # 즉시 떨어짐
    # print(f"After Robot Move : {nextMap}")
    
    # 3. 로봇 올리기
    if nextMap[0][1] > 0:
        nextMap[0][0] = nextRobotNum
        nextMap[0][1] -= 1
        # print(f'Add new Robot {nextMap}')
    

    # 4. 내구도가 0인 칸의 개수 확인하기
    stopping_flag = check_broken(nextMap, K)

    return nextMap, nextRobotNum, stopping_flag

    
def get_robot_order(MAP, N):
    robot_order = []
    """
    robot_order = [[로봇순서, 인덱스], ...]
    """
    for j in range(N):
        curBelt = MAP[j] # [로봇순서, 내구도]
        if curBelt[0] != -1:
            robot_order.append([curBelt[0], j]) # 로봇이 있으면, 로봇의 순서와 로봇의 현재 인덱스를 함께 반환
        
    robot_order.sort(key=lambda a: a[0]) # 우선순위대로 소팅
    
    return robot_order

    
def check_broken(MAP, K):
    cnt = 0
    for belt in MAP:
        if belt[1] <= 0 :
            cnt += 1

    if cnt >= K:
        return True

    return False


if __name__ == "__main__":
    N, K, MAP = input_getter()
    nextRobotNum = 0

    while True:
        nextRobotNum += 1
        # print(f"iteration #{nextRobotNum} : {MAP}")
        
        MAP, nextRobotNum, stopping_flag = move(MAP, N, K, nextRobotNum)
        # print()
        

        if stopping_flag:
            break

        
        

    print(nextRobotNum)

"""
배운점
1. for문 말고도 리스트끼리의 덧셈으로 컨베이어 돌리기를 구현할 수 있다.
2. 직접 써본 [:] 인덱싱으로 copy를 쓰지 않고도 복사하여서 사용할 수 있다.

"""