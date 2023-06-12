import numpy as np

class ChopstixBot:

    # The graph of game states is stored as two dictionaries, one mapping each
    # each state index to it's parent state indexes, and the other mapping
    # each state index to it's child state indexes
    parents = []
    children = []

    # The total number of states in the graph
    stateCount = 0
    
    # The number of fingers on each hand. Generally set to 5, but can be changed.
    # Note that as this number grows, the size of the graph grows O(n^2)
    numOfFingers = 5
    
    # List of all possible tuples a player could have. If numOfFingers == 5, then handSet will be
    # [(0,0),(0,1),(0,2),(0,3),(0,4),(1,1),(1,2),(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4)]
    handSet = []

    # If switching is allowed, players can 'switch' instead of the normal 'attack' on their turn.
    # To switch, a player can redistribute the total number of fingers on each hand, i.e. going
    # from (2, 3) -> (1, 4) or (1, 3) -> (0, 4).
    switchingAllowed = True

    def __init__(self, numOfFingers=5, switchingAllowed=True):
        self.numOfFingers = numOfFingers
        self.switchingAllowed = switchingAllowed
        self.handSet = self.generateHandSet(numOfFingers)
        self.stateCount = len(self.handSet) * len(self.handSet) * 2
        self.stateCount = self.stateCount
        for _ in range(0, self.stateCount):
            self.parents.append([])
            self.children.append([])
        self.initializeGraphEdges()


    # returns a list of length {stateCount} where the nth
    # element is 0.5 if and only if the nth stateIndex is 
    # indeterminate. All other entries are 0.
    # A state is indeterminate if and only if, for all states that could
    # be reached from that state (directly or indirectly), none result in a player winning
    # (Often occurs if switching is not allowed, and is usually just
    # two players stuck in an infinite loop with no other options)
    def getSolutionsForIndeterminateStates(self):
        # Begin by assuming all states are indeterminate
        indeterminateStates = [0.5] * self.stateCount
        statesToProcess = []
        # For every state, if the game ends in that state, it is not indeterminate
        # So, we store it in statesToProcess[] for processing
        for stateIndex in range(0, self.stateCount):
            temp = self.gameOverStatus(stateIndex)
            if temp == 0 or temp == 1:
                statesToProcess.append(stateIndex)
        # Unprocessed non-indeterminate states are set to 0, and their parents
        # must also be non-indeterminate. Therefore, their parents are stored for 
        # processing (unless they have already been marked non-indeterminate).
        # This process is repeated until there are no states left to be processed.
        while(len(statesToProcess)):
            currState = statesToProcess.pop()
            indeterminateStates[currState] = 0
            for parent in self.parents[currState]:
                if indeterminateStates[parent]:
                    statesToProcess.append(parent)
        return indeterminateStates


    # Returns a list of length {stateCount} where the nth element is:
    # 0 if and only if player 0 can guaranteed win from the nth state, 
    # 1 if and only if player 1 can guaranteed win from the nth state,
    # -1 otherwise
    def getSolutionsForPerfectPlay(self):
        # All states start out as neither a win or loss
        solution = [-1] * self.stateCount
        # States we need to evaluate later will be stored here
        statesToEvaluate = []
        # For each state, if it is a win or loss, store all parents 
        # of that state to be a potential guarantee win or loss, and 
        # set that state to 0 or 1 for win or loss
        for stateIndex in range(0, self.stateCount):
            temp = self.gameOverStatus(stateIndex)
            if temp == 0 or temp == 1:
                for parent in self.parents[stateIndex]:
                    statesToEvaluate.append(parent)
                solution[stateIndex] = temp
        # Now we iterate through the rest of the graph
        while(len(statesToEvaluate)):
            # For each state we need to evaluate,
            currState = statesToEvaluate.pop()
            # If it hasn't been solved yet
            if solution[currState] == -1: 
                # Check to see if the player whose turn it is can secure a win
                # i.e. if any of the children states result in a guarantee win,
                # then the current state is a guaranteed win
                for child in self.children[currState]:
                    if solution[child] == self.stateIndexToState(currState)[2]:
                        solution[currState] = solution[child]
                        for parent in self.parents[currState]:
                            statesToEvaluate.append(parent)
                # Otherwise its a guaranteed loss if all children are a loss
                # i.e. the player has no choice but to play to a losing position
                if solution[currState] == -1:
                    allChildrenLose = True
                    for child in self.children[currState]:
                        allChildrenLose = allChildrenLose and solution[child] == solution[self.children[currState][0]] and solution[child] != -1
                    if allChildrenLose: 
                        solution[currState] = solution[self.children[currState][0]]
                        for parent in self.parents[currState]:
                            statesToEvaluate.append(parent)
        return solution


    # Prints the entire graph structure. Used for debugging
    def printGraph(self):
        for stateIndex in range(0, self.stateCount):
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
        for stateIndex in range(0, self.stateCount):
            if len(self.parents[stateIndex]) == 0:
                print(f"{stateIndex}: has no parents;")
            else:
                print(f"{stateIndex}: {self.parents[stateIndex]};")


    # Gets the children of each state via getChildrenOfState()
    # and then accordingly updates parents[] and children[]
    # In other words, fills out the graph.
    def initializeGraphEdges(self):
        for stateIndex in range(0, self.stateCount):
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
            return 1
        elif state[1] == (0, 0):
            return 0
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
    # i.e. if the numOfFingers per hand is 5, then state 
    # notation ((0, 4), (0, 3), 0) would be state index 63
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
        if self.switchingAllowed:
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

    # Solves a matrix equation to rank every state on how likely it is to win for each player from a given point
    # INPUT: (optional) perfectPlaySolutions vector as generated by self.getSolutionsForPerfectPlay
    #        (optional) indeterminateStates vector as generated by self.getSolutionsForIndeterminateStates
    def solveForStateRankings(self, perfectPlaySolutions = None, indeterminateStates = None):
        # If a perfect play vector is not given, we assume players will simply choose their next move 
        # randomly (without evaluating which moves result in guaranteed wins). However, each end state
        # must still correspond with a value of 1 or 0 (depending on who wins).
        # 
        # This means each state's ranking will simply be the average of it's childrens ranks.
        #  
        # This would correspond to a perfectPlay vector of all -1's, except for the end game states with
        # values of 0 or 1 to determine which player wins in the end. See 
        # self.getSolutionsForPerfectPlay() for more information
        if perfectPlaySolutions == None:
            perfectPlaySolutions = [-1] * self.stateCount
            for stateIndex in range(self.stateCount):
                temp = self.gameOverStatus(stateIndex)
                if(temp == 0 or temp == 1):
                    perfectPlaySolutions[stateIndex] = temp

        # If an indeterminate state vector is not given, we assume that all game states can eventually
        # reach an end in the game, except the two states where both players have no fingers available.
        # this corresponds to an indeterminate state vector of [0.5, 0, 0, ..., 0, 0.5, 0, ..., 0, 0]
        # See self.getIndeterminateStates() for more information
        if indeterminateStates == None:
            indeterminateStates = [0] * self.stateCount
            indeterminateStates[self.stateToStateIndex(((0, 0), (0, 0), 0))] = 0.5
            indeterminateStates[self.stateToStateIndex(((0, 0), (0, 0), 1))] = 0.5
        mat = np.zeros((self.stateCount, self.stateCount))
        solution = np.zeros(self.stateCount)
        # assign the rest of the states a value here:
        for stateIndex in range(0, self.stateCount):
            if indeterminateStates[stateIndex]:
                mat[stateIndex][stateIndex] = 1
                solution[stateIndex] = indeterminateStates[stateIndex]
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

    def printStateOptions(self, state, ranks):
        print(f"{state} : {ranks[self.stateToStateIndex(state)]}")
        if(not len(self.children[self.stateToStateIndex(state)])):
            print("GAME OVER, no moves can be made")
        else:
            print("Options are:")
            for child in self.children[self.stateToStateIndex(state)]:
                print(f"\t{self.stateIndexToState(child)} : {ranks[child]}")
        print("\n")

    # Prints all the rankings of every state that
    # isn't a guaranteed win/loss for a player
    # and doesn't end in a draw
    # i.e. states with rank != 1.0 and 
    # states with rank != 0 and
    # states with indeterminateStates of 0.0
    # i.e. all states with a decimal rank != 0.5
    # due to being indeterminate
    def fairestStates(self, ranks, indeterminateStates):
        fairestNode = None
        for stateIndex in range(self.stateCount):
            if not(indeterminateStates[stateIndex] or ranks[stateIndex] == 1 or ranks[stateIndex] == 0):
                print(f"{self.stateIndexToState(stateIndex)} : {ranks[stateIndex]}")
                if(fairestNode == None or abs(ranks[fairestNode]-0.5) > abs(ranks[stateIndex]-0.5)):
                    fairestNode = stateIndex
        print(f"The fairest state is: {CXBot.stateIndexToState(fairestNode)}: {ranks[fairestNode]}")
    
    def playAgainstSelf(self, startState, ranks):
        currState = startState
        visitedStates = []
        visitedStates.append(currState)
        while(not (self.gameOverStatus(currState) == 0 or self.gameOverStatus(currState) == 1)):
            debugFlag = True
            if(debugFlag):
                self.printStateOptions(self.stateIndexToState(currState), ranks)
            else:
                print(f"{self.stateIndexToState(currState)} : {ranks[currState]}")
            currState = self.chooseBestMove(ranks, currState)
            if currState in visitedStates:
                print(f"{self.stateIndexToState(currState)} : {ranks[currState]}")
                print("We've been here before - we're going in circles!")
                return
            else:
                visitedStates.append(currState)
        print(f"{self.stateIndexToState(currState)} : {ranks[currState]}")
        print(f"GAME OVER - PLAYER {self.stateIndexToState(currState)[2] - 1} WINS!")

    def playAgainstPlayer(self, startStateIndex, ranks):
        currStateIndex = startStateIndex
        done = False
        while(not done):
            if(self.gameOverStatus(currStateIndex) == 0 or self.gameOverStatus(currStateIndex) == 1):
                print(f"GAME OVER - PLAYER {self.stateIndexToState(currStateIndex)[2] - 1} WINS!")
                done = True
            else:
                for i in range(100):
                    print()
                print(f"The current state is {self.stateIndexToState(currStateIndex)}")
                if(self.stateIndexToState(currStateIndex)[2]):
                    for i in range(len(self.children[currStateIndex])):
                        print(f"{i}: {self.stateIndexToState(self.children[currStateIndex][i])}")
                    selected = input("Which state do you choose? Type \"exit\" to exit.\n")
                    if(selected == "exit" or selected == "e"):
                        done = True
                    else:
                        selected = int(selected)
                        currStateIndex = self.children[currStateIndex][selected]
                else:
                    currStateIndex = self.chooseBestMove(ranks, currStateIndex)


if __name__ == "__main__":
    CXBot = ChopstixBot(5, True)
    perfectPlay = CXBot.getSolutionsForPerfectPlay()
    indeterminateStates = CXBot.getSolutionsForIndeterminateStates()
    ranks = CXBot.solveForStateRankings(perfectPlay, indeterminateStates)
    
    # for i in range(0, CXBot.stateCount):
    #     print(str(CXBot.stateIndexToState(i)) + " -> " + str(i))
    #CXBot.fairestStates(ranks, indeterminateStates)
    #print(ranks)
    startState = ((1, 1), (1, 2), 1)
    startStateIndex = CXBot.stateToStateIndex(startState)
    print(indeterminateStates)
    #CXBot.playAgainstPlayer(startStateIndex, ranks)
    #CXBot.playAgainstSelf(startStateIndex, ranks)
    #print(CXBot.getAllSwitchStates(startState))