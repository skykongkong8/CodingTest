def input_getter():
    T = int(input())
    test_case = []
    for _ in range(T):
        this_data = list(map(int, input().split(' ')))
        test_case.append(this_data)

    return T, test_case

N = 10
round(3.3)
def calculate_average(test_case, T):
    cnt = 1
    for data in test_case:
        avg = 0
        for i in range(N):
            avg += data[i]
        avg /= N
        print(f"#{cnt} {round(avg)}")
        cnt+=1




if __name__ == "__main__":
    T, test_case = input_getter()
    answer_list = calculate_average(test_case, T)

       