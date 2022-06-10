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
    # assign the rest of the states a value here:
    for node in range(0, graph.vertexCount):
        # if the node has no children
        # i.e. it is a final game-ending state,
        # then we set its value equal to the player
        # who wins (i.e. 0 means player zero wins)
        if len(graph.children[node]) == 0:
            mat[node][node] = 1
            sanityCheck = graph.gameOverStatus(node)
            if sanityCheck == 1 or sanityCheck == 0 or sanityCheck == 0.5:
                solution[node] = graph.gameOverStatus(node)
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

def evaluateMatrix(ranks):
    bestDiff = 2
    fairestNode = -1
    sum = 0
    numOfOnes = 0
    numOfZeros = 0
    for node in range(1, len(ranks)):
        if(ranks[node] == 1): numOfOnes += 1
        if(ranks[node] == 0): numOfZeros += 1
        diff = abs(ranks[node] - 0.5)
        if diff < bestDiff:
            bestDiff = diff
            fairestNode = node
        sum += ranks[node]
    avg = sum/(len(ranks) - 1)
    print(f"Num of Ones is {numOfOnes}")
    print(f"Num of Zeros is {numOfZeros}")
    print(f"Fairest node is {fairestNode}")
    print(f"Average (should be 0.5) is {avg}")
    print(f"Chance is {bestDiff}")

g = cx.Graph(3)
(M, b) = makeMatrix(g)
ans = np.linalg.solve(M, b)
evaluateMatrix(ans)
