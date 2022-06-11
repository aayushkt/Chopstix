class Graph:
    parents = []
    children = []
    vertexCount = 0
    numOfFingers = 0
    handSet = []

    def __init__(self, numOfFingers):
        self.numOfFingers = numOfFingers
        self.handSet = self.generateHandSet(numOfFingers)
        self.vertexCount = len(self.handSet) * len(self.handSet) * 2
        self.vertexCount = self.vertexCount
        for _ in range(0, self.vertexCount):
            self.parents.append([])
            self.children.append([])
        self.initializeGraphEdges()

    # returns a vector of length vertexCount where the nth
    # element is 0.5 iff the nth nodeIndex results
    # in a loop that is impossible to exit (the game
    # can never end). All other entries are 0
    def getSolutionsForUnreachableStates(self):
        endIsReachable = [0.5] * self.vertexCount
        checkIfParentsAreReachable = []
        for nodeIndex in range(0, self.vertexCount):
            temp = self.gameOverStatus(nodeIndex)
            if temp == 0 or temp == 1:
                checkIfParentsAreReachable.append(nodeIndex)
                endIsReachable[nodeIndex] = 0
        while(len(checkIfParentsAreReachable)):
            currNode = checkIfParentsAreReachable.pop()
            endIsReachable[currNode] = 0
            for parent in self.parents[currNode]:
                if endIsReachable[parent]:
                    checkIfParentsAreReachable.append(parent)
        return endIsReachable

    # Returns a vector of length vertexCount where the nth
    # element is: a 0 iff player 0 can guaranteed win from the
    # nth node, a 1 iff player 1 can guaranteed win from the nth
    # node, -1 otherwise
    def getSolutionsForPerfectPlay(self):
        solution = [-1] * self.vertexCount
        nodesToEvaluate = []
        for nodeIndex in range(0, self.vertexCount):
            temp = self.gameOverStatus(nodeIndex)
            if temp == 0 or temp == 1:
                for parent in self.parents[nodeIndex]:
                    nodesToEvaluate.append(parent)
                solution[nodeIndex] = temp
        while(len(nodesToEvaluate)):
            currNode = nodesToEvaluate.pop()
            if solution[currNode] != -1: continue
            for child in self.children[currNode]:
                if solution[child] == self.nodeIndexToState(currNode)[2]:
                    solution[currNode] = solution[child]
                    for parent in self.parents[currNode]:
                        nodesToEvaluate.append(parent)
                        break
            allChildrenMatch = True
            for child in self.children[currNode]:
                allChildrenMatch = (solution[child] == solution[self.children[currNode][0]] and solution[child] != -1)
            if allChildrenMatch: 
                solution[currNode] = solution[self.children[currNode][0]]
                for parent in self.parents[currNode]:
                    nodesToEvaluate.append(parent)
        return solution

    # Prints the entire graph structure. Used for debugging
    def printGraph(self):
        for node in range(0, self.vertexCount):
            nodeState = self.nodeIndexToState(node)
            if len(self.children[node]) == 0:
                print(f"{nodeState}: has no children;")
            else:
                childStateList = []
                for childIndex in self.children[node]:
                    childStateList.append(self.nodeIndexToState(childIndex))
                print(f"{nodeState}: {childStateList};")

    # Prints the parents of every node in the graph.
    # Used for debugging
    def printAllParents(self):
        for node in range(0, self.vertexCount):
            if len(self.parents[node]) == 0:
                print(f"{node}: has no parents;")
            else:
                print(f"{node}: {self.parents[node]};")

    # Gets the children of each node via getChildrenOfNode()
    # and then accordingly updates parents[] and children[]
    def initializeGraphEdges(self):
        for node in range(0, self.vertexCount):
            childrenStates = self.getChildrenOfNode(self.nodeIndexToState(node))
            for state in childrenStates:
                childIndex = self.stateToNodeIndex(state)
                self.parents[childIndex].append(node)
                self.children[node].append(childIndex)
    
    # Returns whether the game is over, and if it is, who won
    def gameOverStatus(self, nodeIndex):
        state = self.nodeIndexToState(nodeIndex)
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
    def nodeIndexToState(self, index):
        numOfHands = len(self.handSet)
        playerTurn = int(index >= (numOfHands * numOfHands))
        playerZeroHandIndex = (int(index / numOfHands)) % (numOfHands)
        playerOneHandIndex = index % numOfHands
        return (self.handSet[playerZeroHandIndex], self.handSet[playerOneHandIndex], playerTurn)

    # Returns the node index for the given state notation
    # i.e. if the numOfFingers per hand is 5, then the 
    # state ((0, 4), (0, 3), 0) would be node index 63
    def stateToNodeIndex(self, state):
        output = 0
        output += self.handSet.index(state[0]) * len(self.handSet)
        output += self.handSet.index(state[1])
        output += state[2] * len(self.handSet) * len(self.handSet)
        return output

    # Given a set number of fingers on each hand
    # (this number is generally 5), generates
    # all the possible hands a player could have
    # INPUT: an integer
    # OUTPUT: a list of pairs in increasing order
    # i.e. 3 -> [(0,0), (0,1), (0,2), (1,1), (1,2), (2, 2)]
    def generateHandSet(self, numOfFingers):
        handSet = []
        for x in range(0, numOfFingers):
            for y in range(x, numOfFingers):
                handSet.append((x, y))
        return handSet

    def getChildrenOfNode(self, parentState):
        childStates = []
        tapStates = self.getAllTapStates(parentState)
        for state in tapStates:
            childStates.append(state)
        switchStates = self.getAllSwitchStates(parentState)
        for state in switchStates:
            childStates.append(state)
        childStates = self.__removeDuplicates__(childStates)
        return childStates

    def getAllSwitchStates(self, state):
        switchStates = []
        if (self.gameOverStatus(self.stateToNodeIndex(state)) + 1):
            return switchStates
        if state[2] == 0:
            activePlayerState = state[0]
            fingerSum = state[0][0] + state[0][1]
        else:
            activePlayerState = state[1]
            fingerSum = state[1][0] + state[1][1]
        for leftHand in range(0, self.numOfFingers + 1):
            rightHand = fingerSum - leftHand
            if rightHand >= 0 and rightHand <= self.numOfFingers and not (leftHand, rightHand) == activePlayerState:
                leftHand = leftHand % self.numOfFingers
                rightHand = rightHand % self.numOfFingers
                if leftHand > rightHand:
                    temp = leftHand
                    leftHand = rightHand
                    rightHand = temp
                if state[2] == 0:
                    switchStates.append(((leftHand, rightHand), state[1], 1))
                else:
                    switchStates.append((state[0], (leftHand, rightHand), 0))
        switchStates = self.__removeDuplicates__(switchStates)
        return switchStates

    # Returns all states that can be achieved in one turn from the given state.
    # INPUT: a state in state notation form i.e. ((1, 3), (0, 4), 0)
    # OUTPUT: a list of states in state notation form (can be empty!)
    # i.e. [((1, 3), (0, 0), 1), ((1, 3), (0, 2), 1)]
    def getAllTapStates(self, state):
        tapStates = []
        for playerHand in range(0, 2):
            if state[state[2]][playerHand]:
                for oppHand in range(0, 2):
                    # Notice 1-state[2] returns the player whose turn it
                    # is NOT, aka the opponent
                    if state[1 - state[2]][oppHand]:
                        # sum is the amount of fingers that will be on the 
                        # new hand (belonging to the opponent) after it has been tapped
                        sum = (state[state[2]][playerHand] + state[1-state[2]][oppHand]) % self.numOfFingers
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
        tapStates = self.__removeDuplicates__(tapStates)
        return tapStates

    # Helper function
    # Removes repeated elements from a list
    def __removeDuplicates__(self, listObj):
        temp = []
        for item in listObj:
            if item not in temp:
                temp.append(item)
        return temp

    # Iterates through a list of state notations
    # and returns the corresponding list of node 
    # indexes
    def getAllStateIndexes(self, listOfStates):
        listOfIndexes = []
        for state in listOfStates:
            listOfIndexes.append(self.stateToNodeIndex(state))
        return listOfIndexes

if __name__ == "__main__":
    g = Graph(3)
    ans = g.getSolutionsForPerfectPlay()
    for x in range (0, g.vertexCount):
        print(f"{g.nodeIndexToState(x)} == {ans[x]}")
