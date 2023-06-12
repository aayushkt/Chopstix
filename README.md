# Chopstix

## Introduction

Chopstix is a project based on the game classic game "Chopsticks", also known as "Finger Chess", "Swords", "Magic Fingers", and more. Although the rules of the game are quite simple, they can lead to surprisingly complex gameplay.

Chopstix algorithmically maps out the entirety of the game - analyzing every single move that can be made, and strategically choosing which move is the optimal one. It takes into account all possibilities, including getting stuck in infinite loops, playing against a perfect player, and more, and makes the objectively best decision. If Chopstix cannot win a game from a position, no one can.

## How to Play

The game itself is quite simple. Each player has two hands, and begins with one finger raised on each hand. The players decide who goes first. Then players alternate taking turns. Each turn, a player has two options - they may either 'attack' the opponent, or 'split' their own hands.

For more information on how to play the game, see [How To Play](How-To-Play.md).

Note: There are many different variations and versions of the game. See https://www.wikihow.com/Play-Chopsticks for more information.

## Solving Chopsticks

My approach to solving the game of chopsticks was to create a mathematically perfect algorithm - making the perfect move every single time without fail. At a high level, the algorithm has three distinct phases. First, the algorithm generates a state index (or number) for every possible state that could occur in the game. Then, it connects all the states together into a graph, showing every possible move that can take place in the game. Next, it analyzes every possible move in order to assign each and every state a rank - a special value which quantifies whether the state favors the player or the opponent. Once these ranks are assigned, the algorithm can take any state, and decide which moves lead to the state with the best rank.

To see a more in-depth, step-by-step walkthrough of my algorithm, check out [The Chopstix Algorithm](The-Chopstix-Algorithm.md).
