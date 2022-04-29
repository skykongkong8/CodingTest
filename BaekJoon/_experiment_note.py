from collections import deque
from winreg import QueryInfoKey
experiment_list = [i for i in range(6)]

def combinations(oneDarray, r):
    total_combinations = []
    n = len(oneDarray)
    global_visited = [False]*n
    
    for i in range(n):
        if not global_visited[i]:
            queue = deque()
            visited = [False]*n
            queue.append([oneDarray[i], i])
            global_visited[i] = True
            visited[i] = True


            while queue:
                curData = queue.pop()
                curNum, curIndex = curData[0], curData[1]

                this_combination = [curNum]

                for j in range(r):
                    tmp_idx = curIndex+1*(j+1)

                    if 0 <= tmp_idx < n:
                        if not visited[tmp_idx]:
                            visited[tmp_idx] = True
                            queue.append([oneDarray[tmp_idx], tmp_idx])
                            this_combination.append(oneDarray[tmp_idx])
                    if len(this_combination) >= r:
                        total_combinations.append(this_combination)
                        break
    return total_combinations

            
total_combinations = []

def combinations(queue, curDepth, r, target_list):
    global total_combinations
    if len(queue) == r:
        total_combinations.append(list(queue))
        return
    
    elif curDepth == len(target_list):
        return
    
    queue.append(target_list[curDepth])

    combinations(queue, curDepth+1, r, target_list)

    queue.pop()
    combinations(queue, curDepth+1, r, target_list)

combinations(deque(), 0, 3, experiment_list)

print(total_combinations)


    
