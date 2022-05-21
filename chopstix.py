import igraph

def nodeIndexToState(index, handSet):
    numOfHands = len(handSet)
    playerTurn = int(index >= numOfHands * numOfHands)
    playerZeroHandIndex = (int(index / 15)) % (15)
    playerOneHandIndex = index % numOfHands
    return (handSet[playerZeroHandIndex], handSet[playerOneHandIndex], playerTurn)

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
    childStates =  removeDuplicates(childStates)
    return childStates

def removeDuplicates(listObj):
    temp = []
    for item in listObj:
        if item not in temp:
            temp.append(item)
    return temp

def isGameOver(state):
    if state[0][0] or state[0][1]:
        return False
    if state[1][0] or state[1][1]:
        return False
    return True

numOfFingers = 5
handSet = generateHandSet(numOfFingers)
numOfNodes = len(handSet) * len(handSet) * 2
state = ((4, 4), (3, 4), 1)
print(getChildrenOfNode(state, numOfFingers))

# cs = igraph.Graph()