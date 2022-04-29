from collections import deque

total_combinations = []
experiment_list = [[i,i+2] for i in range(6)]


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

combinations(deque(), 0, 4, experiment_list)

print(total_combinations)