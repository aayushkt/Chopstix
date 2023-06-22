import numpy as np

class ChopstixBot:
    # These two store a list of parent and children states
    # for each state respectively. i.e. children[17] is 
    # a list of all the states that are direct children 
    # of the state with index 17.
    #
    # These get initialized during initializeGraphEdges()
    parents = None
    children = None

    # This is a list representing the type of state each 
    # state is. See classifyStates() for more info.
    #
    # This field is initialized during classifyStates()
    classifiedStates = None

    # This is a list which contains the final 'rank' (how
    # good or bad a state is) for every state.
    #
    # This field is initialized during computeRanks()
    ranks = None

    # This field is a number representing how many
    # states there are in the game.
    stateCount = None

    # This field represents the total number of fingers
    # players have on each hand. Default value is 5.
    numOfFingers = None

    # This is a list of possible sets of hands a player may
    # have during the game. See generateHandSet() for more info.
    #
    # This field is initialized during generateHandSet()
    handSet = []

    # This field represents whether players are allowed to
    # 'switch' or rearrange fingers between hands on their turn
    #
    # Default value is True.
    switchingAllowed = True

    # This field represents whether players are allowed to 
    # 'switch' or rearrange their fingers into the same configuration
    # on their turn, effectively skipping it. This variable is ignored
    # if switchingAllowed is set to False.
    #
    # Default value is False
    skippingAllowed = False

    def __init__(self, numOfFingers=5, switchingAllowed=True, skippingAllowed=False):
        """Executes the chopstix algorithm in four distinct steps:
        1) All appropriate variables are initialized and states are assigned indexes
        2) The graph is generated, states are connected to each other according to settings
        3) States are classified into specific types for computation
        4) Using the classifications, the rank for each state is computed"""
        # Fields are initialized, algorithm is ready to be run
        self.numOfFingers = numOfFingers
        self.switchingAllowed = switchingAllowed
        self.handSet = self.generateHandSet(numOfFingers)
        self.stateCount = len(self.handSet) * len(self.handSet)
        self.skippingAllowed = skippingAllowed
        self.parents = []
        self.children = []
        for _ in range(0, self.stateCount):
            self.parents.append([])
            self.children.append([])
        
        # Now all the states will be connected up to one another
        # representing which states lead to which other states
        # in the graph. This is done by filling out the self.parents[]
        # and self.children[] fields.
        self.initializeGraphEdges()

        # Now that the graph states have all been connected together
        # properly, we can classify which states are of what type.
        # The results are stored in the field self.classifiedStates
        self.classifyStates()

        # Now we compute the ranks of each state, using the classifications
        # stored in self.classifiedStates. The result of this is stored in 
        # the field self.ranks
        self.computeRanks()

    def generateHandSet(self):
        """Returns a ordered list of every possible set of hands a player may have, starting with (0, 0) and ending with (numFingers - 1, numFingers - 1)"""
        handSet = []
        for x in range(0, self.numOfFingers):
            for y in range(x, self.numOfFingers):
                handSet.append((x, y))
        return handSet
    
    # Given a state in ((a, b), (c, d)) notation,
    # returns the index number of that state
    def stateToIndex(self, state):
        """Given a state in ((a, b), (c, d)) notation, returns the index number of that state"""
        n = self.numOfFingers
        a = state[0][0]
        b = state[0][1]
        c = state[1][0]
        d = state[1][1]
        # This monster formula's derivation will be documented in readme
        return int((a*n-((a*(a-1))/2)+b-a)*((n*(n+1))/2)+(c*n-(c*(c-1))/2+d-c))
    
    def indexToState(self, index):
        """Given a state's index number, returns the state in ((a, b), (c, d)) notation"""
        # This monster formula's derivation will be documeted in readme
        return (self.handSet[int(np.floor(index / len(self.handSet)))], self.handSet[index % len(self.handSet)])
    
    def initializeGraphEdges(self):
        """Initializes the graph structures by filling out the children[] and parent[] fields for each state"""
        for stateIndex in range(0, self.stateCount):
            childrenStates = self.getChildrenOfState(self.indexToState(stateIndex))
            for state in childrenStates:
                childIndex = self.stateToIndex(state)
                self.parents[childIndex].append(stateIndex)
                self.children[stateIndex].append(childIndex)

    def getChildrenOfState(self, parentState):
        """Returns all the possible states that can be reached in one move from the parentState
        parameter. If the state has no children, returns an empty list.
        
        Parameters:
            parentState - a state in the notation ((a, b), (c, d))
            
        Returns:
            A list of states that are immediate children of {parentState}. May be empty."""
        childStates = []
        attackStates = self.getAllAttackStates(parentState)
        # If there were no attack states, our opponent has 
        # no hands left to attack, so they lost the game.
        # This means there are no children states to go from here
        # as the game is over.
        if len(attackStates) == 0:
            return childStates
        
        # Otherwise, we get all the possible states via attacking
        # and all the possible states via switching, and mark them
        # as children of this state
        for state in attackStates:
            if state not in childStates:
                childStates.append(state)
        if self.switchingAllowed:
            switchStates = self.getAllSwitchStates(parentState)
            for state in switchStates:
                if state not in childStates:
                    childStates.append(state)
        return childStates
    
    def getAllAttackStates(self, state):
        """Returns all the possible states that can be reached in one move from the {state}
        parameter by attacking an opponents hand. If the state has no such children, returns an empty
        list.
        
        Parameters:
            state - a state in the notation ((a, b), (c, d))
            
        Returns:
            A list of states that can be reached from {state} by attacking the opponent. 
            May be empty."""
        attackStates = []
        for playerHand in range(0, 2): # For each hand the player has,
            if state[0][playerHand]: # If it is not zero (they can attack w/ it)
                for oppHand in range(0, 2): # They can attack either of the opponent's hands
                    if state[1][oppHand]: # If the opponent's hand is zero
                        # newValue is the new number on the attacked hand
                        newValue = (state[1][oppHand] + state[0][playerHand]) % self.numOfFingers
                        # We have to make sure the opponents hands stay ordered,
                        # if the new value is greater than the one on the other hand
                        # then the other hand should come first
                        # Note: 1-oppHand is the other hand of the opponent
                        if newValue > state[1][1-oppHand]:
                            attackStates.append(((state[1][1-oppHand], newValue), state[0]))
                        else:
                            attackStates.append(((newValue, state[1][1-oppHand]), state[0]))
        return attackStates

    def getAllSwitchStates(self, state):
        """Returns all the possible states that can be reached in one move from the {state}
        parameter by switching. If the state has no such children, returns an empty list.
        
        Parameters:
            state - a state in the notation ((a, b), (c, d))
            
        Returns:
            A list of states that can be reached from {state} by switching. 
            May be empty."""
        if state[0] == (0, 0):
            return []
        switchStates = []
        sum = state[0][0] + state[0][1]
        for i in range(0, len(self.handSet)):
            if(self.handSet[i][0] + self.handSet[i][1] == sum):
                if(self.skippingAllowed or self.handSet[i] != state[0]):
                    switchStates.append((state[1], self.handSet[i]))
        return switchStates

    def gameOverState(self, index):
        """Returns whether the state with the given index is a game over state, and who won.
        
        Parameters:
            index (int) - The index of the state to check
            
        Returns:
            0.5 - If the state is ((0, 0), (0, 0))
            0   - If the current player has lost
            1   - If the current player has won
            -1  - If neither player has lost
        """
        state = self.indexToState(index)
        if state[0] == (0, 0) and state[1] == (0, 0):
            return 0.5
        elif state[0] == (0, 0):
            return 0
        elif state[1] == (0, 0):
            return 1
        else:
            return -1

    # We have four types of states:
    # End states - the leaves of the graph = 0/1
    # Indeterminate states - states with no path to a leaf = 0.5
    # Guaranteed states - states with guarantee to win = 0/1
    # General states - states with many potential paths = -1
    def classifyStates(self):
        """Classifies each state into one of the four categories below.
        
        1) End States - The leaves of the graph, where a player wins
        2) Indeterminate States - States with no path to a End State
        3) Guaranteed States - States with a guaranteed path to an End State where a player wins
        4) General States - States with many potential paths

        Fills out the classifiedStates field with a list of 0's, 1's, 0.5's and -1's:
        0 means the state with that index is either an end state or guaranteed state where the
        player loses.
        1 means the state with that index is either an end state or guaranteed state wher the
        player wins.
        0.5 means the state is indeterminate.
        -1 means the state is a general state.

        This function does not return anything, instead it stores it's results
        in the classifiedStates field
        """
        statesToClassify = []
        output = [0.5] * self.stateCount
        for i in range(1, self.stateCount):
            if len(self.children[i]) == 0:
                output[i] = self.gameOverState(i)
                for parent in self.parents[i]:
                    statesToClassify.append(parent)

        while len(statesToClassify):
            currState = statesToClassify.pop()
            originalValue = output[currState]
            allChildrenLose = True
            guaranteedWin = False
            for child in self.children[currState]:
                if output[child] != 1:
                    allChildrenLose = False
                if output[child] == 0:
                    guaranteedWin = True
            if guaranteedWin:
                output[currState] = 1
            elif allChildrenLose:
                output[currState] = 0
            else:
                output[currState] = -1
            if originalValue != output[currState]:
                for parent in self.parents[currState]:
                        statesToClassify.append(parent)
        self.classifiedStates = output
                
    def computeRanks(self):
        """Computes the ranks of each state based on their classifications.
        End states and guaranteed states are given the rank 0 or 1 according
        to whether the player loses or wins, respectively. Indeterminate states
        are given the rank 0.5 to represent a draw. The remaining general states'
        ranks are calculated via a matrix, with a rank between 0 and 1, closer to 0
        meaning the state is likely to end up losing, and closer to 1 meaning the 
        state is more likely to end up with the current player winning.
        
        This function does not return anything, instead it stores it's results
        in the ranks field"""
        mat = np.zeros((self.stateCount, self.stateCount))
        solution = np.zeros(self.stateCount)
        # assign the rest of the states a value here:
        for stateIndex in range(0, self.stateCount):
            if self.classifiedStates[stateIndex] != -1:
                mat[stateIndex][stateIndex] = 1
                solution[stateIndex] = self.classifiedStates[stateIndex]
            else:
                mat[stateIndex][stateIndex] = len(self.children[stateIndex])
                solution[stateIndex] = len(self.children[stateIndex])
                for child in self.children[stateIndex]:
                    mat[stateIndex][child] = 1
        self.ranks = np.linalg.solve(mat, solution)

if __name__ == "__main__":
    CXBot = ChopstixBot(5, True)
    
    # print ranks
    # for i in range(0, len(ranks)):
    #     print(f"{i} -> {ranks[i]}")

    # print children
    # for i in range(0, CXBot.stateCount):
    #     print(f"{i} -> {CXBot.children[i]}")
    #     print()

    # print index or state
    # print(f"{CXBot.stateIndexToState(56)}")