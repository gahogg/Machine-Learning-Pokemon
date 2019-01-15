## Importing libraries
import numpy as np
import pandas as pd
import names
import copy

## Constants used for Types
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

## An Item to be held by a Pokemon
LEFTOVERS = (0, "Leftovers")

## An Ability
TORRENT = (0, "Torrent")

## Turns the array of Moves into a Dictionary for fast access (Amortized O(1) from Hashing)
def moves_to_dict(moves):
    d = {}
    for i in range(len(moves)):
        d[moves[i].move_str.lower()] = moves[i]
    return d

## Turns the array of Pokemon into a Dictionary for fast access (Amortized O(1) from Hashing)
def pokemon_to_dict(pokemon_array):
    d = {}
    for i in range(len(pokemon_array)):
        d[pokemon_array[i].poke_name.lower()] = pokemon_array[i]
    return d

## Converts a string to a Type. Not amazing code, but I could copy and paste very quickly
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

## Converts a type to a string. Not amazing code, but I could copy and paste very quickly
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

## Categories of Moves
PHYSICAL = 0
SPECIAL = 1
STATUS = 2

## (SAME-TYPE-ATTACK-BONUS is 1.5)
STAB = 1.5

## We make stats a vector for convenience, so we'll define the number of stats as 6
NUM_STATS = 6

## We'll index our stats array like stats[HP] for convenience
HP = 0
ATK = 1
DEF = 2
SPATK = 3
SPDEF = 4
SPD = 5

## We make moves a vector for convenience, so we'll define the number of Moves as 4
NUM_MOVES = 4

## 1 IV ==> 1 increase in that stat, so generally we want to max these out
STD_IVS = np.array([31, 31, 31, 31, 31, 31], dtype = np.int)

## We check if a Pokemon is fainted by if pokemonx.fainted == FAINTED
FAINTED = False
ALIVE = True

## We make a Player's team a vector for convenience, so we'll define the team size as 6 (Standard)
TEAM_SIZE = 6

## We only use this for determining which Player will go first
PLAYER1 = 0
PLAYER2 = 1

## We run the same loop for each Player, so we have Players as a vector and define the number of Players as 2
NUM_PLAYERS = 2

## Decisions of each Player to either stay in and FIGHT, or to SWITCH
FIGHT = 0
SWITCH = -1

## This game works with both People and Computer Players, so this is how we distinguish between these options
PERSON = -4
CPU = -5

## Weather effects
RAIN = 0
SUN = 1
SANDSTORM = 2
HAIL = 3
NORMAL_WEATHER = 4

## Move Terrains
PSYCHIC_TERRAIN = 0
ELECTRIC_TERRAIN = 1
GRASSY_TERRAIN = 2
MISTY_TERRAIN = 3

## Pokemon can have a gender which affect battles
MALE = 1
FEMALE = 2

## A class for a Move, which will be assigned to Pokemon
class Move:
    def __init__(self, type1, power, accuracy, priority, category, chance, move_str):
        self.type = type1 ## Nat representing a Type
        self.power = power ## Nat
        self.accuracy = accuracy ## Int between 0 and 100
        self.priority = priority ## Int
        self.category = category ## 0, 1, or 2 for Category
        self.chance = chance ## Int representing a percentage of an effect
        self.move_str = move_str ## Str which is the name of the Move
        self.pp = 10 ## For now

    ## A convenient string to view a Move
    def __str__(self):
        s = self.move_str + ":\n\n"
        s += "Type: " + type_to_string(self.type) + "\n"
        s += "Power: " + str(self.power) + "\n"
        s += "Category: " + category_to_string(self.category) + "\n"
        s += "Accuracy: " + str(self.accuracy) + "%"
        return s
    
    ## Given a type t, this will return the effectiveness of this Move used against type t
    ## Is 0 for doesn't affect, 0.5 for not very effective, 1 for normal, and 2 for super effective
    ## Relies on a CSV of data, which we will import using Pandas
    def get_effectiveness(self, t):
        ta = self.type
        td = t
        if (ta is None) or (td is None):
            return 1
        df = pd.read_csv('effectiveness.csv', sep = ',', header = None)
        return df[td][ta]
    
    ## Returns a damage boost if WATER move in RAIN or FIRE move in SUN
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

## A sample Move of each Type
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

## A list of these moves
MOVE_LIST = np.array([STRENGTH, SURF, THUNDERBOLT, BRICK_BREAK, EARTHQUAKE, PSYCHIC_M, STONE_EDGE, DARK_PULSE, IRON_HEAD, FLAMETHROWER, GRASS_KNOT, ICE_BEAM, SLUDGE_BOMB, AIR_SLASH, X_SCISSOR, SHADOW_BALL, DRAGON_CLAW, MOONBLAST])

## A class representing a Pokemon
class Pokemon:
    def __init__(self, poke_name, dex_num, name, type1, type2, bases, evs, ivs, moves, item, ability, nature_vector, happiness, gender):
        self.poke_name = poke_name ## Str representing Pokemon name
        self.dex_num = dex_num ## Int
        self.name = name ## Nickname given to Pokemon
        self.type1 = type1 ## Int representing its first type
        self.type2 = type2 ## Int representing its second type
        self.status = None ## Default status is None

        self.bases = bases ## np.array of Ints with shape (6, ) 
        self.evs = evs ## np.array of Ints with shape (6, )
        self.ivs = ivs ## np.array of Ints with shape (6, )

        self.gender = gender ## MALE or FEMALE
        self.happiness = 255 ## Default happiness to 255 (max)
        self.level = 100 ## Default level to 100 (max)
        
        self.crit_stage = 0 ## Default crit stage of 0
        
        self.moves = moves ## np.array of 4 Moves
        self.item = item ## ITEM (for now, tuples of (ID, str))
        self.ability = ability ## ABILITY (for now, tuples of (ID, STR))
        self.nature_vector = nature_vector ## np.array of shape (6, ). Component = 1 if untouched, 1.1 if improving, 0.9 if worsening

        self.stats = np.zeros(6, dtype = int) ## Empty np.array of 6 zeros for now, will soon be updated with bases, evs and ivs
        self.update_stats() ## update stats
        self.original_stats = np.copy(self.stats) ## We might want a copy of the original stats
        self.healthy = ALIVE ## We're not fainted yet!
        self.health_as_percent = self.get_percent_health() ## Showing health as percentage
    
    ## A convenient string to view a Pokemon
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
    
    ## A smaller convenient string to view a Pokemon
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
    
    ## Health as percentage
    def get_percent_health(self):
        return int(100 * (self.stats[HP] / self.original_stats[HP]))

    ## Updates the Pokemon's stats with bases, evs and ivs
    def update_stats(self):
        for i in range(NUM_STATS):
            if i == HP:
                self.stats[HP] = np.floor((2 * self.bases[HP]) + self.ivs[HP] + np.floor(0.25 * self.evs[HP])) + 110
            else:
                self.stats[i] = np.floor( ( ( (2 * self.bases[i]) + self.ivs[i] + np.floor(0.25 * self.evs[i]) ) + 5 ) * self.nature_vector[i])
    
    ## A str to represent what a Nature Vector is doing
    def nature_vector_to_string(self):
        s1 = s2 = ""
        for i in range(NUM_STATS):
            if self.nature_vector[i] == 1.1:
                s1 = stat_to_string(i) + " is increased, "
            elif self.nature_vector[i] == 0.9:
                s2 = stat_to_string(i) + " is decreased."
        return s1 + s2

    ## Returns possible critical damage bonus (probability based on crit stage)
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

    ## (Partly done as a test)
    ## Returns the random calculation in a damage calculation
    def attacking_rando(self):
        return 1 - ((0.15) * np.random.random())

    ## Returns STAB bonus if existent, else 1
    def stab_bonus(self, move):
        if (self.type1 == move.type) or (self.type2 == move.type):
            return STAB
        else:
            return 1
    
    ## Returns True if self has Move with str s, False else
    def has_move(self, s):
        s1 = s.lower()
        for i in range(NUM_MOVES):
            if (self.moves[i].move_str.lower() == s1) or (self.moves[i].move_str.lower() == s1):
                return i
        return False
    
    ## Returns a str of the Pokemon's Moves
    def moves_to_string(self):
        s = ""
        for i in range(NUM_MOVES):
            s += self.moves[i].move_str
            if i != NUM_MOVES - 1:
                s += ', '
            else:
                return s

    ## Returns a damage calculation of self using a move against defender, with given weather
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

## Easy way to get a Nature vector
def get_nature_vector(better, worse):
    n = np.ones(NUM_STATS, dtype = np.float)
    n[better] = 1.1
    n[worse] = 0.9
    return n

## Prints a stat as a Str
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

## Returns a category as a Str
def category_to_string(c):
    if c is PHYSICAL:
        return "Physical"
    elif c is SPECIAL:
        return "Special"
    else:
        return "Status"

## Returns a randomly generated Pokemon (like, really random)
def generate_random_pokemon():
    poke_name = names.get_first_name() ## Random 
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

## Returns a team of 6 random Pokemon
def generate_random_team():
    arr = np.empty(TEAM_SIZE, dtype = object)
    for i in range(TEAM_SIZE):
        arr[i] = generate_random_pokemon()
    return arr

## Returns the constant associated with a Move category's Str
def string_to_category(s):
        if s == "Physical":
            return PHYSICAL
        elif s == "Special":
            return SPECIAL
        else:
            return STATUS

## Returns a random team of 6 GEN1 Pokemon
def generate_random_gen1_team():
    a = np.empty(TEAM_SIZE, dtype = object)
    for i in range(TEAM_SIZE):
        index = np.random.randint(151)
        a[i] = copy.deepcopy(GEN1[index]) 
    return a

## Returns a np.array of moves stored in moves.csv
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

## Stores the Moves in moves.csv in this array
MOVE_ARRAY = get_moves()

## Returns a random PHYSICAL Move with a specified type
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

## Placing the moves in a dictionary for amortized O(1) access
MOVE_DICTIONARY = moves_to_dict(MOVE_ARRAY)

## returns an arry of Pokemon stored in gen1.csv
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

## Storing pokemon in gen1.csv in this constant
GEN1 = get_pokemon_data()

## Converting pokemon array into dictionary for amortized O(1) access
GEN1_DICTIONARY = pokemon_to_dict(GEN1)

## A class representing a Player which has a team of 6 Pokemon
class Player:
    def __init__(self, name, team, controller):
        self.name = name ## Str
        self.team = team ## np.array of 6 Pokemon
        self.active_pokemon_index = 0 
        self.controller = controller ## Either CPU or PERSON
        self.num_wins = 0
        self.won = False

    ## Returns the number of wins the Player has received
    def get_fitness(self):
        return self.num_wins
    
    ## Defining these functions so that python's sorted method will work on Players
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

    ## Will return the index of the Player's Pokemon with name s if it has it, else False
    def team_contains(self, s):
        s1 = s.lower()
        for i in range(TEAM_SIZE):
            if (self.team[i].poke_name.lower() == s1) or (self.team[i].name.lower() == s1):
                return i
        return False
    
    ## Returns the Pokemon the Player currently has active
    def get_active_pokemon(self):
        return self.team[self.active_pokemon_index]
    
    ## Has a small mutation chance (if using genetic.py) to change its team
    def mutation(self, mut_chance):
        for i in range(TEAM_SIZE):
            rando = np.random.randint(100)
            if rando < mut_chance:
                index = np.random.randint(151)
                self.team[i] = copy.deepcopy(GEN1[index]) 

    ## Heals the Player's team
    def refresh(self):
        self.won = False
        self.active_pokemon_index = 0
        for i in range(TEAM_SIZE):
            refreshed_pokemon = copy.deepcopy(GEN1_DICTIONARY[self.team[i].poke_name.lower()])
            self.team[i] = refreshed_pokemon

    ## Used for debugging to return a Boolean array of the Pokemon the Player has ALIVE still
    def get_alive_array(self):
        arr = np.zeros(TEAM_SIZE, dtype = int)
        for i in range(TEAM_SIZE):
            if self.team[i].healthy is ALIVE:
                arr[i] = 1
        return arr

    ## Will return an array of size 4 representing the effectivess of its moves on other_player's active Pokemon
    ## The AI uses it to help make its decision to FIGHT or SWITCH
    def get_goodness_array(self, other_player):
        our_pokemon = self.get_active_pokemon()
        opposing_pokemon = other_player.get_active_pokemon()
        goodness_array = np.zeros(shape = NUM_MOVES, dtype = float)

        for i in range(NUM_MOVES):
            s = our_pokemon.stab_bonus(our_pokemon.moves[i])
            e = our_pokemon.moves[i].get_effectiveness(opposing_pokemon.type1) * our_pokemon.moves[i].get_effectiveness(opposing_pokemon.type2)
            goodness_array[i] = s * e
        return goodness_array

    ## Sending out leading Pokemon
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

    ## Will return either SWITCH or FIGHT for a Player
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
    
    ## Returns the index of the Pokemon it is choosing to SWITCH to
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
    
    ## Print's the Player's team
    def print_team(self):
        print("*************************************************************")
        print(self.name + "'s team:")
        for i in range(TEAM_SIZE):
            print(self.team[i].smaller_string())
        print("*************************************************************")
    
    ## Returns True if the Player can SWITCH, else False
    def can_switch(self):        
        for i in range(TEAM_SIZE):
            if (self.team[i].healthy is ALIVE) and (self.active_pokemon_index != i):
                return True
        return False
    
    ## Changes the Player's active Pokemon to the one with index i
    def switch(self, i):
        if self.can_switch():
            self.active_pokemon_index = i
            #print(self.name + " sent out its " + self.get_active_pokemon().poke_name + "!\n")
        else:
            #print("confused in switch function...")
            pass

    ## Returns the index of the move the Player is choosing to use
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

## A class representing a game
class Game:
    def __init__(self, players):
        self.weather = NORMAL_WEATHER ## No interesting weather to begin
        self.players = players ## np.array of 2 Players
        self.game_over = False
        players[0].won = False
        players[1].won = False
        self.turn_count = 1

        ## Would be printing stuff...
        #for i in range(NUM_PLAYERS):
         #   if self.players[i].controller is PERSON:
        #      pass
                #print(self.players[i].name + "'s team***************")
                #self.players[i].print_team()
                #print("That was " + self.players[i].name + "'s team***************")

        ## Send out the Players' leading Pokemon
        for i in range(NUM_PLAYERS):
            self.players[i].start_selection()
        
        ## Doesn't really matter right now, but we'll say p1 is going first
        self.first = PLAYER1
    
    ## Run one entire turn in the battle
    def turn(self):
        self.turn_count += 1
        #print("Turn " + str(self.turn_count) + ":\n")
        
        ## Decide who goes first based on relative speeds of active pokemon
        if self.players[0].get_active_pokemon().stats[SPD] >= self.players[1].get_active_pokemon().stats[SPD]:
            self.first = PLAYER1
        else:
            self.first = PLAYER2

        ## Each will be either SWITCH, or FIGHT
        choices = np.array([None, None])
    
        ## Return the choices of each Player (SWITCH or FIGHT)
        for i in range(NUM_PLAYERS):
            choices[i] = self.players[i].get_choice(self.players[i-1])

        ## if either Player is switching, their indices to switch to will be stored here
        switch_indices = np.array([None, None])

        ## if either Player is fighting, their Move indices to fight with will be stored here
        move_indices = np.array([None, None])

        ## Getting players switch indices if switching, and Move indices if fighting
        for i in range(NUM_PLAYERS):
            if choices[i] is SWITCH:
                switch_indices[i] = self.players[i].get_switch_index(self.players[i-1])
            else:
                move_indices[i] = self.players[i].choose_move(self.players[i-1])

        ## Performing Switches
        for i in range(NUM_PLAYERS):
            if switch_indices[i] is not None:
                self.players[i].switch(switch_indices[i])
        
        ## If they both switched, might as well end the turn now
        if (choices[0] == SWITCH) and (choices[1] == SWITCH):
            #print("Turn " + str(self.turn_count) + " end\n")
            return

        ## Here we actually do the battling
        for i in range(NUM_PLAYERS):

            ## Here we can use python's negative indexing to decide who is the attacker, and who is defender
            attacker_index, defender_index = 0, 0
            if self.first is PLAYER2:
                    attacker_index = i - 1
                    defender_index = i
            else:
                attacker_index = i
                defender_index = i - 1

            ## If attacker is fighting:
            if move_indices[attacker_index] is not None:
                attacker = self.players[attacker_index]
                attacking_pokemon = attacker.get_active_pokemon()
                attacking_move = attacking_pokemon.moves[move_indices[attacker_index]]

                defender = self.players[defender_index]
                defending_pokemon = defender.get_active_pokemon()

                ## Calculate the damage against defending pokemon with given move and weather
                damage = int(attacking_pokemon.calc_damage(attacking_move, defending_pokemon, self.weather)) 

                ## It has a chance of missing
                if(attacking_move.accuracy >= np.random.randint(100)):
                    defending_pokemon.stats[HP] -= damage
                    #print(defender.name + "'s " + defending_pokemon.poke_name + " got hit by " + attacking_pokemon.poke_name + "'s " + attacking_move.move_str + "!\n")
                    #print("It dealt " + str(damage) + "!\n")
                    
                    ## If we made them faint
                    if (defending_pokemon.stats[HP] <= 0):
                        defending_pokemon.stats[HP] = 0 ## Don't need any negative health values
                        defending_pokemon.healthy = FAINTED ## set the defending Pokemon to FAINTED
                        #print(defender.name + "'s " + defending_pokemon.poke_name + " has fainted!\n")

                        ## If they can switch:
                        if(defender.can_switch()):
                            #print(defender.name + ", please switch in a different pokemon!\n")

                            ## Get switch index and perform switch
                            index = defender.get_switch_index(attacker) 
                            defender.switch(index)
                            break                  
                        else:
                            ## They can't switch, so attacker wins!
                            self.game_over = True
                            #print("Congrats " + attacker.name + ", you have won!")
                            print(attacker.name + " has won " + str(attacker.get_fitness() + 1) + " now!")
                            attacker.won = True ## This is neccessary for genetic.py
                            return
                else:
                    pass
                    #print(attacker.name + "'s " + attacking_pokemon.poke_name + "'s " + attacking_move.move_str + " missed!")
        #print("Turn " + str(self.turn_count) + " end\n")
        return

## We included class trainer Red's team for fun
'''reds_team = np.array([copy.deepcopy(GEN1_DICTIONARY["pikachu"]), copy.deepcopy(GEN1_DICTIONARY["lapras"]), copy.deepcopy(GEN1_DICTIONARY["snorlax"]), copy.deepcopy(GEN1_DICTIONARY["venusaur"]), copy.deepcopy(GEN1_DICTIONARY["charizard"]), copy.deepcopy(GEN1_DICTIONARY["blastoise"])])
reds_team[0].moves = np.array([MOVE_DICTIONARY["volt tackle"], MOVE_DICTIONARY["iron tail"], MOVE_DICTIONARY["quick attack"], MOVE_DICTIONARY["thunderbolt"]])
reds_team[1].moves = np.array([MOVE_DICTIONARY["body slam"], MOVE_DICTIONARY["brine"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["psychic"]])
reds_team[2].moves = np.array([MOVE_DICTIONARY["shadow ball"], MOVE_DICTIONARY["crunch"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["giga impact"]])
reds_team[3].moves = np.array([MOVE_DICTIONARY["frenzy plant"], MOVE_DICTIONARY["giga drain"], MOVE_DICTIONARY["sludge bomb"], MOVE_DICTIONARY["sleep powder"]])
reds_team[4].moves = np.array([MOVE_DICTIONARY["blast burn"], MOVE_DICTIONARY["flare blitz"], MOVE_DICTIONARY["air slash"], MOVE_DICTIONARY["dragon pulse"]])
reds_team[5].moves = np.array([MOVE_DICTIONARY["hydro cannon"], MOVE_DICTIONARY["blizzard"], MOVE_DICTIONARY["flash cannon"], MOVE_DICTIONARY["focus blast"]])
red = Player("Red", reds_team, CPU)'''

## For purposes of genetic.py, we comment this out. But this is how you could play games if you wanted to.
'''
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