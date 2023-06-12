# Chopstix

## Introduction

Chopstix is a project based on the game classic Japanese game "Chopsticks", also known as "Finger Chess", "Swords", "Magic Fingers", and more. Although the rules of the game are quite simple, they can lead to surprisingly complex gameplay.
Chopstix algorithmically maps out the entirety of the game - analyzing every single move that can be made, and strategically choosing which move is the optimal one.

## How to Play

The game itself is quite simple. Each player has two hands, and begins with one finger raised on each hand. The players decide who goes first. The first player can tap either hand with a raised finger on any opponent's hand with a raised finger. Upon doing so, the opponent adds that many fingers to their hand.

For example, say Alice has 2 fingers raised on her left hand and 3 on her right, while Bob has 1 finger raised on his left hand and 2 on his right. Alice can then tap her left hand on Bob's left hand, leaving her hands unchanged, but Bob now has 4 fingers raised on his left hand and 2 on his right.

If a player would have more than five fingers on their hand, they instead subtract 5 and put up the number of fingers leftover. For example, if Alice taps her hand with 3 fingers on Bob's hand with 4 fingers, instead of putting up 7 fingers, Bob will put up 2.

If a player would have exactly 5 fingers raised on their hand, they lose that hand and remove it from play. When a player has no hands left, they lose the game.

During each turn, a player may choose to "Split" instead of tapping an opponent's hand. If they choose to split, they can distribute their fingers in any way amongst both hands (even if one hand is removed from play).

For example, if Alice has 4 fingers on her right hand and none on her left, she can split to have 2 on her left hand and 2 on her right. A player may not split and distribute their fingers into the same rearrangment (effectively skipping their turn).

Note: There are many different variations and versions of the game. See https://www.wikihow.com/Play-Chopsticks for more information.

## Solving Chopsticks

My first approach to solving the game of chopsticks was to create a mathematically perfect algorithm - making the perfect move every single time without fail. In order to do this, I started with modeling the game as a state machine.

### The Chopsticks States

First, I created a notation which allows me to show the game in any state. To begin with, I used an ordered pair to represent a player's hands e.g. (2, 3) corresponds to having two fingers on one hand and three fingers on the other. Since chopsticks doesn't differentiate between a player's right and left hand, we can use an ordered pair (a, b) where a <= b. This means for a traditional game with five fingers on each hand, there are 15 total possible hands.

Next, I translate this to an actual game state. At any point in the game, each player has a number (possibly zero) of fingers on each of their hands, along with it being one player's turn. I represent this as yet another ordered tuple. First, arbitrarily designate a player 0 and a player 1. Then, we put both players' hands in an ordered tuple, along with whose turn it is. For example, ((0, 2), (3, 3), 1) represents player 0 with two fingers on a hand, and player 1 with three fingers on both hands, with it being player 1's turn.

Finally, just for serialization sake, I designate each of these states an index. I iterate over each state and assign it an index:


$$
\displaylines{
((0,0), (0,0), 0) \Leftrightarrow \text{State Index: } 0 \\
((0,0), (0,1), 0) \Leftrightarrow \text{State Index: } 1 \\
((0,0), (0,2), 0) \Leftrightarrow \text{State Index: } 2 \\
\vdots \\
((4,4), (4,4), 0) \Leftrightarrow \text{State Index: } 224 \\
((0,0), (0,0), 1) \Leftrightarrow \text{State Index: } 225 \\
((0,0), (0,1), 1) \Leftrightarrow \text{State Index: } 226 \\
\vdots \\
((4,4), (3,4), 1) \Leftrightarrow \text{State Index: } 448 \\
((4,4), (4,4), 1) \Leftrightarrow \text{State Index: } 449 \\
}
$$

After all of this, we now have a way to represent any point in a game of chopsticks as a single number. Using each of these states and their indexes, we can model the whole game as a state machine - players take the state they are currently in, make an action, and cause the game to proceed to a new state. Some examples of game states and their respective state indexes are shown below.
//TODO: Insert diagram

### Constructing the Chopstix Graph

Now that we have numbered every single state that can occur in the game, we construct a graph. A graph is a mathematical object that consists of nodes (or vertices) connected by links (or edges). We will take each game state and represent it as a node in our graph, for a total of 450 nodes. Then, we will connect each node according to the possible moves that can be made.

For example, the usual starting state for chopsticks is each player begins with one finger on each hand, and it is player zero's turn - or $((1,1), (1,1), 0)$ in our state notation, or state index 80. From here, there is only one possible outcome - player zero will add one to a hand of player two, resulting in the state $((1,1), (1,2), 1)$, or state index 306. So, in our graph, we connect state index 80 to state 306, to show that one state leads to another.

//TODO: Insert diagram of two nodes; state 80 pointing to state 306

Of course, there are points in the game where a player has multiple options to choose from - that is, one node could lead to many different game states. In this case, we simply make multiple connections from that node to each of the possible outcomes. Here is an example:

//TODO: Insert diagram of a state pointing to multiple children

Note that we must also acknowledge that these nodes themselves are being pointed to by other nodes, and that our graph is not this tree-like structure below, but more complex, with all 450 nodes pointing all over the place to one another.

### Ranking Game States

Now that we have this massive graph structure, we can start doing some real math to figure out the best paths to take along the states in our graph to get to victory. Don't worry, I won't be showing too much math here, but if you have any experience with matrices or solving systems of equations, you'll see it's not too complicated.

We start by trying to assign every single state some kind of rank, or rating, which shows how good that state is for a particular player. For example, from the state $((1, 1), (0, 4), 0)$, player zero simply has to use either one of his hands to attack player two's remaining hand and win the game. Therefore, this is a pretty good state for player zero to be in, and a pretty bad one for player one. However, it's not so easy to tell how good or bad a state is for a player just by looking at it. We need some kind of algorithmic way to assign these ranks.

The algorithm I designed is quite simple. First, we iterate through every state in the graph and find the ones that correspond to a player winning (states where a player has no fingers on either hand means their opponent has won the game). Then, I assign each of these states a rank of 0 or 1 depending on if player zero or player one won the game. For example state $((3, 4), (0, 0), 1)$ corresponds to player zero winning, since player one has no fingers on their hand, so we assign it a rank of 0.

Next, we look at the parents of each of these states. Imagine, a state (as shown below) where both of it's children have a rank of 1 (meaning that any option the player takes from here results in player 1 winning). Then, this state should also have a rank of 1 - it is a state in which player 1 winning is guaranteed. Now imagine a situation in which player 1 has two possible moves to play - that is the state has two children in the graph. One child results in player 1 winning, and the other results in player 1 losing (or in other words, one child has rank 0, and the other child has rank 1). Then , we need some way to show this state being a sort of 50/50 fchance for player 1 winning. So, let's assign this state a rank of 0.5 - exactly halfway between player 0 winning and player 1 winning. Similarly, if there were three children, with one resulting in player 1 winning and the other resulting in player 0 winning, then the state would have a 1/3rd chance of player 1 winning and a 2/3rds chance of player zero winning, and so we assign it a rank of 0.667 or 2/3rds. Continuing this pattern above, we can see that the rank of any state should simply be the average of all of it's children. A few simple tree diagrams below show relevant examples.

NOTE: The actual math used to assigne every state it's rank is slightly more complex than this. Notice that our graph is not acyclic - that is, there are some states whose children are themselves. This means that in order to find the rank of every state, we must use a system of linear equations relating all the states to each other. A matrix is perfect for doing such a thing. For more information, see the following page on out-degree laplacian matrices.

Once we have assigned a rank to every single state, it is simply a choice of choosing the child with the rank closest to your player number. For example, if it is player 1's turn and they have three possible options to choose from, they can simply compare the ranks of each state. Let's say option one has a rank of 0.5, option two has a rank of 0.3 and option three has a rank of 0.75. Then, this means that player 1 should choose option three because it has more children that end up with player one winning, and player zero would want to end up in the second state where the rank is 0.3 because it would have more children with player zero winning.

### Indeterminate States

Another issue with this approach is that of indeterminate states. These are states that, when entered, the players enter an infinite loop in which no one can ever win. The existence of indeterminate states depends on a what game settings you play with (such as whether or not players are allowed to 'split' and redistribute their fingers on their turn), but every setting has at least two indeterminate states - $((0, 0), (0, 0), 0)$ and $((0, 0), (0, 0), 1)$. Both of these states are anomalous because they can never happen in an actual game, but according to our graph model, once they do happen, the players just remain stuck in these two states forever, So in order to account for these states 
I simply assigned each of them a value of 0.5 - exactly halfway between winning and losing, as a way of showing that these indeterminate states are more of a draw than either player winning. 

This approach also makes sense when considering what choice to make - if player one has to choose between entering an indeterminate state or not, he may compare their ranks. The indeterminate state has a rank of 0.5 which means he will decide to go for the indeterminate state if the other state's rank is less than 0.5 (that is, if the other state favors player zero). This is essentially equivalent to player 1 decided to draw the game and get stuck in an infinite loop, reather than moving the game into a position where player zero is more likely to win.

### Perfect Play Optimization

The last step in order to make sure that our chopstix algorithm really does implement the best moves, is to ensure that players use 'perfect play'. Until now, the rank of a state was simply the number of winning states that state led to, compared to the number of losing states which the state led to. A state with rank 0.5 meant half of the end states had player 1 winning, and the other half hand player 0 winning. A rank of 0.3 meant that 30% of the possible outcomes from that state had player one winning, while the remaining 70% had player zero winning. However, in a real game, players wouldn't blindly or randomly choose which state to play. For example, imageine a state where it is player 1's turn, and the two children state result in player 1 winning, and the other eresults in player zero winning. Simply taking the average would suggest that the rank of this state should be 0.5, but we can see that if player 1 is smart, they would always choose the path which results in them winning. So, if we assume that player 1 is a perfet layer, he would always choose this path, meaninng thatt the rank of this state should actually be 1.

## The Outcome

// We end up with a rank for each and every state in the game.
