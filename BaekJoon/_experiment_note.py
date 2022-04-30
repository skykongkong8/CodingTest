threeDMAP = [[[]for i in range(5)] for j in range(5)]
import copy
# dup_threeDMAP = copy.deepcopy(threeDMAP)
def mapDup(MAP):
    dupMAP = MAP[:]

    return dupMAP
    
dup_threeDMAP = mapDup(threeDMAP)

threeDMAP[1][3].append(53)






print(dup_threeDMAP)