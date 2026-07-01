s = [
    [1,2,3,4,5],
    [6,7,8,9,10],
    [11,12,13,14,15],
    [16,17,18,19,20]
]
for i in range(len(s)):
    for j in range(len(s[i])):
        s[i][j] = s[i][j] * 2

print(s)

      