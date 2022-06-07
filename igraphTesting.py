# Testing python script to see if chopstix.py works as expected
import numpy as np
import chopstix as cx
from scipy.linalg import null_space

# Generates a matrix equation to solve 
# by setting each node value to the 
# average of its children
def makeMatrix(graph):
    mat = np.zeros((graph.vertexCount, graph.vertexCount))
    solution = np.zeros(graph.vertexCount)
    # State 0 has no children, we set it's 
    # value to 0.5 by hand
    mat[0][0] = 1
    solution[0] = 0.5
    # assign the rest of the states a value here:
    for node in range(1, graph.vertexCount):
        # if the node has no children
        # i.e. it is a final game-ending state,
        # then we set its value equal to the player
        # who wins (i.e. 0 means player zero wins)
        if len(graph.children[node]) == 0:
            mat[node][node] = 1
            sanityCheck = graph.playerWhoWins(node)
            if sanityCheck == 1 or sanityCheck == 0 or sanityCheck == 0.5:
                solution[node] = graph.playerWhoWins(node)
            else:
                print(f"ERROR WITH CHILDREN OF NODE {node}")
                exit()
        # Otherwise we fill out the matrix array to
        # store the node as an average of its children
        else:
            mat[node][node] = len(graph.children[node])
            for child in graph.children[node]:
                mat[node][child] = -1
    return (mat, solution)

# Matrix is non invertible for numOfFingers = 5, 8, 10, 11, 12
def evaluateMatrix(ranks):
    bestDiff = 2
    fairestNode = -1
    sum = 0
    for node in range(1, len(ranks)):
        diff = abs(ranks[node] - 0.5)
        if diff < bestDiff:
            bestDiff = diff
            fairestNode = node
        sum += ranks[node]
    avg = sum/(len(ranks) - 1)

    print(f"Fairest node is {fairestNode}")
    print(f"Average (should be 0.5) is {avg}")
    print(f"Chance is {bestDiff}")

# g = cx.Graph(5)
# (M, b) = makeMatrix(g)
# ans = np.linalg.solve(M, b)
# print(g.endIsReachable)

test = -1
if test: print("HI")