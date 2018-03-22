###############################################################################
# Solution to the hydroponic problem (battledev (FR) 11/2017)                 #
#     https://questionsacm.isograd.com/codecontest/pdf/hydropons.pdf          #
# Name:     qad.py .                                                          #
# Indent:   = 4 spaces (no tab).                                              #
# Width:    79 (comment lines < 73).                                          #
# license:  Nope; consider the below code as public domain.                   #
###############################################################################
"""
    Row 0 : The size N = 3, 4, ..., 50 of the whole field (identified 
        with a (N, N) square.
    Row 1, ...,i, ..., N : Row i of the aforementioned square, as string 
        of size N. The characters of such string are either 'X' (marking
        a water plant) either a blank space.
"""
input = [ # for example... 
    "3", 
    "X..",
    "...",
    "..X",
]


lines = []
for line in input:
	lines.append(line.rstrip('\n'))

N               = int(lines[0])
map_of_water    = lines[1:]

water   = set()     # The water plants.
result  = set()     # Union of the cultivable fieds and the water plants 

def create_water():
    """
        We enlist X/water plants positions.
    """
    for i in range(N):
        string = map_of_water[i] 
        for j in range(N):
            if string[j] == 'X':
                water.add((i, j))
#

def update_result(i, j):
    if is_in_bounds(i, j):
        result.add((i, j))
#

def is_in_bounds(i, j):
    if i in range(N)  and j in range(N):
        return True 
    return False 
#

def is_there_water_in(i, j):
    for element in water:
        if element[0] == i and element[1] == j:
            return True 
    return False
#

# Veni
create_water()

# Vidi
for i in range(N):
    for j in range(N):
        if is_there_water_in(i, j):
            for v in range(-1, 2):
                for h in range(-1, 2):
                    update_result(i+v, j+h)
#

# Vici
print(len(result) -len(water))