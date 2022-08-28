n = int(input())
nums = list(map(int, input().split(' ')))
for i in range(n):
    x = nums[i]
    if x <= 3:
        print('*' * x)
    else:
        print('*')
# print(*['*' * x if x <= 3 else '*' for x in nums], sep='\n')