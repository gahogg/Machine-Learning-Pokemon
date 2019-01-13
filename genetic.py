import numpy as np
import pokemon as pok
import names
import copy as cp

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

class Players:
    def __init__(self, num_players, team_size, mut_chance):
        self.players = np.empty(num_players, dtype = object)
        self.num_players = num_players
        self.team_size = team_size
        self.mut_chance = mut_chance
        self.num_cycles = 0
        self.num_games = 0

        for i in range(self.num_players):
            random_player = pok.Player(names.get_first_name(), pok.generate_random_gen1_team(), pok.CPU)
            self.players[i] = random_player
    
    def __str__(self):
        s = ""
        s += "The population:\n" + str(self.players)
        s += "Average fitness: " + str(self.average_fitness())
        s += "Maximum fitness: " + str(self.max_fitness())
    
    def average_fitness(self):
        return self.fitness_sum() / self.num_players

    def max_fitness(self):
        m = 0
        for i in range(self.num_players):
            if self.players[i].get_fitness() > m:
                m = self.players[i].get_fitness()
        return m

    def fitness_sum(self):
        s = 0
        for i in range(self.num_players):
            s += self.players[i].get_fitness()
        return s

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
    
    def cycle(self):
        self.do_battles()
        self.print_wins()
        self.crossover()
        for i in range(self.num_players):
            self.players[i].mutation(self.mut_chance)
        self.refresh_all()
    
    def cycle_no_changes(self):
        self.do_battles()
        self.refresh_all()
        self.print_wins()
        
    def refresh_all(self):
        for i in range(self.num_players):
            self.players[i].refresh()
    
    def print_wins(self):
        for i in range(self.num_players):
            print(self.players[i].name + " won " + str(self.players[i].get_fitness()) + " games in total!")

#TARGET = np.array([0, 1, 0, 0, 1, 1, 0, 0, 1])

'''def f(c, target):
    s = 0
    for i in range(c.allele_len):
        if (c.allele[i] == target[i]):
            s += 1
    return s'''

players = Players(100, pok.TEAM_SIZE, 2)
print("Initial: " + str(players.max_fitness()))
for i in range(100):
    players.cycle()

players.cycle_no_changes()

print("After 2: " + str(players.max_fitness()))

