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

total_combinations_list = []
def combinations(queue, depth, r, target_list):
    global total_combinations_list
    n = len(target_list)
    if len(queue) == r:
        total_combinations_list.append(list(queue))
        return
        
    elif depth == n:
        return

    queue.append(target_list[depth])
    combinations(queue, depth+1,r,target_list)

    queue.pop()
    combinations(queue, depth+1,r,target_list)

def compute_minimum_chicken_distance(MAP, N, M, house_indicies, chicken_indicies):
    global total_combinations_list
    total_combinations_list = []
    combinations(deque(), 0, M, chicken_indicies)
    all_possible_chicken_indicies_combinations = total_combinations_list
    optimal_chicken_distance = float('inf')

    for possible_chicken_indicies in all_possible_chicken_indicies_combinations:
        total_city_chicken_distance = 0
        for h in range(len(house_indicies)):
            houseR, houseC = house_indicies[h][0], house_indicies[h][1]
            chicken_distance = get_chicken_distance(possible_chicken_indicies, houseR, houseC, N)
            total_city_chicken_distance += chicken_distance
        
        optimal_chicken_distance = min(optimal_chicken_distance, total_city_chicken_distance)
    return optimal_chicken_distance     

if __name__ == "__main__":
    N, M, MAP = input_getter()
    house_indicies, chickens_indicies = get_direct_accessing_information(MAP, N)
    answer = float('inf')
    for m in range(1, M+1):
        """각각의 m을 시도해보고, 최대 m을 답으로 출력하자."""
        local_minimum = compute_minimum_chicken_distance(MAP, N, M, house_indicies, chickens_indicies)
        answer = min(answer, local_minimum)
    print(answer)
        

