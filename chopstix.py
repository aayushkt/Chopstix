class Graph:
    parents = []
    children = []
    vertexCount = 0
    handSet = []

    def __init__(self, numOfFingers):
        self.handSet = generateHandSet(numOfFingers)
        self.vertexCount = len(self.handSet) * len(self.handSet) * 2
        self.vertexCount = self.vertexCount
        for _ in range(0, self.vertexCount):
            self.parents.append([])
            self.children.append([])

    def updateGraph(self, childIndexes, parentIndex):
        for childIndex in childIndexes:
            self.parents[childIndex].append(parentIndex)
            self.children[parentIndex].append(childIndexes)

    def printGraph(self):
        for node in range(0, self.vertexCount):
            if len(self.children[node]) == 0:
                print(f"{node}: has no children;")
            else:
                print(f"{node}: {self.children[node]};")

    def printAllParents(self):
        for node in range(0, self.vertexCount):
            if len(self.parents[node]) == 0:
                print(f"{node}: has no parents;")
            else:
                print(f"{node}: {self.parents[node]};")

# Returns the state notation for the given node index
# i.e. if the numOfFingers per hand is 5, then node 63
# would be the state ((0, 4), (0, 3), 0)
def nodeIndexToState(index, handSet):
    numOfHands = len(handSet)
    playerTurn = int(index >= numOfHands * numOfHands)
    playerZeroHandIndex = (int(index / 15)) % (15)
    playerOneHandIndex = index % numOfHands
    return (handSet[playerZeroHandIndex], handSet[playerOneHandIndex], playerTurn)

# Returns the node index for the given state notation
# i.e. if the numOfFingers per hand is 5, then the 
# state ((0, 4), (0, 3), 0) would be node index 63
def stateToNodeIndex(state, handSet):
    output = 0
    output += handSet.index(state[0]) * len(handSet)
    output += handSet.index(state[1])
    output += state[2] * len(handSet) * len(handSet)
    return output

# Given a set number of fingers on each hand
# (this number is generally 5), generates
# all the possible hands a player could have
# INPUT: an integer
# OUTPUT: a list of pairs in increasing order
# i.e. 3 -> [(0,0), (0,1), (0,2), (1,1), (1,2), (2, 2)]
def generateHandSet(numOfFingers):
    handSet = []
    for x in range(0, numOfFingers):
        for y in range(x, numOfFingers):
            handSet.append((x, y))
    return handSet

# Returns all states that can be achieved in one turn from the given state.
# INPUT: a state in state notation form i.e. ((1, 3), (0, 4), 0)
# OUTPUT: a list of states in state notation form (can be empty!)
# i.e. [((1, 3), (0, 0), 1), ((1, 3), (0, 2), 1)]
def getChildrenOfNode(parentState, numOfFingers):
    childStates = []
    if isGameOver(parentState):
        return childStates
    # If it is player zero's turn,
    if parentState[2] == 0:
        # Check to see if player zero has fingers on their left hand
        if parentState[0][0]:
            # If player zero (the current player whose turn it is) has 
            # fingers on their left hand, and player one has fingers on
            # their right hand, then player one can have the new hand of
            # LR, determined by player zero hitting their left hand on 
            # player one's right hand.
            if parentState[1][1]:
                LR = (parentState[1][0], (parentState[1][1] + parentState[0][0]) % numOfFingers)
                # Make sure it is in the proper increasing order notation
                if LR[0] > LR[1]:
                    LR = (LR[1], LR[0])
                childStates.append((parentState[0], LR, parentState[2]))
            
            if parentState[1][0]:
                LL = ((parentState[1][0] + parentState[0][0]) % numOfFingers, parentState[1][1])
                if LL[0] > LL[1]:
                    LL = (LL[1], LL[0])
                childStates.append((parentState[0], LL, parentState[2]))

        if parentState[0][1]:
            # Similarly, if player zero has fingers on their right hand
            # They can add it to their opponents left or right hand if
            # those hands have fingers on them
            if parentState[1][1]:
                RR = (parentState[1][0], (parentState[1][1] + parentState[0][1]) % numOfFingers)
                if RR[0] > RR[1]:
                    RR = (RR[1], RR[0])
                childStates.append((parentState[0], LR, parentState[2]))
            
            if parentState[1][0]:
                RL = ((parentState[1][0] + parentState[0][1]) % numOfFingers, parentState[1][1])
                if RL[0] > RL[1]:
                    RL = (RL[1], RL[0])
                childStates.append((parentState[0], LL, parentState[2]))
    else:
        if parentState[1][0]:
            # Similarly, if it's player one's turn and they have
            # fingers on their left hand, check whether player 
            # zero has fingers on their right and left hands
            if parentState[0][1]:
                LR = (parentState[0][0], (parentState[0][1] + parentState[1][0]) % numOfFingers)
                if LR[0] > LR[1]:
                    LR = (LR[1], LR[0])
                childStates.append((LR, parentState[1], parentState[2]))
            
            if parentState[0][0]:
                LL = ((parentState[0][0] + parentState[1][0]) % numOfFingers, parentState[0][1])
                if LL[0] > LL[1]:
                    LL = (LL[1], LL[0])
                childStates.append((LL, parentState[1], parentState[2]))

        if parentState[1][1]:
            # Finally we check if its player one's turn and they have
            # fingers on their right hand, then we check whether player
            # zero has fingers on their left or right hands to add to
            if parentState[0][0]:
                RR = (parentState[0][0], (parentState[0][1] + parentState[1][1]) % numOfFingers)
                if RR[0] > RR[1]:
                    RR = (RR[1], RR[0])
                childStates.append((RR, parentState[1], parentState[2]))
            
            if parentState[1][0]:
                RL = ((parentState[0][0] + parentState[1][1]) % numOfFingers, parentState[0][1])
                if RL[0] > RL[1]:
                    RL = (RL[1], RL[0])
                childStates.append((RL, parentState[1], parentState[2]))
    # Finally, if a state leads to another state in more than one way
    # (often caused by symmetrical hands etc.), then we can remove
    # the additional unnecessary copies 
    childStates =  __removeDuplicates__(childStates)
    return childStates

# Helper function for getChildrenOfNode()
# Removes repeated elements from a list
def __removeDuplicates__(listObj):
    temp = []
    for item in listObj:
        if item not in temp:
            temp.append(item)
    return temp

# Checks to see whether either player has
# Lost the game yet
def isGameOver(state):
    if state[0][0] or state[0][1]:
        return False
    if state[1][0] or state[1][1]:
        return False
    return True

# Iterates through a list of state notations
# and returns the corresponding list of node 
# indexes
def getChildStateIndexes(childStates):
    childIndexes = []
    for state in childStates:
        childIndexes.append(stateToNodeIndex(state))
    return childIndexes
