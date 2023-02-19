# Chopstix

## Introduction

Chopstix is a project based on the game classic Japanese game "Chopsticks", also known as "Finger Chess", "Swords", "Magic Fingers", and more. Although the rules of the game are quite simple, they can lead to surprisingly complex gameplay.

Chopstix is project that aims to solve the game of Chopsticks through a multitude of different technologies. Chopstix will contain two bots which the user can play against: Chick and Stop.

Chick plays Chopsticks by algorithmically mapping out the entirety of the game - analyzing every single move that can be made, and strategically choosing which move is the optimal one.

Stop plays in his own separate way entirely. Implementing Machine Learning technology and advanced neural network concepts, Stop uses Google's TensorFlow software to make decisions and learn the game in real-time.

## How to Play

The game itself is quite simple. Each player has two hands, and begins with one finger raised on each hand. The players decide who goes first. The first player can tap either hand with a raised finger on any opponent's hand with a raised finger. Upon doing so, the opponent adds that many fingers to their hand.

For example, say Alice has 2 fingers raised on her left hand and 3 on her right, while Bob has 1 finger raised on his left hand and 2 on his right. Alice can then tap her left hand on Bob's left hand, leaving her hands unchanged, but Bob now has 4 fingers raised on his left hand and 2 on his right.

If a player would have more than five fingers on their hand, they instead put up the left over number after subtracting five. For example, if Alice taps her hand with 3 fingers on Bob's hand with 4 fingers, instead of putting up 7 fingers, Bob will put up 2.

If a player would have exactly 5 fingers raised on their hand, they lose that hand and remove it from play. When a player has no hands left, they lose the game.

During each turn, a player may choose to "Split" instead of tapping an opponent's hand. If they choose to split, they can distribute their fingers in any way amongst both hands (even if one hand is removed from play).

For example, if Alice has 4 fingers on her right hand and none on her left, she can split to have 2 on her left hand and 2 on her right. A player may not split and distribute their fingers into the same rearrangment (effectively skipping their turn).

Note: There are many different variations and versions of the game. See https://www.wikihow.com/Play-Chopsticks for more information.

## Solving Chopsticks

My first approach to solving the game of chopsticks was to create a mathematically perfect algorithm - making the perfect move every single time without fail. In order to do this, I started with modeling the game as a state machine.

### The Chopsticks State Machine

First, I created a notation which allows me to show the game in any state. To begin with, I used an ordered pair to represent a player's hands e.g. (2, 3) corresponds to having two fingers on one hand and three fingers on the other. Since chopsticks doesn't differentiate between a player's right and left hand, we can use an ordered pair (a, b) where a <= b. This means for a traditional game with five fingers on each hand, there are 15 total possible hands.

Next, I translate this to an actual game state. At any point in the game, each player has a number (possibly zero) of fingers on each of their hands, along with it being one player's turn. I represent this as yet another ordered tuple. First, arbitrarily designate a player 0 and a player 1. Then, we put both players' hands in an ordered tuple, along with whose turn it is. For example, ((0, 2), (3, 3), 1) represents player 0 with two fingers on a hand, and player 1 with three fingers on both hands, with it being player 1's turn.

Finally, just for serialization sake, I designate each of these states an index. I enumerate over each state and assign it a number as so:

((0,0), (0,0), 0) -> 0

((0,0), (0,1), 0) -> 1

((0,0), (0,2), 0) -> 2

.

.

.

((4, 4), (4, 4), 0) -> 224

((0, 0), (0, 0), 1) -> 225

((0, 0), (0, 1), 1) -> 226

.

.

.

((4, 4), (3, 4), 1) -> 448

((4, 4), (4, 4), 1) -> 449

After all of this, we now have a way to represent any point in a game of chopsticks as a single number. Using each of these states and their indexes, we can model the whole game as a state machine - players take the state they are currently in, make an action, and cause the game to proceed to a new state. 
