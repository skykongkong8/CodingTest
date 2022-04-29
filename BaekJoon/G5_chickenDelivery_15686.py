# 치킨 배달
from collections import deque

def input_getter():
    N, M = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))
    
    return N, M, MAP

"""
아이디어
목표 : 치킨거리를 최소하는,
1. Brute Force로 13까지 해보라는 뜻인 것 같다. 그리고 그중 최댓값인 것을 출력하면 될 듯.

2. 그렇다면 예를 들어 m개의 치킨집을 남기는 iteration이라고 해보자:
    어떠어떠한 치킨집을 없애야 좋을까?

    - 아이디어 0 : brute force로 다 하나하나 선택하면서 (엄청난 computational complexity)
        -> 전체 주어진 치킨집 들 중에서 m개를 선택하여 그때 당시의 전체 치킨 거리를 계산한다.

    - 아이디어1 : 반대로 치킨집에서부터 '집 거리'를 계산하고, 그게 큰 순서부터?

    - 아이디어2 : 

"""

def get_direct_accessing_information(MAP, N):
    house_indicies = []
    chickens_indicies = []
    for r in range(N):
        for c in range(N):
            if MAP[r][c] == 1:
                house_indicies.append([r,c])
            elif MAP[r][c] == 2:
                chickens_indicies.append([r,c])

    return house_indicies, chickens_indicies

def manhattan_distance(r_1, c_1, r_2, c_2):
    return abs(r_1 - r_2) + abs(c_1 - c_2)

def get_chicken_distance(chickens_indicies, home_r, home_c, N):
    distance = N*N
    for chicken_index in chickens_indicies:
        chick_r, chick_c = chicken_index[0], chicken_index[1]
        tmp_chicken_distance = manhattan_distance(home_r, home_c, chick_r, chick_c)
        distance = min(tmp_chicken_distance, distance)
    return distance


def combinations(oneDarray, r):
    total_combinations = []
    n = len(oneDarray)
    
    for i in range(n):
        queue = deque()
        queue.append(oneDarray[i])
        while queue:
            curNum = queue.pop()







if __name__ == "__main__":
    N, M, MAP = input_getter()
    house_indicies, chickens_indicies = get_direct_accessing_information(MAP, N)
    for m in range(1, M+1):
        """각각의 m을 시도해보고, 최대 m을 답으로 출력하자."""
        

