# Testing python script to see if chopstix.py works as expected

import chopstix as cx

g = cx.Graph(3)
print(g.handSet)
print(g.vertexCount)

# TODO: add this function to populate the 
# parents[] and children[] of the graph
# with the
# g.populateGraph()

g.printAllParents()
g.printGraph()

