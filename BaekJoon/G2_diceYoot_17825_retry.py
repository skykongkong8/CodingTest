# 주사위 윷놀이

def input_getter():
    dice = list(map(int, input().split(' ')))

    return dice

"""
MAP을 어떻게 구현할 것인가? -> 
1. 시작/도착/파란색칸을 기준으로 잘라서 구현 해서 점프점프
2. 각각을 노가다 노드로 만들어서 그래프처럼 묶자?

"""
class Node:
    def __init__(self, num):
        self.num = num
        self.red = None
        self.blue = None

start = Node(0)
destination = Node(-1)

two = Node(2)
four = Node(4)
six = Node(6)
eight = Node(8)
ten = Node(10)
twelve = Node(12)
thirteen = Node(13)
fourteen = Node(14)
sixteen_1 = Node(16)
sixteen_2 = Node(16)
eightteen=Node(18)
nineteen = Node(19)
twenty = Node(20)
twentytwo_1 = Node(22)
twentytwo_2 = Node(22)
twentyfour_1 = Node(24)
twentyfour_2 = Node(24)
twentyfive = Node(25)
twentysix_1 = Node(26)
twentysix_2 = Node(26)
twentyseven = Node(27)
twentyeight_1 = Node(28)
twentyeight_2 = Node(28)
thirty_1 = Node(30)
thirty_2 = Node(30)
thirtytwo = Node(32)
thirtyfour = Node(34)
thirtyfive = Node(35)
thirtysix = Node(36)
thirtyeight = Node(38)
fourty = Node(40)

two.red = four
four.red = six
six.red = eight
eight.red = ten
ten.red = twelve
twelve.red = fourteen
fourteen.red = sixteen_1
sixteen_1.red = eightteen
eightteen.red = twenty
twenty.red = twentytwo_1
twentytwo_1.red = twentyfour_1
twentyfour_1.red = twentysix_1
twentysix_1.red = twentyeight_1
twentyeight_1.red = thirty_1
thirty_1.red = thirtytwo
thirtytwo.red = thirtyfour
thirtyfour.red = thirtysix
thirtysix.red = thirtyeight
thirtyeight.red = fourty
fourty.red = destination


ten.blue = thirteen
thirteen.red = sixteen_2
sixteen_2.red = nineteen
nineteen.red = twentyfive
twentyfive.red = thirty_2
thirty_2.red =thirtyfive
thirtyfive.red = fourty

twenty.blue = twentytwo_2
twentytwo_2.red = twentyfour_2
twentyfour_2.red = twentyfive

thirty_1.blue = twentyeight_2
twentyeight_2.red = twentyseven
twentyseven.red = twentysix_2
twentysix_2.red = twentyfive

start.red = two


# 4개의 말

def make_new_player():
    """
    player = [
        score, : Int
        curPos, : Node()
        isFinished : Bool
    ]
    """
    return [0, start, False]

def playerMove(player, N):
    # 주사위 눈금 N만큼 움직이는 함수
    if not player[2]:
        if player[1].blue is not None:
            player[1] = player[1].blue
            player[0] += player[1].num

            for p in range(N-1):
                player[1] = player[1].red
                if player[1].num != -1:
                    player[0] += player[1].num

                elif player[1].num == -1:
                    player[2] = True
                    break
        
        else:
            for p in range(N):
                player[1] = player[1].red
                if player[1].num != -1:
                    player[0] += player[1].num

                elif player[1].num == -1:
                    player[2] = True
                    break
        
    # if player[2] == True:
    #     return player
    return player

def getTotalScore(player_list):
    TotalScore = 0
    for player in player_list:
        TotalScore += player[0]

    return TotalScore

def isInSamePlace(player1, player2):
    """
    # 특수 케이스 : 말이 이동을 마치는 칸에 다른말이 있는 경우를 잘 체크 : 현재 num과 red의 num이 모두 같은면 같은 장소에 있는 것.
    """
    if player1[1].num == player2[1].num:
        if player1[1].red.num == player2[1].red.num:
            return True
    return False

from itertools import product

def tryForAllCases(dice):
    """
    모든 player들별, 그들에게 주어진 dice눈금 등을 할당해서 각각의 경우에 대한 점수를 얻은 후 최댓값 업데이트 방식으로 도출하는 함수
    """
    MAXIMUM = -1
    
    # 어떻게 각 player들에게 눈금을 나누어서 분배할 것인가?
    # 아이디어 1 : 순열 (순서가 상관 있으므로)
    # 각 player끼리는 구분이 없으므로, 눈금을 분배하기만 하면 됨
    # 꼭 모두 4 개로 나눌 필요는 없고, 1개 분배, 2개 분배, 3개 분배, 4개 분배 이렇게 각각에 대하여 해보아야함.
    # 아 근데 눈금 순서는 픽스임..!
    
    

    # 1 플레이어 하나만 쓰는 경우:
    player = make_new_player()
    for i in range(len(dice)):
        curDice = dice[i]
        if player[2] != True:
            player = playerMove(player, curDice)
        else:
            break
    
    MAXIMUM = max(MAXIMUM, player[0])

    # 2 플레이어 둘 쓰는 경우:
    

    # 각 플레이어가 어느 눈금을 선택할지를 정해야함
    # playOrderList = product(range(2),range(2),range(2),range(2),range(2),range(2),range(2),range(2),range(2),range(2))
    
    # for order in playOrderList:
    #     player_list = [make_new_player() for _ in range(2)]
    #     commonPlaceFlag = False
    #     for i in range(len(order)):
    #         player = player_list[order[i]]
    #         curDice = dice[i]
    #         if player[2] != True:
    #             player = playerMove(player, curDice)
    #         else:
    #             break
            
    #         if isInSamePlace(player_list[0], player_list[1]):
    #             commonPlaceFlag = True
    #     if commonPlaceFlag:
    #         score = 0
    #     else:
    #         score = getTotalScore(player_list)
    #     MAXIMUM = max(score, MAXIMUM)
    
    for P in range(2,5):
        playOrderList = product(range(P),range(P),range(P),range(P),range(P),range(P),range(P),range(P),range(P),range(P))
        for order in playOrderList:
            player_list = [make_new_player() for _ in range(P)]
            commonPlaceFlag = False
            for i in range(len(order)):
                player = player_list[order[i]]
                curDice = dice[i]
                if player[2] != True:
                    player = playerMove(player, curDice)
                else:
                    break
                
                if isInSamePlace(player_list[0], player_list[1]):
                    commonPlaceFlag = True
            if commonPlaceFlag:
                score = 0
            else:
                score = getTotalScore(player_list)
            MAXIMUM = max(score, MAXIMUM)
    return MAXIMUM

if __name__ == "__main__":
    dice = input_getter()
    ans = tryForAllCases(dice)
    print(ans)


    




