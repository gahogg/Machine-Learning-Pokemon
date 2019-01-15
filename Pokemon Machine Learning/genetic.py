## Importing libraries
import numpy as np
import pokemon as pok
import names
import copy as cp

## This class represents a Population, where each member of the Population is a Player with a team of 6 Pokemon
## We consider each Player to be a Chromosome in the Population, where their team of 6 Pokemon is the Chromosome's Allele
## The Fitness Function we use for a Player is the number of wins they get in a cycle (every Player battles against every other)
## Read the README and guide for more information
class Players:

    ## To define a Population of Players, we pass in the size of our desired Population, the size of the Allele,
    ## and a mutation chance as an integer from 0-100
    def __init__(self, num_players, team_size, mut_chance):
        self.players = np.empty(num_players, dtype = object) # Vector of Players representing the Population, initially empty array
        self.num_players = num_players 
        self.team_size = team_size
        self.mut_chance = mut_chance

        ## Assigning each component of the vector a random Player of 6 random Pokemon
        for i in range(self.num_players):
            random_player = pok.Player(names.get_first_name(), pok.generate_random_gen1_team(), pok.CPU)
            self.players[i] = random_player
    
    ## A nice string representation to show the Population
    def __str__(self):
        s = ""
        s += "The population:\n" + str(self.players)
        s += "Maximum fitness: " + str(self.max_fitness())

    ## Returns the maximum number of wins that any player received in the most recent cycle
    def max_fitness(self):
        m = 0
        for i in range(self.num_players):
            if self.players[i].get_fitness() > m:
                m = self.players[i].get_fitness()
        return m

    ## Returns the sum of the fitnesses of the Population, which we use to make a weighted Selection
    def fitness_sum(self):
        s = 0
        for i in range(self.num_players):
            s += self.players[i].get_fitness()
        return s
    
    ## Every Player battles against every other, recording the number of wins they have in the Player object
    def do_battles(self):
        for i in range(self.num_players - 1):
            player = self.players[i]
            index = i
            while True:
                if index == self.num_players - 1:
                    break
                other = self.players[index + 1]
                player.refresh()
                other.refresh()
                
                g = pok.Game(np.array([player, other]))
                while True:
                    g.turn()
                    if player.won:
                        player.num_wins += 1
                        break
                    elif other.won:
                        other.num_wins += 1
                        break
                    
                index += 1
        
    ## This will return a vector with the same size as the Population earlier defined. Each component of the array
    ## is a 2D vector, where each object of this 2D vector is a parent (a chromosome in the population). 
    ## We get these parents through a weighted selection proportionate to the fitness levels of the Players.
    ## We will call this function from crossover, where we create the new generation of Players
    def selection(self):
        s = self.fitness_sum()
        self.players.sort()
        parent_array = np.empty(self.num_players, dtype = object)
        for i in range(self.num_players):
            parents = np.empty(2, dtype = object)
            for j in range(2):
                num = np.random.randint(s)
                cur_index = 0
                for k in range(self.num_players):
                    cur_index += self.players[k].get_fitness()
                    if cur_index > num:
                        parents[j] = self.players[k]
                        break
            parent_array[i] = parents
        return parent_array

    ## This function will not return anything, but it will create the new generation of Players using the Selected Parents.
    ## For each set of Parents, we choose a split index to merge Parent 1's Allele with Parent 2's Allele. We then create
    ## a new Player object with this merged team of Pokemon.
    def crossover(self):
        parent_array = self.selection()
        new_players = np.empty(self.num_players, dtype = object)
        for i in range(self.num_players):
            split_index = np.random.randint(self.team_size)
            new_team = np.concatenate((parent_array[i][0].team[0:split_index], parent_array[i][1].team[split_index:]), axis = None)
            name = names.get_first_name()
            player = pok.Player(name, new_team, pok.CPU)
            new_players[i] = player
        self.players = new_players
    
    ## Running one cycle of battling, selection and crossover
    def cycle(self):
        self.do_battles()
        self.print_wins()
        self.crossover()
        for i in range(self.num_players):
            self.players[i].mutation(self.mut_chance) ## Small chance of each Pokemon changing to a random one, to stay diverse
        self.refresh_all() ## Refresh just ensures each Player's team is healthy
    
    ## We use this because running a whole cycle will create a new generation, which we don't always want to do
    def cycle_no_changes(self):
        self.do_battles()
        self.refresh_all()
        self.print_wins()
    
    ## Ensure's each Player's team is healthy
    def refresh_all(self):
        for i in range(self.num_players):
            self.players[i].refresh()
    
    ## Shows the wins of each Player
    def print_wins(self):
        for i in range(self.num_players):
            print(self.players[i].name + " won " + str(self.players[i].get_fitness()) + " games in total!")

## Here is where we actually run the code...

## We create a Population of 100 (arbitrary choice) Players, each with pok.TEAM_SIZE == 6 Pokemon, and a mutation chance of 2 percent
players = Players(100, pok.TEAM_SIZE, 2)

## We output our maximum Fitness
print("Initial: " + str(players.max_fitness()))

## We run 25 cycles (Still takes pretty long!)
for i in range(25):
    players.cycle()

## Do one more cycle where we don't change the Population
players.cycle_no_changes()

## Finally we output the number of wins that the best Player recieved (For me was around 90/99 games)
print("After 25: " + str(players.max_fitness()))

## And that is the end of our program!



## We leave this commented-out code below to show how an arbitrary genetic algorithm works (Selection, Crossover, Mutation)
## The code is uncommented as it is essentially the same as how our Players class operates, with the exception of
## of passing in a desired fitness function to use, and an optional target which could represent a desired allele.

## This is an example of how a desired allele might look. This is for pattern matching
#TARGET = np.array([0, 1, 0, 0, 1, 1, 0, 0, 1])

## Here is an example of a fitness function that matches the pattern matching
'''def f(c, target):
    s = 0
    for i in range(c.allele_len):
        if (c.allele[i] == target[i]):
            s += 1
    return s'''

'''ALLELE_LEN = 9
ALPHABET_SIZE = 2
MUT_CHANCE = 1
        
class Chromosome:
    def __init__(self, allele, mut_chance, fit_function, target):
        self.allele = allele
        self.allele_len = len(allele)
        self.mut_chance = mut_chance
        self.fitness_function = fit_function
        self.target = target

    def mutation(self):
        for locus in range(self.allele_len):
            rando = np.random.randint(100)
            if rando < self.mut_chance:
                while True:
                    change = np.random.randint(ALPHABET_SIZE)
                    if change == self.allele[locus]:
                        continue
                    else:
                        self.allele[locus] = change
                        break
    
    def __str__(self):
        s = ""
        s += str(self.allele)
        return s

    def get_fitness(self):
        return self.fitness_function(self, self.target)

    def __eq__(self, other):
        return self.get_fitness() == other.get_fitness()
    
    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()
    
    def __le__(self, other):
        return self.get_fitness() <= other.get_fitness()
    
    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()
    
    def __ge__(self, other):
        return self.get_fitness() >= other.get_fitness()'''


'''class Population:
    def __init__(self, pop_size, allele_len, alph_size, mut_chance, fit_funciton, target):
        self.pop = np.empty(pop_size, dtype = object)
        self.pop_size = pop_size
        self.allele_len = allele_len
        self.alph_size = alph_size
        self.mut_chance = mut_chance
        self.fitness_function = fit_funciton
        self.target = target
        self.turns = 0

        for i in range(self.pop_size):
            random_allele = np.random.randint(self.alph_size, size = self.allele_len)
            self.pop[i] = Chromosome(random_allele, self.mut_chance, self.fitness_function, self.target)
    
    def __str__(self):
        s = ""
        s += "The population:\n" + str(self.pop)
        s += "Average fitness: " + str(self.average_fitness())

    def average_fitness(self):
        return self.fitness_sum() / self.pop_size

    def fitness_sum(self):
        s = 0
        for i in range(self.pop_size):
            s += self.pop[i].get_fitness()
        return s

    def selection(self):
        s  = self.fitness_sum()
        self.pop.sort()
        parent_array = np.empty(self.pop_size, dtype = object)
        for i in range(self.pop_size):
            parents = np.empty(2, dtype = object)
            for j in range(2):
                num = np.random.randint(s)
                cur_index = 0
                for k in range(self.pop_size):
                    cur_index += self.pop[k].get_fitness()
                    if cur_index > num:
                        parents[j] = self.pop[k]
                        break
            parent_array[i] = parents
        return parent_array
    
    def crossover(self):
        parent_array = self.selection()
        new_pop = np.empty(self.pop_size, dtype = object)
        for i in range(self.pop_size):
            split_index = np.random.randint(self.allele_len)
            new_allele = np.concatenate((parent_array[i][0].allele[0:split_index], parent_array[i][1].allele[split_index:]), axis = None)
            new_pop[i] = Chromosome(new_allele, self.mut_chance, self.fitness_function, self.target)
        self.pop = new_pop
    
    def cycle(self):
        self.crossover()
        for i in range(self.pop_size):
            self.pop[i].mutation()'''