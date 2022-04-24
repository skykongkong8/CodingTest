my_list = [i for i in range(10)]
tmp = None
for i in range(10):
    cur = my_list[i]
    if tmp is not None:
        print(cur)
        print(tmp)


    tmp= cur