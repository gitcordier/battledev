###############################################################################
# Solution to Pizzarama problem (battledev (FR) 11/2017)                      #
#     https://questionsacm.isograd.com/codecontest/pdf/spacepizza.pdf         #
# Name:     spacepizza.py .                                                   #
# Indent:   = 4 spaces (no tab).                                              #
# Width:    79 (comment lines < 73).                                          #
# license:  Nope; consider the below code as public domain.                   #
###############################################################################
###############################################################################
# We are given N (N > 4) points {a, b, c, ...} of the physical space.
# Each of them is so equipped with cartesian coordinates (x, y, z). 
# From now on, we assume that two distinct points have different y's.
#   NB (*):
#   Our points are then ordered with respect to the following total and 
#   strict order R:
#       R: pRp' if and only if that y(p) < y(p') (given any p, p')
#   
# We aim at visiting all these points the following way:
#
# A.  Outward ("as y increases"):
#   i.  We start from p_min, the point with the least y'.
#
#   ii. If we are at p, we can reach any p' such that y(p') > y(p).
#       But points p" with smaller y (y(p") <  y(p)) are out of reach.
#
#   iii.We so reach p_max, the point with the greated y.
#
# B. Return back ("as y decreases"):
#   i.  We start from p_max.
#  
#   ii. If we are at p, we can reach any p" such that y(p") < y(p).
#       But points p' with greater y (y(p') >  y(p)) are out of reach.
#       Moreover,  
#           (a) We MUST visit any p' that was not visited outward
#               (so that all points get visited, eventually);
#           (c) No point can be visited twice.
# 
#   vi. Finally, we come back to p_min. So ends the journey :)
# 
# It seems there are many possible trips, then (actually, yes: There are
# exactly 2^(N-2) possible trips)!
# 
# So arises the question: What is the shortest one?
#
# This is what we aim at computing now. 
#
# To do so, we first sort the points by increasing y, so that the y of 
# node #j is smaller than the y of node #i (j < i).
# 
# Next, we split the set of all possible paths into subsets S(i): 
#
#   S(i) := {    
#               All trips during which the point #i is visited 
#               just before we 'jump' to the 'highest point, i.e. 
#               the point #(N-1). 
#       } 
#   (i = 0, 1, 2, ..., N-2)
#
# Given i, there so exits a minimal distance for the whole trip, namely 
#
#   min_i_total := min{lengths of trips in S(i)} 
#
# The wished minimal length is then 
#
#   min_i_total := min{min_i_total: i = 0, 1, 2, ..., N-1} .
#
# From now on, d(j,i) denotes the distance between the nodes #i,#j, 
# as i < j. 
#
# In the below figure, each point is identified with its index
# 
#       (outward)   (return) 
#           0         0               |
#           |         |               | y increases
#           |         |              \ /
#           |         |
#           |         |
#          |j|_   <---|-------| What happens here has a minimal length
#           |  \_     |            min_j. Does NOT depend on min_i.
#           |    \_   |
#           |      \__|
#           |        j+1
#           |         |
#           |        i-1
#           |         |
#          |i|_  <----|-------| What happens here has a minimal length
#           |  \_     |            min_i
#           |    \_   |
#           |      \__|_
#           |       |i+1|
#           |        ...
#           |        N-2  <--| In the below part, distances are fixed,
#           N-1      N-1           provided i
#
# NB:
#   For symmetry reasons, we can assume that point #N-2 is part of the 
#   return, then discard the case i = N-2.
#
# Assume that we know min_0, ..., min_j (j < i), provided i: We can 
# compute m_i then straightforwardly obtain min_i_total.
# Since m_0 = d(0, 1), it follows from the induction principle that 
# all m_i_total's are computable.
#
# The below function compute_min implements the such routines and so
# returns the desired result.
#
# It can be proved that the whole cost (in time) is O(N^2) in the worst
# case.
# 
########################################################################
import sys
from operator import itemgetter
from math import sqrt


# Get the list-shaped input: First line for N, any other one for a point 
# coordinates.
lines = []

for line in sys.stdin:
    lines.append(line.rstrip('\n'))

N = int(lines[0])

# From lines, get a "y-sorted" list of the points, aka 'node_', 
# so that the y of node #j is smaller than the y of node #i (j < i).


nodes_unsorted_as_strings   = lines[1: ]
nodes_unsorted              = []

for line in nodes_unsorted_as_strings:
    s = line.split(" ")
    v = []
    for x in s:
        v.append(float(x))
    nodes_unsorted.append(v)

node_ = sorted(nodes_unsorted, key=itemgetter(1))

# Euclidian norm. 
#   NB: Could be ANY cost function c. In other words, we can drop the
#       assumption that our ambient space is the usual euclidian one.
#       We only need a finite amount of points that are:
#       i.  well sorted in an arbitrary fashion (cf. (*), above)
#       ii. nodes of an edge-weighted graph.
def get_distance_between(a, b):
    """
        input: Two vectors a(x, y, z), b(x', y', z')
        output: the euclidian norm |a-b|
    """
    X = (b[0] - a[0])**2
    Y = (b[1] - a[1])**2
    Z = (b[2] - a[2])**2
    return sqrt(X + Y + Z)

# Given two points (p,p'), we enlist the distance between p and p.
distance = []
for i in range(N):
    distance.append([])
    for j in range(i):
        distance[i].append(get_distance_between(node_[j], node_[i]))
    #
#

def d(j, i):
    """
        Since points are indexed, we find more customary to deal with 
        d(j, i) instead of d(node(i), d(node(j))).
    """
    if i == j :
        return 0
    else:
        return distance[i][j]

# Outward (A)

# Last jump is the distance of the (last) segment [p, p_max].
last_jump_from = [float("inf")]*(N-1)
for i in range(N-2):
    last_jump_from[i] = d(i, N-1)
#

# Return (B)

# s(N-1)    = 0 
# s(k)      = s(N-1) + ... + s(k+1) + d(k+1, k)
s = [0]*N
for i in range(1, N):
    k = N-1-i
    s[k] = s[k+1] + d(k, k+1)
#

# delta(j, i) := s(j+1) - s(i-1)
def delta(j, i):
    if j >= 0 and j+1 < i-1:
        return s[j+1] - s[i-1]
    return 0

# Given a triangle {p(i-1), p(i), p(i+1)}, 
#
#            i-1
#           / |
#          i  |     lenght(i) = d(i-1, i+1)
#           \ |
#             i
#
def length(i):
    """ Input:i
        Output: d(i-1, i+1)
    """
    return distance[i+1][i-1]

def compute_min():
    """
        Puts everything together and so compute the desired min.
    """
    min_        = [float("inf")] * (N-2)
    
# i = 0
    min_[0]     = d(0, 1)
    min_0_total = last_jump_from[0] + s[1] + min_[0]

# i = 1
    min_[1]     = min_[0] + length(1)
    min_1_total = last_jump_from[1] + s[2] + min_[1]

# So, up to now,
    min_total   = min(min_0_total, min_1_total)
    
# i = 2, 3, ..., N-3 (N > 4)
    for i in range(2, N-2): 
        
        min_i_total = float("inf")
        min_i       = float("inf")
        
        for j in range(i):
            min_i_j = float("inf")
            
            if i-j != 1:
                min_i_j =               \
                        d(j, i)     +   \
                        delta(j, i) +   \
                        length(i)   +   \
                        min_[j]
            #
            else: # That was the tricky part.
                for  k in range(j):
                    min_i_j_k =             \
                        min_[k]         +   \
                        s[k+1] - s[i]   +   \
                        d(k, i+1)
                    min_i_j = min(min_i_j, min_i_j_k)
                #
            min_i   = min(min_i, min_i_j)
        #
        min_[i]     = min_i
        min_i_total = last_jump_from[i] + s[i+1] + min_[i]
        min_total   = min(min_total, min_i_total)
    return min_total
#
 
print(int(compute_min()))

# END

