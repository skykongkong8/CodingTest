# 조별과제

def input_getter():
    N = int(input())
    test_case = []

    for _ in range(N):
        num = int(input())
        test_case.append(num)
    return N, test_case

def distribute_students(N, test_case):
    for i in range(N):
        total_students = test_case[i]

        answer = int(total_students/3)
        print(f"#{i+1} {answer}")

if __name__ == "__main__":
    N, test_case = input_getter()
    distribute_students(N, test_case)