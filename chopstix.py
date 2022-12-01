import numpy as np
from collections import OrderedDict

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
    # element is 0.5 iff the nth stateIndex results
    # in a loop that is impossible to exit (the game
    # can never end). All other entries are 0
    def getSolutionsForUnreachableStates(self):
        endIsReachable = [0.5] * self.vertexCount
        checkIfParentsAreReachable = []
        for stateIndex in range(0, self.vertexCount):
            temp = self.gameOverStatus(stateIndex)
            if temp == 0 or temp == 1:
                checkIfParentsAreReachable.append(stateIndex)
                endIsReachable[stateIndex] = 0
        while(len(checkIfParentsAreReachable)):
            currState = checkIfParentsAreReachable.pop()
            endIsReachable[currState] = 0
            for parent in self.parents[currState]:
                if endIsReachable[parent]:
                    checkIfParentsAreReachable.append(parent)
        return endIsReachable

    # Returns a vector of length vertexCount where the nth
    # element is: a 0 iff player 0 can guaranteed win from the
    # nth state, a 1 iff player 1 can guaranteed win from the nth
    # state, -1 otherwise
    def getSolutionsForPerfectPlay(self):
        solution = [-1] * self.vertexCount
        statesToEvaluate = []
        for stateIndex in range(0, self.vertexCount):
            temp = self.gameOverStatus(stateIndex)
            if temp == 0 or temp == 1:
                for parent in self.parents[stateIndex]:
                    statesToEvaluate.append(parent)
                solution[stateIndex] = temp
        while(len(statesToEvaluate)):
            currState = statesToEvaluate.pop()
            if solution[currState] != -1: continue
            for child in self.children[currState]:
                if solution[child] == self.stateIndexToState(currState)[2]:
                    solution[currState] = solution[child]
                    for parent in self.parents[currState]:
                        statesToEvaluate.append(parent)
                        break
            allChildrenMatch = True
            for child in self.children[currState]:
                allChildrenMatch = (solution[child] == solution[self.children[currState][0]] and solution[child] != -1)
            if allChildrenMatch: 
                solution[currState] = solution[self.children[currState][0]]
                for parent in self.parents[currState]:
                    statesToEvaluate.append(parent)
        return solution

    # Prints the entire graph structure. Used for debugging
    def printGraph(self):
        for stateIndex in range(0, self.vertexCount):
            state = self.stateIndexToState(stateIndex)
            if len(self.children[stateIndex]) == 0:
                print(f"{state}: has no children;")
            else:
                childStateList = []
                for childIndex in self.children[stateIndex]:
                    childStateList.append(self.stateIndexToState(childIndex))
                print(f"{state}: {childStateList};")

    # Prints the parents of every state in the graph.
    # Used for debugging
    def printAllParents(self):
        for stateIndex in range(0, self.vertexCount):
            if len(self.parents[stateIndex]) == 0:
                print(f"{stateIndex}: has no parents;")
            else:
                print(f"{stateIndex}: {self.parents[stateIndex]};")

    # Gets the children of each state via getChildrenOfState()
    # and then accordingly updates parents[] and children[]
    def initializeGraphEdges(self):
        for stateIndex in range(0, self.vertexCount):
            childrenStates = self.getChildrenOfState(self.stateIndexToState(stateIndex))
            for state in childrenStates:
                childIndex = self.stateToStateIndex(state)
                self.parents[childIndex].append(stateIndex)
                self.children[stateIndex].append(childIndex)
    
    # Returns whether the game is over, and if it is, who won
    def gameOverStatus(self, stateIndex):
        state = self.stateIndexToState(stateIndex)
        if state[0] == (0, 0) and state[1] == (0, 0):
            return 0.5
        elif state[0] == (0, 0):
            return 0
        elif state[1] == (0, 0):
            return 1
        else:
            return -1

    # Returns the state notation for the given state index
    # i.e. if the numOfFingers per hand is 5, then state 63
    # would be the state ((0, 4), (0, 3), 0)
    def stateIndexToState(self, index):
        numOfHands = len(self.handSet)
        playerTurn = int(index >= (numOfHands * numOfHands))
        playerZeroHandIndex = (int(index / numOfHands)) % (numOfHands)
        playerOneHandIndex = index % numOfHands
        return (self.handSet[playerZeroHandIndex], self.handSet[playerOneHandIndex], playerTurn)

    # Returns the state index for the given state notation
    # i.e. if the numOfFingers per hand is 5, then the 
    # state ((0, 4), (0, 3), 0) would be state index 63
    def stateToStateIndex(self, state):
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

    def getChildrenOfState(self, parentState):
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
        if (self.gameOverStatus(self.stateToStateIndex(state)) + 1):
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
    # and returns the corresponding list of state 
    # indexes
    def getAllStateIndexes(self, listOfStates):
        listOfIndexes = []
        for state in listOfStates:
            listOfIndexes.append(self.stateToStateIndex(state))
        return listOfIndexes

    # Solves a matrix equation to rank every 
    # state on how likely it is to win
    # for each player from a given point
    # INPUT: (optional) perfectPlaySolutions vector as generated by self.getSolutionsForPerfectPlay
    #        (optional) unreachableStates vector as generated by self.getSolutionsForUnreachableStates
    def solveForStateRankings(self, perfectPlaySolutions = None, unreachableStates = None):
        # If a perfect play vector is not given, we assume players will simply choose their next move 
        # randomly (without evaluating which moves result in guaranteed wins). However, each end state
        # must still correspond with a value of 1 or 0 (depending on who wins). 
        # This would correspond to a perfectPlay vector of all -1's, except for the end game states with
        # values of 0 or 1 to determine which player wins in the end. See 
        # self.getSolutionsForPerfectPlay for more information
        if perfectPlaySolutions == None:
            perfectPlaySolutions = [-1] * self.vertexCount
        # If an unreachable state vector is not given, we assume that all game states can eventually
        # reach an end in the game, except the two states where both players have no fingers available.
        # this corresponds to an unreachable state vector of [0.5, 0, 0, ..., 0, 0.5, 0, ..., 0, 0]
        # See self.getUnreachableStates for more information
        if unreachableStates == None:
            unreachableStates = [0] * self.vertexCount
            unreachableStates[g.stateToStateIndex(((0, 0), (0, 0), 0))] = 0.5
            unreachableStates[g.stateToStateIndex(((0, 0), (0, 0), 1))] = 0.5
        mat = np.zeros((self.vertexCount, self.vertexCount))
        solution = np.zeros(self.vertexCount)
        # assign the rest of the states a value here:
        for stateIndex in range(0, self.vertexCount):
            if unreachableStates[stateIndex]:
                mat[stateIndex][stateIndex] = 1
                solution[stateIndex] = unreachableStates[stateIndex]
            elif perfectPlaySolutions[stateIndex] != -1:
                mat[stateIndex][stateIndex] = 1
                solution[stateIndex] = perfectPlaySolutions[stateIndex]
            else:
                mat[stateIndex][stateIndex] = len(self.children[stateIndex])
                for child in self.children[stateIndex]:
                    mat[stateIndex][child] = -1
        return np.linalg.solve(mat, solution)

    def chooseBestMove(self, rankings, stateIndex):
        bestDiff = 2
        bestState = 0
        for child in self.children[stateIndex]:
            diff = abs(rankings[child] - self.stateIndexToState(stateIndex)[2])
            if diff < bestDiff:
                bestDiff = diff
                bestState = child
        return bestState

    def fairestStates(self, ranks):
        ranksDict = {}
        for i in range(0, self.vertexCount):
            ranksDict.update({self.stateIndexToState(i) : abs(ranks[i] - 0.5)})
        sortedDict = dict(sorted(ranksDict.items(), key=lambda item: item[1]))
        for item in sortedDict:
            print(f"{item} : {ranks[self.stateToStateIndex(item)]}")

    def playGame(self, startState, ranks):
        currState = startState
        visitedStates = []
        visitedStates.append(currState)
        print(f"{self.stateIndexToState(currState)} : {ranks[currState]}")
        while(not (self.gameOverStatus(currState) == 0 or self.gameOverStatus(currState) == 1)):
            currState = self.chooseBestMove(ranks, currState)
            print(f"{self.stateIndexToState(currState)} : {ranks[currState]}")
            if currState in visitedStates:
                return
            else:
                visitedStates.append(currState)

if __name__ == "__main__":
    g = Graph(5)
    pp = g.getSolutionsForPerfectPlay()
    ur = g.getSolutionsForUnreachableStates()
    ranks = g.solveForStateRankings(perfectPlaySolutions=pp, unreachableStates=ur)
    g.fairestStates(ranks)
    #startState = ((1, 1), (1, 1), 0)
    #startState = g.stateToStateIndex(startState)
    #g.playGame(startState, ranks)
    