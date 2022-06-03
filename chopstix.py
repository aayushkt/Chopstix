import random

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
        for _ in range(0, self.vertexCount):
            self.parents.append([])
            self.children.append([])
        self.populateGraph()

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
            childrenStates = getChildrenOfNode(nodeIndexToState(node, self.handSet), self.numOfFingers)
            for state in childrenStates:
                childIndex = stateToNodeIndex(state, self.handSet)
                self.parents[childIndex].append(node)
                self.children[node].append(childIndex)

    def playerWhoWins(self, nodeIndex):
        state = nodeIndexToState(nodeIndex, self.handSet)
        if state[0] == (0, 0):
            return 1
        elif state[1] == (0, 0):
            return 0
        else:
            return -1

# Returns the state notation for the given node index
# i.e. if the numOfFingers per hand is 5, then node 63
# would be the state ((0, 4), (0, 3), 0)
def nodeIndexToState(index, handSet):
    numOfHands = len(handSet)
    playerTurn = int(index >= numOfHands * numOfHands)
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
def getChildrenOfNode(parentState, numOfFingers):
    childStates = []
    tapStates = getAllTapStates(parentState, numOfFingers)
    for state in tapStates:
        childStates.append(state)
    switchStates = getAllSwitchStates(parentState, numOfFingers)
    for state in switchStates:
        childStates.append(state)
    childStates = __removeDuplicates__(childStates)
    return childStates

def getAllSwitchStates(state, numOfFingers):
    switchStates = []
    if isGameOver(state):
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
    if isGameOver(state):
        return tapStates
    # If it is player zero's turn,
    if state[2] == 0:
        # Check to see if player zero has fingers on their left hand
        if state[0][0]:
            # If player zero (the current player whose turn it is) has 
            # fingers on their left hand, and player one has fingers on
            # their right hand, then player one can have the new hand of
            # LR, determined by player zero hitting their left hand on 
            # player one's right hand.
            if state[1][1]:
                LR = (state[1][0], (state[1][1] + state[0][0]) % numOfFingers)
                # Make sure it is in the proper increasing order notation
                if LR[0] > LR[1]:
                    LR = (LR[1], LR[0])
                tapStates.append((state[0], LR, 1))
            
            if state[1][0]:
                LL = ((state[1][0] + state[0][0]) % numOfFingers, state[1][1])
                if LL[0] > LL[1]:
                    LL = (LL[1], LL[0])
                tapStates.append((state[0], LL, 1))

        if state[0][1]:
            # Similarly, if player zero has fingers on their right hand
            # They can add it to their opponents left or right hand if
            # those hands have fingers on them
            if state[1][1]:
                RR = (state[1][0], (state[1][1] + state[0][1]) % numOfFingers)
                if RR[0] > RR[1]:
                    RR = (RR[1], RR[0])
                tapStates.append((state[0], RR, 1))
            
            if state[1][0]:
                RL = ((state[1][0] + state[0][1]) % numOfFingers, state[1][1])
                if RL[0] > RL[1]:
                    RL = (RL[1], RL[0])
                tapStates.append((state[0], RL, 1))
    else:
        if state[1][0]:
            # Similarly, if it's player one's turn and they have
            # fingers on their left hand, check whether player 
            # zero has fingers on their right and left hands
            if state[0][1]:
                LR = (state[0][0], (state[0][1] + state[1][0]) % numOfFingers)
                if LR[0] > LR[1]:
                    LR = (LR[1], LR[0])
                tapStates.append((LR, state[1], 0))
            
            if state[0][0]:
                LL = ((state[0][0] + state[1][0]) % numOfFingers, state[0][1])
                if LL[0] > LL[1]:
                    LL = (LL[1], LL[0])
                tapStates.append((LL, state[1], 0))

        if state[1][1]:
            # Finally we check if its player one's turn and they have
            # fingers on their right hand, then we check whether player
            # zero has fingers on their left or right hands to add to
            if state[0][1]:
                RR = (state[0][0], (state[0][1] + state[1][1]) % numOfFingers)
                if RR[0] > RR[1]:
                    RR = (RR[1], RR[0])
                tapStates.append((RR, state[1], 0))
            
            if state[0][0]:
                RL = ((state[0][0] + state[1][1]) % numOfFingers, state[0][1])
                if RL[0] > RL[1]:
                    RL = (RL[1], RL[0])
                tapStates.append((RL, state[1], 0))
    # Finally, if a state leads to another state in more than one way
    # (often caused by symmetrical hands etc.), then we can remove
    # the additional unnecessary copies 
    tapStates =  __removeDuplicates__(tapStates)
    return tapStates

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

if __name__ == "__main__":
    state = ((1, 4), (3, 4), 0)
    a = getAllSwitchStates(state, 5)
    print(a)
