from collections import Counter

my_list = [1,1,1,1,2,2,2,2,4,4,4,4,55,5,1,1,1,1,11,3,3,8,6,66,6,6,7,7,7,7]

count = Counter(my_list)
print(count)

print(count[1])

from collections import OrderedDict