#Row 0 : The size N = 3, 4, ..., 50 of the whole field (identified 
# with a (N, N) square.
# Row 1, ...,i, ..., N : Row i of the aforementioned square, as string 
# of size N. The characters of such string are either 'X' (marking
# a water plant) either a blank space.
#
import sys

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

N = int(lines[0])
d = [[w for w in r] for r in lines[1:]]
w = set((i, j) for j in range(N) for i in range(N) if (d[i][j] is 'X'))
r = set()

for i in range(N):
    for j in range(N):
        if (i, j) in w:
            for v in range(-1, 2):
                for h in range(-1, 2):
                    t = (i + v, j + h)
                    if all(x in range(N) for x in t):
                        r.add(t)
                    
print(len(r) - len(w))