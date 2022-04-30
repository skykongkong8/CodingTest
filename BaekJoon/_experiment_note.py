from collections import deque

total_combinations_list = []

def combinations(queue, depth, r, target_list):
    global total_combinations_list
    n = len(target_list)
    if len(queue)==r:
        total_combinations_list.append(list(queue))
        return

    elif depth == n:
        return
    
    queue.append(target_list[depth])
    combinations(queue, depth+1, r, target_list)

    queue.pop()
    combinations(queue, depth+1, r, target_list)


target = [i+1 for i in range(5)]

combinations(deque(), 0, 2, target)
print(total_combinations_list)