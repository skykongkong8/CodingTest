matrix = [[i*j for i in range(1,10)] for j in range(1,10)]

rot_matrix = [list(row) for row in list(zip(*matrix[::-1]))]



print(matrix)

print(rot_matrix)