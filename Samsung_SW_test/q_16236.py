# 아기 상어
import sys
from collections import deque
MAP = []

class BabyShark():
    def __init__(self):
        self.size = 2
        self.mommy = False
        self.time = 0
        self.curPos = [0,0]

        self.fish_to_grow = 2
    
    def eat_and_grow(self, time_distance, fishPos):
        # 물고기는 이미 먹을 수 있다는 것이 확인된 상태, 먹은 후 성장 조건이 충족되었는지 확인하고, 충족되었다면 성장하는 함수
        # 만약 여러 물고기가 레이더에 잡히면 우선 수위를 정해서
        # 먹었으므로 시간 증가, 크기 증가
        
        # 이동 및 시간
        if len(fishPos) > 1:
            fishPos.sort(key=lambda x : (x[0], x[1]))
        # print(fishPos)
        self.curPos = fishPos[0]
        self.time += time_distance
        
        # 식사 및 성장
        MAP[self.curPos[0]][self.curPos[1]] = 0 # 먹었으니까 0
        self.fish_to_grow -=1
        if self.fish_to_grow == 0:
            self.size += 1
            self.fish_to_grow = self.size
        # """
        # 맵체커
        # """
        # map_checker(MAP)
        

    def search(self):
        # 먹을 수 있는 물고기를 탐색하고,  각 위치와 도달하는 시간을 반환하는 함수
        # 만약 먹을 수 있는 물고기가 없다면 엄마를 부른다.
        # movable_Map = self.get_movable_MAP()
        cost_Map, max_cost = self._bfs() # movable_Map
        # """
        # 맵체커
        # """
        # map_checker(movable_Map)
        # map_checker(cost_Map)

        time_distance = 1 # 0은 자신이 있는 곳이거나, 갈 수 없는 곳
        flag = False
        edible_fishes = []
        while (time_distance < max_cost+1):
            for i in range(len(cost_Map)):
                for j in range(len(cost_Map)):
                    if cost_Map[i][j] == time_distance:
                        if MAP[i][j] < self.size and MAP[i][j] != 0:
                            flag = True
                            edible_fishes.append([i,j])
            if flag:
                break
            time_distance += 1

        if not flag:
            self.mommy = True
            return [None], 0

        return edible_fishes, time_distance

    def _bfs(self):
        flag = False

        queue = deque()
        queue.append(self.curPos)
        visited_map = [[0]*len(MAP) for _ in range(len(MAP))] # 방문했는지를 체크하는 노드
        cost_map = [[0]*len(MAP) for _ in range(len(MAP))] # 최단 거리
        max_cost = 0
        
        while queue:
            # 굳이 다 찾을 필요 없이 이번 거리대에 있는, 먹을 수 있는 물고기를 찾으면 종료한다?
            curfish = queue.popleft()
            visited_map[curfish[0]][curfish[1]] = 1

            adj_idxes = self._get_adjacent_idxes(curfish)
            for idx in adj_idxes:
                # if movable_map[idx[0]][idx[1]] and not visited_map[idx[0]][idx[1]]: # 갈 수 있는 곳이고, 간 적이 없으면
                #     cost_map[idx[0]][idx[1]] = cost_map[curfish[0]][curfish[1]] + 1
                #     max_cost = max(max_cost, cost_map[idx[0]][idx[1]])
                #     queue.append(idx)
                if MAP[idx[0]][idx[1]] <= self.size and not visited_map[idx[0]][idx[1]]: # 갈 수 있는 곳이고, 간 적이 없으면
                    cost_map[idx[0]][idx[1]] = cost_map[curfish[0]][curfish[1]] + 1
                    max_cost = max(max_cost, cost_map[idx[0]][idx[1]])
                    
                    if not MAP[idx[0]][idx[1]] > self.size: # 만약 먹을 수까지 있다면, 더이상 걔 이상으로 찾을 필요 없음 (걔쪽 가지에 한해)
                        queue.append(idx)
            
        return cost_map, max_cost

    def _get_adjacent_idxes(self, pos):
        # 동서남북의 인접 위치들이 담긴 리스트를 반환한다.
        idx1 = [pos[0]+1, pos[1]]
        idx2 = [pos[0], pos[1]+1]
        idx3 = [pos[0], pos[1]-1]
        idx4 = [pos[0]-1, pos[1]]
        adj_idxes = [idx1, idx2, idx3, idx4]
        true_idxes = []
        for idx in adj_idxes:
            if 0<= idx[0] < len(MAP) and 0 <=idx[1] < len(MAP):
                true_idxes.append(idx)
        return true_idxes
    
    # def get_movable_MAP(self):
    #     movable_Map = [[0]*len(MAP) for _ in range(len(MAP))]
    #     for i in range(len(MAP)):
    #         for j in range(len(MAP)):
    #             if MAP[i][j] <= self.size:
    #                 movable_Map[i][j] = 1
    #     return movable_Map

def game():
    # 게임을 진행함. 한번의 탐색이 끝날 때마다 지날때마다 엄마를 불렀는지 확인해야함
    #1 처음 상어의 위치 파악
    shark = BabyShark()
    for i in range(len(MAP)):
        for j in range(len(MAP)):
            if MAP[i][j] == 9:
                shark.curPos = [i,j] # r,c
                MAP[i][j] = 0 # 앞으로의 탐색 편의상

    
    while not shark.mommy:
        #2 상어의 탐색
        edible_fishes, time_step = shark.search()
        if shark.mommy:
            break

        #3 탐색 성공 -> 상어 식사 후 탐색 재개
        shark.eat_and_grow(time_step, edible_fishes)
        # print(f"현재 시간 : {shark.time}\n 현재 사이즈 : {shark.size}")

    #4 탐색 실패 -> 상황 종료
    if shark.mommy:
        return shark.time
    

def input_getter():
    N = int(sys.stdin.readline())
    for i in range(N):
        row = list(map(int, sys.stdin.readline().split(' ')))
        MAP.append(row)
    
    return N, MAP

def map_checker(maps):
    for i in range(len(maps)):
        print(maps[i])
    print()

if __name__ == '__main__':
    N, MAP = input_getter()
    t = game()
    print(t)

# """#1 시간 초과 : 모든 물고기까지 다 찾으려해서 그렇다"""