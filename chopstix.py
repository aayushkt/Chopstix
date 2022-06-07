class Graph:
    parents = []
    children = []
    vertexCount = 0
    numOfFingers = 0
    handSet = []

    def __init__(self, numOfFingers):
        self.numOfFingers = numOfFingers
        self.handSet = generateHandSet(numOfFingers)
        self.vertexCount = len(self.handSet) * len(self.handSet) * 2
        self.vertexCount = self.vertexCount
        for nodeIndex in range(0, self.vertexCount):
            self.parents.append([])
            self.children.append([])
        self.populateGraph()

    def getSolutionsForUnreachableStates(self):
        # returns a vector of length vertexCount where the nth
        # element is 0.5 iff the nth nodeIndex results
        # in a loop that is impossible to exit (the game
        # can never end). 
        endIsReachable = [0] * self.vertexCount
        checkIfParentsAreReachable = []
        for nodeIndex in range(0, self.vertexCount):
            temp = gameOverStatus(nodeIndexToState(nodeIndex, self.handSet))
            if temp == 0 or temp == 1:
                checkIfParentsAreReachable.append(nodeIndex)
                endIsReachable[nodeIndex] = 0.5
        while(len(checkIfParentsAreReachable)):
            currNode = checkIfParentsAreReachable.pop()
            endIsReachable[currNode] = 0.5
            for parent in self.parents[currNode]:
                if not endIsReachable[parent]:
                    checkIfParentsAreReachable.append(parent)

    def updateGraph(self, childIndexes, parentIndex):
        for childIndex in childIndexes:
            self.parents[childIndex].append(parentIndex)
            self.children[parentIndex].append(childIndexes)

    def printGraph(self):
        for node in range(0, self.vertexCount):
            nodeState = nodeIndexToState(node, self.handSet)
            if len(self.children[node]) == 0:
                print(f"{nodeState}: has no children;")
            else:
                childStateList = []
                for childIndex in self.children[node]:
                    childStateList.append(nodeIndexToState(childIndex, self.handSet))
                print(f"{nodeState}: {childStateList};")

    def printAllParents(self):
        for node in range(0, self.vertexCount):
            if len(self.parents[node]) == 0:
                print(f"{node}: has no parents;")
            else:
                print(f"{node}: {self.parents[node]};")

    def populateGraph(self):
        for node in range(0, self.vertexCount):
            childrenStates = getChildrenOfNode(nodeIndexToState(node, self.handSet), self.numOfFingers, self.handSet)
            for state in childrenStates:
                childIndex = stateToNodeIndex(state, self.handSet)
                self.parents[childIndex].append(node)
                self.children[node].append(childIndex)

    def initializeReachable(self, checkIfParentsAreReachable):
        while(len(checkIfParentsAreReachable) > 0):
            node = checkIfParentsAreReachable.pop()
            for parent in self.parents[node]:
                if not self.endIsReachable[parent]:
                    self.endIsReachable[parent] = 1
                    checkIfParentsAreReachable.append(parent)
        
def gameOverStatus(nodeIndex, handSet):
    state = nodeIndexToState(nodeIndex, handSet)
    if state[0] == (0, 0) and state[1] == (0, 0):
        return 0.5
    elif state[0] == (0, 0):
        return 0
    elif state[1] == (0, 0):
        return 1
    else:
        return -1

# Returns the state notation for the given node index
# i.e. if the numOfFingers per hand is 5, then node 63
# would be the state ((0, 4), (0, 3), 0)
def nodeIndexToState(index, handSet):
    numOfHands = len(handSet)
    playerTurn = int(index >= (numOfHands * numOfHands))
    playerZeroHandIndex = (int(index / numOfHands)) % (numOfHands)
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
def getChildrenOfNode(parentState, numOfFingers, handSet):
    childStates = []
    tapStates = getAllTapStates(parentState, numOfFingers)
    for state in tapStates:
        childStates.append(state)
    switchStates = getAllSwitchStates(parentState, numOfFingers, handSet)
    for state in switchStates:
        childStates.append(state)
    childStates = __removeDuplicates__(childStates)
    return childStates

def getAllSwitchStates(state, numOfFingers, handSet):
    switchStates = []
    if (gameOverStatus(state, handSet) + 1):
        return switchStates
    if state[2] == 0:
        activePlayerState = state[0]
        fingerSum = state[0][0] + state[0][1]
    else:
        activePlayerState = state[1]
        fingerSum = state[1][0] + state[1][1]
    for leftHand in range(0, numOfFingers + 1):
        rightHand = fingerSum - leftHand
        if rightHand >= 0 and rightHand <= numOfFingers and not (leftHand, rightHand) == activePlayerState:
            leftHand = leftHand % numOfFingers
            rightHand = rightHand % numOfFingers
            if leftHand > rightHand:
                temp = leftHand
                leftHand = rightHand
                rightHand = temp
            if state[2] == 0:
                switchStates.append(((leftHand, rightHand), state[1], 1))
            else:
                switchStates.append((state[0], (leftHand, rightHand), 1))
    switchStates = __removeDuplicates__(switchStates)
    return switchStates

def getAllTapStates(state, numOfFingers):
    tapStates = []
    for playerHand in range(0, 2):
        if state[state[2]][playerHand]:
            for oppHand in range(0, 2):
                # Notice 1-state[2] returns the player whose turn it
                # is NOT, aka the opponent
                if state[1 - state[2]][oppHand]:
                    # sum is the amount of fingers that will be on the 
                    # new hand (belonging to the opponent) after it has been tapped
                    sum = (state[state[2]][playerHand] + state[1-state[2]][oppHand]) % numOfFingers
                    if (playerHand + oppHand) == 0:
                        newHands = (sum, state[1 - state[2]][1])
                    elif (playerHand + oppHand) == 2:
                        newHands = ((state[1 - state[2]][0], sum))
                    elif playerHand == 1: # Then we know oppHand == 0,
                        newHands = (sum, state[1-state[2]][1])
                    else: # We know playerHand==0 and oppHand==1
                        newHands = (state[1 - state[2]][0], sum)
                    if newHands[0] > newHands[1]:
                        newHands = (newHands[1], newHands[0])
                    if state[2]:
                        newState = (newHands, state[1], 0)
                    else:
                        newState = (state[0], newHands, 1)
                    tapStates.append(newState)
    tapStates = __removeDuplicates__(tapStates)
    return tapStates

# Helper function for getChildrenOfNode()
# Removes repeated elements from a list
def __removeDuplicates__(listObj):
    temp = []
    for item in listObj:
        if item not in temp:
            temp.append(item)
    return temp

# Iterates through a list of state notations
# and returns the corresponding list of node 
# indexes
def getChildStateIndexes(childStates):
    childIndexes = []
    for state in childStates:
        childIndexes.append(stateToNodeIndex(state))
    return childIndexes

if __name__ == "__main__":
    g = Graph(5)
    print(g.getSolutionsForUnreachableStates)
