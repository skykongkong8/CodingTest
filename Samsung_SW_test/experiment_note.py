start = 0
def make_new_player():
    return [0, start, False]

plist = [make_new_player() for _ in range(4)]

plist[0][0] +=1
print(plist)


from itertools import product

lists = product(range(2), range(2), range(2))

for i in lists:
    print(i)