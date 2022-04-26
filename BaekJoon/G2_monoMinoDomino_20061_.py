# 모노미노도미노

from torch import block_diag


def input_getter():
    N = int(input())
    block_sequence = []
    for _ in range(N):
        blocknum, x, y = map(int, input().split(' '))
        block_sequence.append([blocknum, [x-1, y-1]])
    MAP = [[0]*10 for _ in range(10)]
    
    """
    block_sequence = [
        ...
        [ blocknum, [ r, c ] ]
        ...
    ]
    """
    return N, block_sequence, MAP

def makeBlockShape(blockNum, r, c):
    if blockNum == 1:
        return [ blockNum, [[ r, c ]] ]

    elif blockNum == 2:
        return [ blockNum, [[ r, c ], [r, c+1]] ]

    elif blockNum == 3:
        return [blockNum, [ blockNum, [[ r, c ], [r+1, c]] ]]


def setBlock_to_redArea(block, MAP):
    """
    block = [ blocknum, [ r, c ] ]
    """
    blockShape = makeBlockShape(block[0], block[1][0], block[1][1])

    MAP = GreenGravity(MAP, blockShape)
    MAP = BlueGravity(MAP, blockShape)

    return MAP
    

def countGreenAndBlueTiles(MAP):
    total_Cnt = 0
    rot_MAP = [list(row) for row in list(zip(*MAP[::-1]))]
    for r in range(5,10):
        for c in range(4):
            total_Cnt += MAP[r][c]
            total_Cnt += rot_MAP[r][c]

    return total_Cnt

def GreenGravity(MAP, blockShape):
    """
    blockShape = [ blockNum, [[r,c], [r+1, c]] ] 등
    """
    blockIndicies = blockShape[1]
    blockNum = blockShape[0]

    while True:
        if blockNum == 1:
            block_r, block_c = blockIndicies[0][0], blockIndicies[0][1]
            tmp_block_r = block_r + 1
            if 0 <= tmp_block_r < 10 and MAP[tmp_block_r][block_c] == 0:
                block_r = tmp_block_r
            else:
                break

        elif blockNum == 2 :
            for bi in range(len(blockIndicies)):
                block_r, block_c = blockIndicies[bi][0], blockIndicies[bi][1]

                tmp_block_r = block_r + 1
                if 0 <= tmp_block_r < 10: 
                    if MAP[tmp_block_r][block_c] == 0:
                        block_r = min(blockIndicies[0][0], blockIndicies[1][0])
                        block_c = min(blockIndicies[0][1], blockIndicies[1][1])
                    else:
                        break
                else:
                    break


        elif blockNum == 3 :
            block_r, block_c = blockIndicies[1][0], blockIndicies[1][1]
            tmp_block_r = block_r + 1
            if 0 <= tmp_block_r < 10: 
                if MAP[tmp_block_r][block_c] == 0:
                    block_r = tmp_block_r
                else:
                    block_r = tmp_block_r - 1
                    break
            else:
                block_r = tmp_block_r - 1
                break
        
    if blockNum == 1:
        MAP[block_r][block_c] = blockNum
    elif blockNum == 2:
        MAP[block_r][block_c] = blockNum
        MAP[block_r][block_c+1] = blockNum
    elif blockNum == 3:
        MAP[block_r][block_c] = blockNum
        MAP[block_r +1][block_c] = blockNum
    
    return MAP

def BlueGravity(blockShape, MAP):
    rotMAP = [list(row) for row in list(zip(*MAP[::-1]))] # 이게 시계방향 맞나 -> 확인

    MAP = GreenGravity(rotMAP, blockShape)

    MAP = [list(row) for row in list(zip(*MAP))[::-1]]

    return MAP

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()







if __name__ == '__main__':
    N, block_sequence, MAP = input_getter()
    for BLOCK_INDEX in range(N):
        current_block_information = block_sequence[BLOCK_INDEX]

        MAP = setBlock_to_redArea(current_block_information, MAP)
        print('after GREEN BLUE GRAVITY')
        MAP_printer(MAP)





