# 상어 초등학교

dr = [1,-1,0,0]
dc = [0,0,1,-1]

def input_getter():
    N = int(input())
    MAP = [[0]*N for _ in range(N)]

    students = []
    for i in range(N**2):
        student_info = list(map(int, input().split(' ')))
        student_info = [student_info[0], list(student_info[1:])]
        students.append(student_info)
        
    return N, MAP, students

def manhattan_distance(r_1, c_1, r_2, c_2):
    return abs(r_1 - r_2) + abs(c_1-c_2)

Satisfication_Hash = {
    0 : 0,
    1 : 1,
    2 : 10,
    3 : 100,
    4 : 1000
}

def sitting_criterion(student, MAP, N):
    seat_candidates = []
    # 조건1 선호하는 학생 수
    # 조건2 비어있는 칸 많은 칸
    # 조건3 row/column 작은 순
    for r in range(N):
        for c in range(N):
            if MAP[r][c] == 0:
                preferred_students = 0
                empty_seat_cnt = 0
                for k in range(4):
                    tmp_r, tmp_c = r + dr[k], c + dc[k]
                    if 0<= tmp_r < N and 0 <= tmp_c < N:

                        try:
                            if MAP[tmp_r][tmp_c][0] in student[1]:
                                preferred_students += 1
                                
                        except:
                            pass

                        if MAP[tmp_r][tmp_c] == 0:
                            empty_seat_cnt += 1

                curSeatScore = [preferred_students, empty_seat_cnt,-r, -c]

                seat_candidates.append(curSeatScore)

    seat_candidates.sort(key=lambda a : (a[0], a[1], a[2], a[3]), reverse = True)

    return -seat_candidates[0][2], -seat_candidates[0][3]

def find_favList_with_num(student_num, students):
    for i in range(len(students)):
        student = students[i]
        if student_num == student[0]:
            return student[1]
    return False

def give_seats(MAP, students, N):
    for student in students:
        opt_r, opt_c = sitting_criterion(student, MAP, N)

        MAP[opt_r][opt_c] = [student[0]]

    satisfcation_score = 0

    for r in range(N):
        for c in range(N):
            curStudentFavList = find_favList_with_num(MAP[r][c][0], students)
            if curStudentFavList:
                friend_score = 0
                for k in range(4):
                    tmp_r, tmp_c = r + dr[k], c + dc[k]
                    if 0 <= tmp_r < N and 0 <= tmp_c < N:
                        if MAP[tmp_r][tmp_c][0] in curStudentFavList:
                            friend_score += 1
            satisfcation_score += Satisfication_Hash[friend_score]
                            

    return satisfcation_score


if __name__ == "__main__":
    N, MAP, students = input_getter()
    score = give_seats(MAP,students, N)
    # for row in MAP:
    #     print(row)
    print(score)