###############################################################################
# Solution to DNA problem (battledev (FR) 11/2017)                            #
#     https://questionsacm.isograd.com/codecontest/pdf/DNA.pdf                #
# Name:     dna.py .                                                          #
# Indent:   = 4 spaces (no tab).                                              #
# Width:    79 (comment lines < 73).                                          #
# license:  Nope; consider the below code as public domain.                   #
###############################################################################

# inputs: BEGINNING ###########################################################
input = [ # for example:
    "6", 
    "G", 
    "C", 
    "A", 
    "T", 
    "T", 
    "ACG"
]


lines = []
for line in input:
	lines.append(line.rstrip('\n'))

N           = int(lines[0])
string_     = lines[1: ]
full_length = len("".join(string_))
half_length = int(full_length/2)
#

def permute(a_list):
    """
        returns all permutations of list.
    """
    n = len(a_list)
    # 
    if n < 2:
        return [a_list]
    #
    result = []
    for i in range(n):
        _ = list(a_list[1: ])
        if i > 0: 
            _[i-1]  = a_list[0]
        #
        permutation_    =   permute(_)
        for permutation in  permutation_:
            permutation.insert(0, a_list[i])
            result.append(permutation)
    return result
#
permutations_of_string_ = permute(string_)

# Inputs: END #################################################################

def find():
    return {
            represent(permutation) for permutation in permutations_of_string_  
                if test(permutation, "ACTG")
        }
#

def represent(a_list):
    """
        Turns a list ['A', 'B', 'C', ...] of even length into a string
            "A B ...#...' with '#' at the center.
    """
    lc  = 0             # We'll count the elements 'A', 'B', 'C',  ...
    ls  = 0             # We'll count the spaces between the elements.
    s   = ""            # We'll concatenate 'A', 'B', 'C', ... .
    for e in a_list:
        s   += e
        lc  += len(e)
        ls  += 1
        #
        if lc  == half_length:
            s += "#"
        elif lc < full_length:
            s += " "
    return s
#

def test(permutation, match):
    ls = 0
    #
    for element in permutation:
        ls     += len(element)
        #
        if ls  == half_length:
            s = "".join(permutation)
            #
            for i in range(half_length):
                if not is_a_match(
                        s[i], 
                        s[i + half_length   ], 
                        match):
                    return False
            return True
    return False 


# match = "ACTG"
def is_a_match(s, t, match):
    for i in range(len(match) - 2):
        if  s == match[ i   ] and t == match[ i + 2] or \
            s == match[-i -1] and t == match[-i - 3]:
            return True
    return False
#

print(find())