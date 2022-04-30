# 상어초등학교 리뷰

def input_getter():
    N = int(input())
    student_info = []
    for _ in range(N*N):
        a,b,c,d,e = map(int, input().split(' '))
        student_info.append([a, [b,c,d,e]])

    MAP = [[0]*N for _ in range(N)]

    """
    preference_list = [
        ...
        [ num, [pref1, pref2, pref3, pref4] ] : student_info[1] = preference_list
        ...
    ]
    
    """
    return N, student_info, MAP
dr = [0,0,1,-1]
dc = [1,-1,0,0]

def howManyCriterionsNearThisIndex(r, c, MAP, N, preference):
    empty = 0
    prefer = 0
    tmp_r, tmp_c = r, c
    for l in range(4):
        tmp_r, tmp_c = r+dr[l], c+dc[l]
        if 0<= tmp_r < N and 0 <= tmp_c < N:
            if MAP[tmp_r][tmp_c] == 0:
                empty += 1
            elif MAP[tmp_r][tmp_c] in preference:
                prefer += 1
    return prefer, empty

def distribute_students(student_info, MAP, N):
    preferenceMAP = [[0]*N for _ in range(N)]
    for i in range(N*N):
        studentNum, preference = student_info[i][0], student_info[i][1]
        seat_candidates = []
        for j in range(N):
            for k in range(N):
                if MAP[j][k] == 0:
                    prefer, empty = howManyCriterionsNearThisIndex(j, k, MAP, N, preference)
                    seat_candidates.append([prefer, empty, j, k]) # 마지막에 어짜피 다시 봐야해서 지금 어떤 자리에 앉았는지는 저장하지 않음!
        
        seat_candidates.sort(key = lambda a : (-a[0], -a[1], a[2], a[3]))
        optimal_seat = seat_candidates[0]
        # print(f"seat candidates : {seat_candidates}")
        # print(f"optimal seat : {optimal_seat}")
        opt_r, opt_c = optimal_seat[2], optimal_seat[3]

        MAP[opt_r][opt_c] = studentNum
        # MAP_printer(MAP)
        preferenceMAP[opt_r][opt_c] = preference

    return MAP, preferenceMAP


def compute_answer(MAP, N, preferenceMAP):
    preference_weight = {
        0 : 0,
        1 : 1,
        2 : 10,
        3 : 100,
        4 : 1000
    }
    satisfaction = 0
    for i in range(N):
        for j in range(N):
            studentNum = MAP[i][j]
            studentPreference = preferenceMAP[i][j]
            prefer, _ = howManyCriterionsNearThisIndex(i, j, MAP,N, studentPreference)

            satisfaction += preference_weight[prefer]

    return satisfaction

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

if __name__ == "__main__":
    N, student_info, MAP = input_getter()

    MAP, preferenceMAP = distribute_students(student_info, MAP, N)
    satisfaction = compute_answer(MAP, N, preferenceMAP)

    print(satisfaction)




