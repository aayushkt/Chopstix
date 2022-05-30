# Testing python script to see if chopstix.py works as expected
import numpy as np
import chopstix as cx

# Generates a matrix equation to solve 
# by setting each node value to the 
# average of its children and solving 
# Returns the rank of each state in an array
def graphSolver(graph):
    arr = np.zeros((graph.vertexCount, graph.vertexCount))
    solution = np.zeros(graph.vertexCount)
    # State 0 has no children, we set it's 
    # value to 0.5 by hand
    arr[0][0] = 1
    solution[0] = 0.5
    # assign the rest of the states a value here:
    for node in range(1, graph.vertexCount):
        # if the node has no children
        # i.e. it is a final game-ending state,
        # then we set its value equal to the player
        # who wins (i.e. 0 means player zero wins)
        if len(graph.children[node]) == 0:
            arr[node][node] = 1
            sanityCheck = graph.playerWhoWins(node)
            if sanityCheck == 1 or sanityCheck == 0:
                solution[node] = graph.playerWhoWins(node)
            else:
                print(f"ERROR WITH CHILDREN OF NODE {node}")
                exit()
        # Otherwise we fill out the matrix array to
        # store the node as an average of its children
        else:
            arr[node][node] = len(graph.children[node])
            for child in graph.children[node]:
                arr[node][child] = -1
    rankings = np.linalg.solve(arr, solution)
    return rankings
    
g = cx.Graph(7)

ranks = graphSolver(g)

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