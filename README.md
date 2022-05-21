# Chopstix

## Introduction

Chopstix is a project based on the game classic Japanese game "Chopsticks", also known as "Finger Chess", "Swords", "Magic Fingers", and more. Although the rules of the game are quite simple, they can lead to surprisingly complex gameplay.

Chopstix is project that aims to solve the game of Chopsticks through a multitude of different technologies. Chopstix will contain two bots which the user can play against: Chick and Stop.

Chick plays Chopsticks by algorithmically mapping out the entirety of the game - analyzing every single move that can be made, and strategically choosing which move is the optimal one.

Stop plays in his own separate way entirely. Implementing Machine Learning technology and advanced neural network concepts, Stop uses Google's TensorFlow software to make decisions and learn the game in real-time.

## How to Play

The game itself is quite simple. Each player has two hands, with one finger raised on each hand. The players decide who goes first. The first player can tap either hand with a raised finger on any opponent's hand with a raised finger. Upon doing so, the opponent adds that many fingers to their hand.

For example, say Alice has 2 fingers raised on her left hand and 3 on her right, while Bob has 1 finger raised on his left hand and 2 on his right. Alice can then tap her left hand on Bob's left hand, leaving her hands unchanged, but Bob now has 4 fingers raised on his left hand and 2 on his right.

If a player would have more than five fingers on their hand, they instead put up the left over number after subtracting five. For example, if Alice taps her hand with 3 fingers on Bob's hand with 4 fingers, instead of putting up 7 fingers, Bob will put up 2.

If a player would have exactly 5 fingers raised on their hand, they lose that hand and remove it from play. When a player has no hands left, they lose the game.

During each turn, a player may choose to "Split" instead of tapping an opponent's hand. If they choose to split, they can distribute their fingers in any way amongst both hands (even if one hand is removed from play).

For example, if Alice has 4 fingers on her right hand and none on her left, she can split to have 2 on her left hand and 2 on her right. A player may not split and distribute their fingers into the same rearrangment (effectively skipping their turn).

Note: There are many different variations and versions of the game. See https://www.wikihow.com/Play-Chopsticks for more information.