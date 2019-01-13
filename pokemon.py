import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import names
import copy

NORMAL = 0
FIGHTING = 1
FLYING = 2
POISON = 3
GROUND = 4
ROCK = 5
BUG = 6
GHOST = 7
STEEL = 8
FIRE = 9
WATER = 10
GRASS = 11
ELECTRIC = 12
PSYCHIC = 13
ICE = 14
DRAGON = 15
DARK = 16
FAIRY = 17

NUM_TYPES = 18

LEFTOVERS = (0, "Leftovers")

TORRENT = (0, "Torrent")


def moves_to_dict(moves):
    d = {}
    for i in range(len(moves)):
        d[moves[i].move_str.lower()] = moves[i]
    return d

def pokemon_to_dict(pokemon_array):
    d = {}
    for i in range(len(pokemon_array)):
        d[pokemon_array[i].poke_name.lower()] = pokemon_array[i]
    return d
        
def string_to_type(t):

    if t is np.nan:
        return None
    t = t.upper()

    if t == "NORMAL":
        return NORMAL
    elif t == "WATER":
        return WATER
    elif t == "ELECTRIC":
        return ELECTRIC
    elif t == "FIGHTING":
        return FIGHTING
    elif t == "GROUND":
        return GROUND
    elif t == "PSYCHIC":
        return PSYCHIC
    elif t == "ROCK":
        return ROCK
    elif t == "DARK":
        return DARK
    elif t == "STEEL":
        return STEEL
    elif t == "FIRE":
        return FIRE
    elif t == "GRASS":
        return GRASS
    elif t == "ICE":
        return ICE
    elif t == "POISON":
        return POISON
    elif t == "FLYING":
        return FLYING
    elif t == "BUG":
        return BUG
    elif t == "GHOST":
        return GHOST
    elif t == "DRAGON":
        return DRAGON
    elif t == "FAIRY":
        return FAIRY
    else:
        return None

def type_to_string(t):
    if t is NORMAL:
        return "Normal"
    elif t is WATER:
        return "Water"
    elif t is ELECTRIC:
        return "Electric"
    elif t is FIGHTING:
        return "Fighting"
    elif t is GROUND:
        return "Ground"
    elif t is PSYCHIC:
        return "Psychic"
    elif t is ROCK:
        return "Rock"
    elif t is DARK:
        return "Dark"
    elif t is STEEL:
        return "Steel"
    elif t is FIRE:
        return "Fire"
    elif t is GRASS:
        return "Grass"
    elif t is ICE:
        return "Ice"
    elif t is POISON:
        return "Poison"
    elif t is FLYING:
        return "Flying"
    elif t is BUG:
        return "Bug"
    elif t is GHOST:
        return "Ghost"
    elif t is DRAGON:
        return "Dragon"
    elif t is FAIRY:
        return "Fairy"
    elif t is None:
        return "non-existent"

PHYSICAL = 0
SPECIAL = 1
STATUS = 2

STAB = 1.5

NUM_STATS = 6

HP = 0
ATK = 1
DEF = 2
SPATK = 3
SPDEF = 4
SPD = 5

NUM_MOVES = 4
STD_IVS = np.array([31, 31, 31, 31, 31, 31], dtype = np.int)
FAINTED = False
ALIVE = True

TEAM_SIZE = 6
PLAYER1 = 0
PLAYER2 = 1
NUM_PLAYERS = 2

FIGHT = 0
SWITCH = -1
PERSON = -4
CPU = -5

RAIN = 0
SUN = 1
SANDSTORM = 2
HAIL = 3
NORMAL_WEATHER = 4

PSYCHIC_TERRAIN = 0
ELECTRIC_TERRAIN = 1
GRASSY_TERRAIN = 2
MISTY_TERRAIN = 3

MALE = 1
FEMALE = 2

class Move:
    def __init__(self, type1, power, accuracy, priority, category, chance, move_str):
        self.type = type1
        self.power = power
        self.accuracy = accuracy
        self.priority = priority
        self.category = category
        self.chance = chance
        self.move_str = move_str
        self.pp = 10 ## For now

    def __str__(self):
        s = self.move_str + ":\n\n"
        s += "Type: " + type_to_string(self.type) + "\n"
        s += "Power: " + str(self.power) + "\n"
        s += "Category: " + category_to_string(self.category) + "\n"
        s += "Accuracy: " + str(self.accuracy) + "%"
        return s

    def get_effectiveness(self, t):
        ta = self.type
        td = t
        if (ta is None) or (td is None):
            return 1
        df = pd.read_csv('effectiveness.csv', sep = ',', header = None)
        return df[td][ta]

    def attacking_weather_bonus(self, weather):
        if (weather is not SUN) and (weather is not RAIN):
            return 1
        elif weather is SUN: 
            if self.type is FIRE:
                return 1.5
            elif self.type is WATER:
                return 0.5
            else:
                return 1
        elif weather is RAIN:
            if self.type is WATER:
                return 1.5
            elif self.type is FIRE:
                return 0.5
            else:
                return 1

STRENGTH = Move(NORMAL, 80, 100, 0, PHYSICAL, None, "Strength")
SURF = Move(WATER, 90, 100, 0, SPECIAL, None, "Surf")
THUNDERBOLT = Move(ELECTRIC, 90, 100, 0, SPECIAL, 10, "Thunderbolt")
BRICK_BREAK = Move(FIGHTING, 75, 100, 0, PHYSICAL, 100, "Brick Break")
EARTHQUAKE = Move(GROUND, 100, 100, 0, PHYSICAL, 0, "Earthquake")
PSYCHIC_M = Move(PSYCHIC, 90, 100, 0, SPECIAL, 20, "Psychic")
STONE_EDGE = Move(ROCK, 100, 80, 0, PHYSICAL, None, "Stone Edge")
DARK_PULSE = Move(DARK, 80, 100, 0, SPECIAL, 20, "Dark Pulse")
IRON_HEAD = Move(STEEL, 80, 100, 0, PHYSICAL, 30, "Iron Head")
FLAMETHROWER = Move(FIRE, 90, 100, 0, SPECIAL, 10, "Flamethrower")
GRASS_KNOT = Move(GRASS, 90, 100, 0, SPECIAL, None, "Grass knot")
ICE_BEAM = Move(ICE, 90, 100, 0, SPECIAL, 10, "Ice Beam")
SLUDGE_BOMB = Move(POISON, 90, 100, 0, SPECIAL, 30, "Sludge Bomb")
AIR_SLASH = Move(FLYING, 75, 95, 0, SPECIAL, 30, "Air Slash")
X_SCISSOR = Move(BUG, 80, 100, 0, PHYSICAL, None, "X_Scissor")
SHADOW_BALL = Move(GHOST, 80, 100, 0, SPECIAL, 20, "Shadow Ball")
DRAGON_CLAW = Move(DRAGON, 75, 100, 0, PHYSICAL, None, "Dragon Claw")
MOONBLAST = Move(FAIRY, 95, 100, 0, SPECIAL, 30, "Moonblast")
MOVE_LIST = np.array([STRENGTH, SURF, THUNDERBOLT, BRICK_BREAK, EARTHQUAKE, PSYCHIC_M, STONE_EDGE, DARK_PULSE, IRON_HEAD, FLAMETHROWER, GRASS_KNOT, ICE_BEAM, SLUDGE_BOMB, AIR_SLASH, X_SCISSOR, SHADOW_BALL, DRAGON_CLAW, MOONBLAST])

class Pokemon:
    def __init__(self, poke_name, dex_num, name, type1, type2, bases, evs, ivs, moves, item, ability, nature_vector, happiness, gender):
        self.poke_name = poke_name
        self.dex_num = dex_num
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.status = None

        self.bases = bases
        self.evs = evs
        self.ivs = ivs

        self.gender = gender
        self.happiness = 255
        self.level = 100
        
        self.crit_stage = 0
        
        self.moves = moves
        self.item = item
        self.ability = ability
        self.nature_vector = nature_vector

        self.stats = np.zeros(6, dtype = int)
        self.update_stats()
        self.original_stats = np.copy(self.stats)
        self.healthy = ALIVE
        self.health_as_percent = self.get_percent_health()
    
    def __str__(self):
        s = self.name + " is a " + self.poke_name
        s += "\nIt is the " + str(self.dex_num) + "th Pokemon in the dex."
        s += "\nIts first type is " + type_to_string(self.type1) + ", and its second type is " + type_to_string(self.type2) + "."
       
        s += "\n\nBase Stats:\n"
        
        for i in range(NUM_STATS):
            s += "\t-" + stat_to_string(i) + ": " + str(self.bases[i]) + "\n"
        
        s += "\n\nEVS:\n"
        
        for i in range(NUM_STATS):
            s += "\t-" + stat_to_string(i) + ": " + str(self.evs[i]) + "\n"

        s += "\n\nIVS:\n"
        
        for i in range(NUM_STATS):
            s += "\t-" + stat_to_string(i) + ": " + str(self.ivs[i]) + "\n"

        s += "\n\nStats\n"
        for i in range(NUM_STATS):
            s += "\t-" + stat_to_string(i) + ": " + str(self.stats[i]) + "\n"

        s += "\n\nMoves:\n"
        for i in range(NUM_MOVES):
            s += "\t-" + self.moves[i].move_str + "\n"
        
        s += "\n\nIt is holding a " + self.item[1] + ".\n"
        s+= "Its ability is " + self.ability[1] + ".\n" 
        s += "From its Nature, " + self.nature_vector_to_string() + "\n"
        
        return s
    
    def smaller_string(self):
        s = self.name + " is a " + self.poke_name
        s += "\nIts first type is " + type_to_string(self.type1) + ", and its second type is " + type_to_string(self.type2) + "."
        s += "\n\nMoves:\n"
        for i in range(NUM_MOVES):
            s += "\t-" + self.moves[i].move_str + "\n"
        s += "\n\nStats\n"
        for i in range(NUM_STATS):
            s += "\t-" + stat_to_string(i) + ": " + str(self.stats[i]) + "\n"
        s += "\n\nIt is holding a " + self.item[1] + ".\n"
        s += "Its ability is " + self.ability[1] + ".\n" 
        s += "Its max health is " + str(self.original_stats[HP]) + ", but now it is only " + str(self.stats[HP]) + ", which is " + str(self.health_as_percent) + "%.\n\n"
        return s
    
    def get_percent_health(self):
        return int(100 * (self.stats[HP] / self.original_stats[HP]))

    def update_stats(self):
        for i in range(NUM_STATS):
            if i == HP:
                self.stats[HP] = np.floor((2 * self.bases[HP]) + self.ivs[HP] + np.floor(0.25 * self.evs[HP])) + 110
            else:
                self.stats[i] = np.floor( ( ( (2 * self.bases[i]) + self.ivs[i] + np.floor(0.25 * self.evs[i]) ) + 5 ) * self.nature_vector[i])
    
    def nature_vector_to_string(self):
        s1 = s2 = ""
        for i in range(NUM_STATS):
            if self.nature_vector[i] == 1.1:
                s1 = stat_to_string(i) + " is increased, "
            elif self.nature_vector[i] == 0.9:
                s2 = stat_to_string(i) + " is decreased."
        return s1 + s2

    def attacking_critical_bonus(self, move):
        p = 0
        if self.crit_stage == 0:
            p = (1/24)
        elif self.crit_stage == 1:
            p = (1/8)
        elif self.crit_stage == 2:
            p = (1/2)
        else:
            p = 100
        r = np.random.random()
        if r <= p:
            return 1.5
        else:
            return 1

    def attacking_rando(self):
        return 1 - ((0.15) * np.random.random())

    def stab_bonus(self, move):
        if (self.type1 == move.type) or (self.type2 == move.type):
            return 1.5
        else:
            return 1

    def has_move(self, s):
        s1 = s.lower()
        for i in range(NUM_MOVES):
            if (self.moves[i].move_str.lower() == s1) or (self.moves[i].move_str.lower() == s1):
                return i
        return False
    
    def moves_to_string(self):
        s = ""
        for i in range(NUM_MOVES):
            s += self.moves[i].move_str
            if i != NUM_MOVES - 1:
                s += ', '
            else:
                return s

    def calc_damage(self, move, defender, weather):
        A = 0
        B = 0
        if move.category is PHYSICAL:
            A = self.stats[ATK]
            B = defender.stats[DEF]
        else:
            A = self.stats[SPATK]
            B = defender.stats[SPDEF]

        weather_bonus = move.attacking_weather_bonus(weather)
        crit = self.attacking_critical_bonus(move)
        rando = self.attacking_rando()
        type_effectiveness = move.get_effectiveness(defender.type1) * move.get_effectiveness(defender.type2)
        stab = self.stab_bonus(move)
        power = move.power

        ## Nerfing OP Moves
        if power >= 100:
            power = 100
        
        modifiers = weather_bonus * crit * rando * stab * type_effectiveness
        
        return np.floor(( ( ( ( (2 * self.level) / 5 ) + 2) * power * (A/B) / 50 ) + 2 ) * modifiers)


def get_nature_vector(better, worse):
    n = np.ones(NUM_STATS, dtype = np.float)
    n[better] = 1.1
    n[worse] = 0.9
    return n

def stat_to_string(s):
    if s is HP:
        return "HP"
    elif s is ATK:
        return "Atk"
    elif s is DEF:
        return "Def"
    elif s is SPATK:
        return "Sp. Atk"
    elif s is SPDEF:
        return "Sp. Def"
    elif s is SPD:
        return "Spd"
    elif s is None:
        return "non-existent"

def category_to_string(c):
    if c is PHYSICAL:
        return "Physical"
    elif c is SPECIAL:
        return "Special"
    else:
        return "Status"

def generate_random_pokemon():
    poke_name = names.get_first_name()
    dex_num = np.random.randint(150)
    name = names.get_first_name()
    t1 = int((NUM_TYPES) * np.random.random_sample())
    t2 = 0
    while True:
        t2 = int((NUM_TYPES) * np.random.random_sample())
        if t2 is not t1:
            break
    bases = np.random.randint(60, 120, size = NUM_STATS)
    ev_indices = np.empty(2, dtype = np.int)
    while True:
        ev_indices = np.random.randint(0, NUM_STATS, size = 2)
        if (ev_indices[0] != ev_indices[1]):
            break
    evs = np.zeros(NUM_STATS)
    evs[ev_indices[0]], evs[ev_indices[1]] = 252, 252
    ivs = STD_IVS
    move_indices = np.random.randint(MOVE_LIST.size, size = NUM_MOVES)
    moves = MOVE_LIST[move_indices]
    item = LEFTOVERS
    ability = TORRENT
    nature_indices = np.array([0, 0])
    while True:
        nature_indices = np.random.randint(NUM_STATS, size = 2)
        if (nature_indices[0] != nature_indices[1]) and (HP not in nature_indices):
            break
    nature_vector = get_nature_vector(nature_indices[0], nature_indices[1])
    happiness = 255
    gender = MALE
    return Pokemon(poke_name, dex_num, name, t1, t2, bases, evs, ivs, moves, item, ability, nature_vector, happiness, gender)

def generate_random_team():
    arr = np.empty(TEAM_SIZE, dtype = object)
    for i in range(TEAM_SIZE):
        arr[i] = generate_random_pokemon()
    return arr

def string_to_category(s):
        if s == "Physical":
            return PHYSICAL
        elif s == "Special":
            return SPECIAL
        else:
            return STATUS

def generate_random_gen1_team():
    a = np.empty(TEAM_SIZE, dtype = object)
    for i in range(TEAM_SIZE):
        index = np.random.randint(151)
        a[i] = copy.deepcopy(GEN1[index]) 
    return a

def get_moves():
    data = np.array(pd.read_csv('moves.csv', sep = ',', header = None))
    arr = np.empty(len(data), dtype = object)
    for i in range(len(data)):
        row = data[i]
        move_num = row[0]
        move_str = row[1]
        type1 = string_to_type(row[2].upper())
        category = string_to_category(row[3])
        pp = row[4]
        power = row[5]
        if (power == 'None') or (power == 'None\xa0') or(power is None) or (power is None) or (power is np.nan):
            power = 0
        power = int(power)
        accuracy = row[6]
        if (accuracy == 'None') or (accuracy == 'None\xa0') or (accuracy is None) or (accuracy is None) or (accuracy is np.nan):
            accuracy = 0
        accuracy = int(accuracy)
        m = Move(type1, power, accuracy, 0, category, None, move_str)
        arr[i] = m
    return arr

MOVE_ARRAY = get_moves()
def random_move_with_type(t):
    rand_index = np.random.randint(500)
    i = rand_index
    while True:
        if (MOVE_ARRAY[i].type == t) and (MOVE_ARRAY[i].category == PHYSICAL):
            return MOVE_ARRAY[i]
        elif i == 741:
            i = 0
            continue
        i += 1

MOVE_DICTIONARY = moves_to_dict(MOVE_ARRAY)

def get_pokemon_data():
    data = np.array(pd.read_csv('gen1.csv', sep = ',', header = None))
    new = np.empty(len(data), dtype = object)
    for i in range(len(data)):
        row = data[i]
        poke_name = row[0]
        type1 = string_to_type(row[1])
        type2 = string_to_type(row[2])

        stat_total = row[3]
        bases = np.array(row[4:10])
        move_indices = np.random.randint(MOVE_LIST.size, size = NUM_MOVES)
        moves = MOVE_LIST[move_indices]
        ev_indices = np.empty(2, dtype = np.int)
        while True:
            ev_indices = np.random.randint(0, NUM_STATS, size = 2)
            if (ev_indices[0] != ev_indices[1]):
                break
        evs = np.zeros(NUM_STATS)
        evs[ev_indices[0]], evs[ev_indices[1]] = 252, 252
        nature_indices = np.array([0, 0])
        while True:
            nature_indices = np.random.randint(NUM_STATS, size = 2)
            if (nature_indices[0] != nature_indices[1]) and (HP not in nature_indices):
                break

        nature_vector = get_nature_vector(nature_indices[0], nature_indices[1])
        
        new[i] = Pokemon(poke_name, i+1, names.get_first_name(), type1, type2, bases, evs, STD_IVS, moves, LEFTOVERS, TORRENT, nature_vector, 255, MALE)
        ## Changing first move to be of that pokemon's first type, and also second if it exists (Physical for now, and yes this will be slow)
        new[i].moves[0] = random_move_with_type(new[i].type1)
        if new[i].type2 is not None:
            new[i].moves[1] = random_move_with_type(new[i].type2) 
    return new

GEN1 = get_pokemon_data()

GEN1_DICTIONARY = pokemon_to_dict(GEN1)

class Player:
    def __init__(self, name, team, controller):
        self.name = name
        self.team = team
        self.active_pokemon_index = 0
        self.controller = controller
        self.num_wins = 0
        self.won = False

    def get_fitness(self):
        return self.num_wins
    
    def __eq__(self, other):
        return self.get_fitness() == other.get_fitness()
    
    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()
    
    def __le__(self, other):
        return self.get_fitness() <= other.get_fitness()
    
    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()
    
    def __ge__(self, other):
        return self.get_fitness() >= other.get_fitness()

    def team_contains(self, s):
        s1 = s.lower()
        for i in range(TEAM_SIZE):
            if (self.team[i].poke_name.lower() == s1) or (self.team[i].name.lower() == s1):
                return i
        return False
    
    def get_active_pokemon(self):
        return self.team[self.active_pokemon_index]
    
    def mutation(self, mut_chance):
        for i in range(TEAM_SIZE):
            rando = np.random.randint(100)
            if rando < mut_chance:
                index = np.random.randint(151)
                self.team[i] = copy.deepcopy(GEN1[index]) 

    def refresh(self):
        self.won = False
        self.active_pokemon_index = 0
        for i in range(TEAM_SIZE):
            refreshed_pokemon = copy.deepcopy(GEN1_DICTIONARY[self.team[i].poke_name.lower()])
            self.team[i] = refreshed_pokemon

    def get_alive_array(self):
        arr = np.zeros(TEAM_SIZE, dtype = int)
        for i in range(TEAM_SIZE):
            if self.team[i].healthy is ALIVE:
                arr[i] = 1
        return arr

    def get_goodness_array(self, other_player):
        our_pokemon = self.get_active_pokemon()
        opposing_pokemon = other_player.get_active_pokemon()
        goodness_array = np.zeros(shape = NUM_MOVES, dtype = float)

        for i in range(NUM_MOVES):
            s = our_pokemon.stab_bonus(our_pokemon.moves[i])
            e = our_pokemon.moves[i].get_effectiveness(opposing_pokemon.type1) * our_pokemon.moves[i].get_effectiveness(opposing_pokemon.type2)
            goodness_array[i] = s * e
        return goodness_array

    def start_selection(self):
        if self.controller is CPU:
            self.active_pokemon_index = 0 ## ML DECISION
            #print(self.name + " sent out its " + self.get_active_pokemon().poke_name + "!\n")
        else:
            while True:
                name = input(self.name + ", type the name of the pokemon you want to send out first!\n")
                p = self.team_contains(name)
                if p is False:
                    pass
                    #print("Try again " + self.name + ", you don't have that pokemon in your team.\n")
                else:
                    self.active_pokemon_index = p
                    break

    def get_choice(self, other_player):
        if self.controller is CPU:
            arr = self.get_goodness_array(other_player)
            max_num = np.max(arr)
            if (max_num < 1) and (self.can_switch()):
                return SWITCH
            else:
                return FIGHT
        else:
            while True:
                choice = input(self.name + ", type switch, or fight.\n").lower()

                if (choice != "switch") and (choice != "fight"):
                    #print("Try again " + self.name + ", type switch or fight please.\n")
                    pass
                elif choice == "switch":
                    if self.can_switch():
                        return SWITCH
                    else:
                        #print(self.name + ", all of your other pokemon have fainted! Choice has been made to fight.\n")
                        return FIGHT
                else:
                    return FIGHT
    
    def get_switch_index(self, other_player):
        if self.controller is CPU:
            our_pokemon = self.get_active_pokemon()
            opposing_pokemon = other_player.get_active_pokemon()
            dummy_moves = np.array([Move(opposing_pokemon.type1, 0, 0, 0, PHYSICAL, 0, "dummy"), Move(opposing_pokemon.type2, 0, 0, 0, PHYSICAL, 0, "dummy")])

            badness_array = np.zeros(TEAM_SIZE, dtype = float)
            for i in range(TEAM_SIZE):
                arr = np.empty(2, dtype = np.float)
                if (self.team[i].healthy == ALIVE) and (i != self.active_pokemon_index):
                    for j in range(2):
                        arr[j] = dummy_moves[j].get_effectiveness(our_pokemon.type1) * dummy_moves[j].get_effectiveness(our_pokemon.type2)
                    badness_array[i] = np.max(arr)
                else:
                    HUGE_NUMBER = 100000
                    badness_array[i] = HUGE_NUMBER
            best_index = np.argmin(badness_array)
            return best_index
        else:
            while True:
                name = input("Type the name of the pokemon you want to switch into please.\n").lower()
                p = self.team_contains(name)
                if p is False:
                    #print("Try again " + self.name + ", you don't have that pokemon in your team.\n")
                    pass
                elif self.team[p].healthy is FAINTED:
                    pass
                    #print("Try again " + self.name + ", that pokemon is fainted.\n")
                else:
                    return p
    
    def print_team(self):
        print("*************************************************************")
        print(self.name + "'s team:")
        for i in range(TEAM_SIZE):
            print(self.team[i].smaller_string())
        print("*************************************************************")
                    
    def can_switch(self):        
        for i in range(TEAM_SIZE):
            if (self.team[i].healthy is ALIVE) and (self.active_pokemon_index != i):
                return True
        return False
    
    def switch(self, i):
        if self.can_switch():
            self.active_pokemon_index = i
            #print(self.name + " sent out its " + self.get_active_pokemon().poke_name + "!\n")
        else:
            #print("confused in switch function...")
            pass

    def choose_move(self, other_player):
        if self.controller is CPU:
            goodness_array = self.get_goodness_array(other_player)
            return np.argmax(goodness_array)
        else:
            while True:
                #print(self.name + ", type which move would you like your " + self.get_active_pokemon().poke_name + " to use\n")
                #print(self.get_active_pokemon().poke_name + " has " + self.get_active_pokemon().moves_to_string() + ".\n")
                answer = input("...\n")
                move_index = self.get_active_pokemon().has_move(answer)
                if move_index is False:
                    pass
                    #print("Sorry " + self.name + ", your " + self.get_active_pokemon().poke_name + " does not have that move. Try again please.\n")
                else:
                    return move_index

class Game:
    def __init__(self, players):
        self.weather = NORMAL_WEATHER
        self.players = players
        self.game_over = False
        players[0].won = False
        players[1].won = False

        for i in range(NUM_PLAYERS):
            if self.players[i].controller is PERSON:
                pass
                #print(self.players[i].name + "'s team***************")
                #self.players[i].print_team()
                #print("That was " + self.players[i].name + "'s team***************")

        for i in range(NUM_PLAYERS):
            self.players[i].start_selection()
        
        self.first = PLAYER1

        if np.random.random() > .5:
            self.first = PLAYER2
        self.turn_count = 0
        
    def turn(self):
        self.turn_count += 1
        #print("Turn " + str(self.turn_count) + ":\n")
        
        if self.players[0].get_active_pokemon().stats[SPD] >= self.players[1].get_active_pokemon().stats[SPD]:
            self.first = PLAYER1
        else:
            self.first = PLAYER2

        choices = np.array([None, None])
    
        for i in range(NUM_PLAYERS):
            choices[i] = self.players[i].get_choice(self.players[i-1]) ## I think

        switch_indices = np.array([None, None])
        move_indices = np.array([None, None])

        for i in range(NUM_PLAYERS):
            if choices[i] is SWITCH:
                switch_indices[i] = self.players[i].get_switch_index(self.players[i-1])
            else:
                move_indices[i] = self.players[i].choose_move(self.players[i-1])

        ## Performing Switches
        for i in range(NUM_PLAYERS):
            if switch_indices[i] is not None:
                self.players[i].switch(switch_indices[i])
        
        if (choices[0] == SWITCH) and (choices[1] == SWITCH):
            #print("Turn " + str(self.turn_count) + " end\n")
            return

        for i in range(NUM_PLAYERS):
            attacker_index, defender_index = 0, 0
            if self.first is PLAYER2:
                    attacker_index = i - 1
                    defender_index = i
            else:
                attacker_index = i
                defender_index = i - 1

            if move_indices[attacker_index] is not None:
                attacker = self.players[attacker_index]
                attacking_pokemon = attacker.get_active_pokemon()
                attacking_move = attacking_pokemon.moves[move_indices[attacker_index]]

                defender = self.players[defender_index]
                defending_pokemon = defender.get_active_pokemon()

                damage = int(attacking_pokemon.calc_damage(attacking_move, defending_pokemon, self.weather))

                if(attacking_move.accuracy >= np.random.randint(100)):
                    defending_pokemon.stats[HP] -= damage
                    #print(defender.name + "'s " + defending_pokemon.poke_name + " got hit by " + attacking_pokemon.poke_name + "'s " + attacking_move.move_str + "!\n")
                    #print("It dealt " + str(damage) + "!\n")
                    
                    if (defending_pokemon.stats[HP] <= 0):
                        defending_pokemon.stats[HP] = 0
                        defending_pokemon.healthy = FAINTED
                        #print(defender.name + "'s " + defending_pokemon.poke_name + " has fainted!\n")
            
                        if(defender.can_switch()):
                            #print(defender.name + ", please switch in a different pokemon!\n")
                            index = defender.get_switch_index(attacker)
                            defender.switch(index)
                            break                  
                        else:
                            self.game_over = True
                            #print("Congrats " + attacker.name + ", you have won!")
                            print(attacker.name + " has won " + str(attacker.get_fitness() + 1) + " now!")
                            attacker.won = True
                            return
                else:
                    pass
                    #print(attacker.name + "'s " + attacking_pokemon.poke_name + "'s " + attacking_move.move_str + " missed!")
        #print("Turn " + str(self.turn_count) + " end\n")
        return

'''reds_team = np.array([copy.deepcopy(GEN1_DICTIONARY["pikachu"]), copy.deepcopy(GEN1_DICTIONARY["lapras"]), copy.deepcopy(GEN1_DICTIONARY["snorlax"]), copy.deepcopy(GEN1_DICTIONARY["venusaur"]), copy.deepcopy(GEN1_DICTIONARY["charizard"]), copy.deepcopy(GEN1_DICTIONARY["blastoise"])])
reds_team[0].moves = np.array([MOVE_DICTIONARY["volt tackle"], MOVE_DICTIONARY["iron tail"], MOVE_DICTIONARY["quick attack"], MOVE_DICTIONARY["thunderbolt"]])
reds_team[1].moves = np.array([MOVE_DICTIONARY["body slam"], MOVE_DICTIONARY["brine"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["psychic"]])
reds_team[2].moves = np.array([MOVE_DICTIONARY["shadow ball"], MOVE_DICTIONARY["crunch"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["giga impact"]])
reds_team[3].moves = np.array([MOVE_DICTIONARY["frenzy plant"], MOVE_DICTIONARY["giga drain"], MOVE_DICTIONARY["sludge bomb"], MOVE_DICTIONARY["sleep powder"]])
reds_team[4].moves = np.array([MOVE_DICTIONARY["blast burn"], MOVE_DICTIONARY["flare blitz"], MOVE_DICTIONARY["air slash"], MOVE_DICTIONARY["dragon pulse"]])
reds_team[5].moves = np.array([MOVE_DICTIONARY["hydro cannon"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["flash cannon"], MOVE_DICTIONARY["focus blast"]])

red = Player("Red", reds_team, CPU)

#p1 = Player("Greg", generate_random_gen1_team(), CPU)
p2 = Player(names.get_first_name(), generate_random_gen1_team(), CPU)
#p1.print_team()
#p2.print_team()
g = Game(np.array([red, p2]))

while True:
    g.turn()
    new_game = True
    if g.game_over:
        while True:
            inp = input("Do you wish to play again? [Y/N]")
            inp = inp.lower()
            if inp == "y":
                p1 = Player("Greg", generate_random_gen1_team(), CPU)
                p2 = Player(names.get_first_name(), generate_random_gen1_team(), CPU)
                p1.print_team()
                p2.print_team()
                g = Game(np.array([p1, p2]))
                new_game = True
                break
            elif inp == "n":
                new_game = False
                break
            else:
                print("Try again, please type [Y/N] for new game.")
    if new_game:
        continue
    else:
        break
print("DONE")'''