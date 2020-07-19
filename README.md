# Machine-Learning-Pokemon
This program uses genetic algorithms and artificial intelligence to build the best Pokemon team.

What does it do?

This program will create a N players, each of which will be treated as a chromosome in a Population (based on Darwin's Theory of Evolution).
Every player has a team of 6 random Pokemon from the first Generation of Pokemon (Blue, Red) but with up-to-date moves and types. We call the team the allele of the Player.

We then run n cycles, where each player will battle against every other, keeping track of the number of wins each player obtained. We call the number of wins of each player their Fitness.
Next, we do a weighted selection (directly proportionate to each player's fitness level) to choose the parents for the offspring for the next generation.
For each set of parents, we do Crossover, which will create a Player that has a combination of its two parent's Pokemon. We now have a new Population of the same size, where each Player is likely better than the previous generation.
The final step is a small mutation chance of each part of the allele, which will create a new random Pokemon in a player's team.

How do I use it?

To use the program, simply download and then run genetic.py. Personally I use Jupyter Notebook as this is the easiest way to interact with it. At the bottom of Genetic.py you can adjust the parameters in creating the instance of the class Player, which represents the Population.

I also included commented-out classes of Population and Chromosome which demonstrate how an abstract genetic algorithm class works.
