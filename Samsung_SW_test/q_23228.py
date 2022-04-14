# 주사위 굴리기 2
from collections import deque
dr = [0,0,1,-1] # MAP 동서남북
dc = [1,-1,0,0]

"""
주사위 프로파일 모델링:
'TOP' : 현재 맨 위인 수
나머지 : N이 위에 있을 때, 동-서-남-북 으로 갔을  때의 각각 맨 위에 오는 수

주사위가 YAW회전하지 않기 때문에 사용 가능한 모델이다. 즉, 하나의 TOP수에 대해, 하나의 profile밖에 존재할 수 없다! # 이 생각이 틀린 것으로 판명남!
"""
dice_profile = {
    1 : [4,3,2,5],
    2 : [6,1,3,4],
    3 : [6,1,5,2],
    4 : [1,6,5,2],
    5 : [4,3,1,2],
    6 : [4,3,5,2]
}

class Dice:
    def __init__(self):
        self.curPos = [0,0]
        self.curDir = 0
        self.TOP = 1
        self.score = 0
        
        self.profile =  {
                            1 : [4,3,2,5],
                            2 : [6,1,3,4],
                            3 : [6,1,5,2],
                            4 : [1,6,2,5],
                            5 : [4,3,1,2],
                            6 : [4,3,5,2]
                        }

        self.profilev2 = {
            'TOP' : 1,
            0 : 3, # 동
            1 : 4, # 서
            2 : 5, # 남
            3 : 2, # 북
            'BOTTOM' : 6
        }

    def Bottom(self):
        top_down_cache = {
            1 : 6,
            6 : 1,
            2 : 5,
            5 : 2,
            3 : 4,
            4 : 3
        }
        return top_down_cache[self.TOP]

    def go(self, dsnb):
        total_dsnb = [0,1,2,3]
        going_direction = dsnb
        reverse_direction = reverse_normal_dsnb(dsnb)
        total_dsnb.remove(going_direction)
        total_dsnb.remove(reverse_direction)

        neighboring_direction_1 = total_dsnb[0]
        neighboring_direction_2 = total_dsnb[1]

        new_dice_profile = {}

        new_dice_profile[going_direction] = self.profilev2['TOP']
        new_dice_profile[reverse_direction] = self.profilev2['BOTTOM']
        new_dice_profile['TOP'] = self.profilev2[reverse_direction]
        new_dice_profile['BOTTOM'] = self.profilev2[going_direction]

        new_dice_profile[neighboring_direction_1] = self.profilev2[neighboring_direction_1]
        new_dice_profile[neighboring_direction_2] = self.profilev2[neighboring_direction_2]

        self.profilev2 = new_dice_profile
        self.TOP = self.profilev2['TOP']

        # 동쪽(X)으로 가면 -> 서(X')이 curTOP (= 동(X)가 curBOTTOM), 남and북 유지, TOP이 cur서 (= BOTTOM이 cur동),  

        # 서쪽으로 가면 -> 
    def rotate(self, CCW_or_CW):
        new_dice_profile = {}
        new_dice_profile['TOP'] = self.profilev2['TOP']
        new_dice_profile['BOTTOM'] = self.profilev2['BOTTOM']
        if CCW_or_CW == 0: # CCW
            new_dice_profile[3] = self.profilev2[1]
            new_dice_profile[1] = self.profilev2[3]
            new_dice_profile[0] = self.profilev2[2]
            new_dice_profile[2] = self.profilev2[0]
        elif CCW_or_CW == 1: # CW
            new_dice_profile[3] = self.profilev2[0]
            new_dice_profile[1] = self.profilev2[2]
            new_dice_profile[0] = self.profilev2[3]
            new_dice_profile[2] = self.profilev2[1]


        self.profilev2 = new_dice_profile


# 또다른 dice 모델링 아이디어
"""
dice = [
    TOP,
    동,
    서,
    남,
    북,
    BOTTOM
]
동쪽(X)으로 가면 -> 동(X)이 curTOP (= 서(X')가 curBOTTOM), 남and북 유지, TOP이 cur서 (= BOTTOM이 cur동),  
YAW 회전:
CW -> TOP/BOTTOM유지, 남이 cur동(= 북이 cur서), 동이 cur북 (= 서가 cur남)
CCW -> TOP/BOTTOM유지, 남이 cur서(= 북이 cur동), 동이 cur남 (= 서가 cur북) 
"""

dice = Dice()

def input_getter():
    N, M, K = map(int, input().split(' '))
    MAP = []
    
    for _ in range(N):
        this_row = list(map(int, input().split(' ')))
        MAP.append(this_row)

    return N, M, K, MAP

def roll_dice(dice, dsnb): # 동 : 0, 서 : 1, 남 : 2,  북 : 3
    """동/서/남/북과 현재 TOP 수에 따른 다음 Top 수 변경 후 dice 오브젝트 다시 반환"""
    current_top_number = dice.TOP
    current_dsnb_profile = dice.profile[current_top_number]

    dice.TOP = current_dsnb_profile[dsnb]

    return dice

def circulating_dsnb_bounder(circulating_dsnb):
    if circulating_dsnb > 3:
        circulating_dsnb -= 4
    elif circulating_dsnb < 0:
        circulating_dsnb += 4
    return circulating_dsnb

def circulating_dsnb_to_normal_dsnb(circulating_dsnb):
    hasher = {
        0 : 0,
        1 : 3,
        2 : 1,
        3 : 2
    }
    return hasher[circulating_dsnb]

def normal_dsnb_to_circulating_dsnb(normal_dsnb):
    hasher = {
        0 : 0,
        3 : 1,
        1 : 2,
        2 : 3
    }
    return hasher[normal_dsnb]

def get_next_direction(A, B, dsnb):    
    circulating_dsnb = normal_dsnb_to_circulating_dsnb(dsnb)
    circulating_dsnb_list = [0,1,2,3] # circulating_dsnb : 동북서남 +1하면 CCW -1하면 CW
    CCW_or_CW = -1

    if A == B:
        return dsnb, CCW_or_CW

    elif A > B:
        CCW_or_CW = 1
        circulating_dsnb -= 1
        circulating_dsnb = circulating_dsnb_bounder(circulating_dsnb)
        return circulating_dsnb_to_normal_dsnb(circulating_dsnb), CCW_or_CW
    
    elif A < B:
        CCW_or_CW = 0
        circulating_dsnb += 1
        circulating_dsnb = circulating_dsnb_bounder(circulating_dsnb)
        return circulating_dsnb_to_normal_dsnb(circulating_dsnb), CCW_or_CW

def reverse_normal_dsnb(normal_dsnb):
    hasher = {
        0 : 1,
        1 : 0,
        2 : 3,
        3 : 2
    }
    return hasher[normal_dsnb]

def move_dice(MAP, M, N, dice):
    """주어진 MAP에 적힌 대로, 방향을 정해 주사위를 움직인다. 1회 움직일 때마다 점수를 쌓아나간다. K번 호출되는 함수"""
    curR, curC = dice.curPos[0], dice.curPos[1]

    dsnb = dice.curDir
    nextR, nextC = curR + dr[dsnb], curC + dc[dsnb]

    if not (0 <= nextR < N and 0<= nextC < M): # 격자를 벗어날 경우 방향을 반대로 전환한다.
        # print(f"WARNING : Out of Index!")
        prev_dsnb = dice.curDir
        dsnb = reverse_normal_dsnb(dsnb)
        dice.curDir = dsnb
        # print(f"switch current direction from : {prev_dsnb} to : {dice.curDir}\n")

        nextR, nextC = curR + dr[dsnb], curC + dc[dsnb]

    dice.curPos = [nextR, nextC]
    
    # dice = roll_dice(dice, dsnb) # 다음 TOP을 업데이트해주는 함수 roll_dice
    dice.go(dsnb) # dice 프로파일 업데이트

    # A = dice.Bottom() # TOP을 알면 Bottom도 안다.
    A = dice.profilev2['BOTTOM']
    B = MAP[nextR][nextC]

    next_dsnb, CCW_or_CW = get_next_direction(A, B, dsnb)
    
    # if CCW_or_CW != -1:
    #     dice.rotate(CCW_or_CW)

    dice.curDir = next_dsnb

    score = get_score(MAP, B, dice, N, M)
    dice.score+=score

    return dice

def get_score(MAP, B, dice, N, M):
    """도착한 장소에서의 점수를 계산해내는 함수 bfs/dfs로 계산하면 될듯"""
    total_size_of_connected_component = 1
    root_r, root_c = dice.curPos[0], dice.curPos[1]
    root = [root_r, root_c]
    visited_MAP = [[False]*M for _ in range(N)]
    visited_MAP[root_r][root_c] = True
    queue = deque()
    queue.append(root)

    while queue:
        current_position = queue.pop()
        current_r, current_c = current_position[0], current_position[1]

        for i in range(4):
            tmp_r, tmp_c = current_r + dr[i], current_c + dc[i]
            if 0 <= tmp_r < N and 0<= tmp_c < M:
                if  visited_MAP[tmp_r][tmp_c] == False:
                    visited_MAP[tmp_r][tmp_c] = True
                    if MAP[tmp_r][tmp_c] == B:                   
                        queue.append([tmp_r, tmp_c])
                        total_size_of_connected_component += 1
    total_score = total_size_of_connected_component * B

    return total_score





if __name__ == "__main__":
    N, M, K, MAP = input_getter()
    for _ in range(K):
        # print(f"curTOP : {dice.TOP}")
        # print(f"curProfile : {dice.profilev2}")
        # print(f"curPos : {dice.curPos}")
        # print(f"curDir : {dice.curDir}")
        # print(f"curScore : {dice.score}")
        # print()

        dice = move_dice(MAP, M, N, dice)
        

    # print(f"curTOP : {dice.TOP}")
    # print(f"curProfile : {dice.profilev2}")
    # print(f"curPos : {dice.curPos}")
    # print(f"curDir : {dice.curDir}")
    # print(f"curScore : {dice.score}")
    ultimate_score = dice.score

    print(ultimate_score)




"""
교훈 : 문제를 잘 읽자.....
그리고 주사위를 모델링하는 법을 배우게 되었다. 이번에 생각해낸 아이디어가 참 좋은 것 같다.
주사위와 같이 유한한 면을 가지고 있는 물체의 경우 하드코딩하는 것도 방법이다.
추가적으로 상황을 잘 인지해야 한다. 주사위가 yaw 방향으로 회전하는지 회전하지 않는지 늘 체크하자!!!

처음 시도했던 profile은 아예 성립될 수 없음을 인지하자. 하나의 눈 당 꼭 하나의 프로파일만 존재한다는 것은 말이 안된다. 다양한 방향으로 굴릴 수 있기 때문에 좌우좌우로만 돌다보면 바뀔 것이다.

새로 만든 단순한 딕셔너리 프로파일이 유용함을 인지하자.
하드 코딩한 클래스 함수 go와 rotate의 포맷에 대해서 잘 기억하자.

"""
