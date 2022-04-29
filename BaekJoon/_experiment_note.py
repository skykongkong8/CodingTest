threeD_map = [[[False]]*10 for _ in range(10)]

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

for r in range(len(threeD_map)):
    for c in range(len(threeD_map[0])):
        if not threeD_map[r][c][0]:
            threeD_map[r][c][0] = list()

MAP_printer(threeD_map)