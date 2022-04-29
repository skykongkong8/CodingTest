# 새로운 게임2

dr = [0,0,-1,1]
dc = [1,-1,0,0]

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

def input_getter():
    N, K = map(int, input().split(' '))
    MAP = []
    for _ in range(N):
        MAP.append(list(map(int, input().split(' '))))
    agents_list = []
    agentTowerMAP = [[False]*N for _ in range(N)] # 3차원 리스트는 우선 2차원을 만든 후 나중에 1차원 자료구조를 넣어주는 형태로 구현.
    
    for k in range(K):
        """
        agent = [agentNum, [agentPos], agentDir]

        agent_list = [agent, agent, agent, ... ]

        agentTower = [
            ...
            [ [agentNum, agentDir], [agentNum, agentDir], ... ] # 쌓여진 agent들의 순서
            ...
        ]
        """
        r, c, d = map(int, input().split(' '))
        r -= 1
        c -= 1
        d -= 1
        agent = [k, [r,c], d]
        agents_list.append(agent) 

        agentTowerMAP[r][c] = [agent] # 쌓을 수 있는 구조를 형성하려면?

    for i in range(len(agentTowerMAP)):
        for j in range(len(agentTowerMAP[0])):
            if agentTowerMAP[i][j] == False:
                agentTowerMAP[i][j] = list()



    return N, K, MAP, agents_list, agentTowerMAP

def reverse_agent_direction(direction):

    if direction == 0:
        direction = 1
    elif direction ==1:
        direction = 0
    elif direction == 2:
        direction = 3
    elif direction == 3:
        direction = 2

    return direction

def towerLengthChecker(agentTower):
    if len(agentTower) >= 4:
        return True
    else:
        return False


def move_agents(agents_list, agentTowers, MAP, N, K):
    endgame = False
    for a in range(len(agents_list)):
        agent = agents_list[a]
        agentNum = agent[0]
        noMovementFlag = False
        # print(f"current agent : {agent}\n")

        agentR, agentC = agent[1][0], agent[1][1]
        agentDir = agent[2]
        currentAgentTower = agentTowers[agentR][agentC]
        # print(f"current agent Tower : {currentAgentTower}\n")
        anyTowerLengthBiggerThanFourFlag = False
        agentTowerIndex = currentAgentTower.index(agent) # 현재 agent위를 다 데리고 가기위한
            
        actualMovingAgentTower = currentAgentTower[agentTowerIndex:] # 현재 agent위들
        # if currentAgentTower[:agentTowerIndex] == []:
        #     agentTowers[agentR][agentC] = [currentAgentTower[:agentTowerIndex]] # 기존에 있던 Tower에서 움직이는 부분을 없애줌
        # else:
        agentTowers[agentR][agentC] = currentAgentTower[:agentTowerIndex]
        # print(f"insert this to original towerPos {currentAgentTower[:agentTowerIndex]}")

        tmp_r, tmp_c = agentR + dr[agentDir], agentC + dc[agentDir]
        if 0 <= tmp_r < N and 0<= tmp_c < N:
            mapColor = MAP[tmp_r][tmp_c]          
            
            if mapColor == 0:
                agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])

            elif mapColor == 1:
                actualMovingAgentTower.reverse()
                # print(f"reversed tower : {actualMovingAgentTower}")

                agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])


            elif mapColor == 2:
                agents_list[a][2] = reverse_agent_direction(agentDir)
                agentDir = agents_list[a][2]
                tmp_r, tmp_c =  agentR + dr[agentDir], agentC + dc[agentDir]

                if 0<= tmp_r < N and 0 <= tmp_c < N:
                    newMapColor = MAP[tmp_r][tmp_c]
                    if newMapColor == 0:
                        agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                        anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])


                    elif newMapColor == 1:
                        actualMovingAgentTower.reverse()
                        # print(f"reversed tower : {actualMovingAgentTower}")
                        agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                        anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])


                    else:
                        agentTowers[agentR][agentC].extend(actualMovingAgentTower)
                        noMovementFlag = True
                        anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])
                else:
                    agentTowers[agentR][agentC].extend(actualMovingAgentTower)
                    noMovementFlag = True
                    # anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])
                        
        else:
            agents_list[a][2] = reverse_agent_direction(agentDir)
            agentDir = agents_list[a][2]
            tmp_r, tmp_c =  agentR + dr[agentDir], agentC + dc[agentDir]

            if 0<= tmp_r < N and 0 <= tmp_c < N:
                newMapColor = MAP[tmp_r][tmp_c]
                if newMapColor == 0:
                    agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                    anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])


                elif newMapColor == 1:
                    actualMovingAgentTower.reverse()
                    agentTowers[tmp_r][tmp_c].extend(actualMovingAgentTower)
                    anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])


                else:
                    agentTowers[agentR][agentC].extend(actualMovingAgentTower)
                    noMovementFlag = True

                    anyTowerLengthBiggerThanFourFlag = towerLengthChecker(agentTowers[tmp_r][tmp_c])
        if not noMovementFlag:
            totalTowerPos = [tmp_r, tmp_c]

            for agl in range(len(actualMovingAgentTower)):
                actualMovingAgentTower[agl][1] = totalTowerPos
                curAgent = actualMovingAgentTower[agl]
                agentNumberIndex = curAgent[0]
                # agentChangedDir = curAgent[2]

                agents_list[agentNumberIndex][1] = totalTowerPos
                # agents_list[agentNumberIndex][2] = agentChangedDir


            agents_list[a][1] = [tmp_r, tmp_c]
        #     print(f"updated agents_list : {agents_list}")
        # print("after agentMove: ")
        # MAP_printer(agentTowers)
        
        if anyTowerLengthBiggerThanFourFlag:
            endgame = True
            
    return agents_list, agentTowers, endgame

    

        
        


if __name__ == "__main__":
    N, K, MAP, agents_list, agentTowers = input_getter()
    time_step = 0
    timeOverflowFlag = False
    # print("init agentTowers")
    # MAP_printer(agentTowers)

    # print(f"init agentList : {agents_list}")
    while True:

        agents_list, agentTowers, endgame = move_agents(agents_list, agentTowers, MAP, N, K)
        time_step += 1
        # print(f"current TIME STEP : {time_step}\n")

        if endgame:
            break
        if time_step >= 1000:
            timeOverflowFlag = True
            break

    if timeOverflowFlag:
        print(-1)
    else:
        print(time_step)
            

"""
배운점

1. 3차원 리스트를 처음부터 생성하려고 하지 말자. 더헷갈린다.. (헷갈리는 요소: 기본 인덱싱, 이후 세부 자료구조 요소 접근 인덱싱 등 다 꼬임)
    차라리, 2차원 리스트를 생성한 뒤, 개별 요소를 만들어서 집어넣는 방식으로 해야한다.
    repeat: 1차원, 2차원 리스트만 만들 수 있다.
    
2. MAP 자료구조, towerMAP 자료구조, agents_list 자료구조 의 3중 이용 
"""