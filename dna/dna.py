###############################################################################
# Solution to DNA (in French: ADN) problem (battledev (FR) 11/2017)           #
#     https://www.isograd.com/FR/solutionconcours.php?contest_id=28           #
#     https://questionsacm.isograd.com/codecontest/pdf/DNA.pdf                #
# Name:     dna.py .                                                          #
# Indent:   = 4 spaces (no tab).                                              #
# Width:    79 (comment lines < 73).                                          #
# license:  Nope; consider the below code as public domain.                   #
###############################################################################

import sys 
from itertools import permutations

lines = []
for line in sys.stdin: # Change 'sys.stdin' to 'input' if you work locally.
	lines.append(line.rstrip('\n'))

strings = lines[1: ]
N = int(lines[0])
L = len(''.join(strings))
Q = L // 2
S = 'ACTG'

all_permutations = permutations(strings)

def find():
    return list({represent(p) for p in all_permutations if test(p)})[0]

def represent(a):
    """
        Turns a list (even length) of strings (S, T, U, ...) into a string
            STU… with '#' right in the middle.
    """
    c = 0
    for i in range(N):
        c += len(a[i])
        if c == Q:
            i += 1
            break
    u = ' '.join(a[: i])
    v = ' '.join(a[i: ])
    return '#'.join((u, v))

def test(p):
    ls = 0
    for e in p:
        ls += len(e)
        
        if ls  == Q:
            s = ''.join(p)
            
            for i in range(Q):
                if is_a_match((s[i], s[i+Q])):
                    pass
                else:
                    return False
            return True
        elif ls > Q:
            return False
        else:
            pass
    return True


def is_a_match(t):
    for i in range(len(S) - 2):
        if t == (S[i], S[i+2]) or t == (S[-1-i], S[-3-i]):
            return True
    return False
#

print(find())