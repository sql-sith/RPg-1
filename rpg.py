import random
import enemies
import encounters

file = open("stats.txt", "r+")


class Player:
    def __init__(self):
        self.stats = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "wis": 0,
            "int": 0,
            "cha": 0,
        }
        self.stat_ability = {
            "str_ability": 0,
            "dex_ability": 0,
            "con_ability": 0,
            "wis_ability": 0,
            "int_ability": 0,
            "cha_ability": 0,
        }
        self.status = {
            "health": 0,
            "max_health": 0,
            "ac": 0,
            "poison": 0,
        }
        self.skills = {
            "attack": 1,
            "flee": 1,
            "defend": 0,
        }
        self.knownMonsters = ["slime"]

    def stat_reset(self):
        self.status = {
            "health": random.randint(1, 8) + self.stat_ability["con_ability"],
            "max_health": self.status["health"],
            "ac": 10 + self.stat_ability["dex_ability"],
            "poison": 0
        }
        self.skills = {
            "attack": 1,
            "flee": 1,
            "defend": 0,
        }

    def basic_combat(self, enemy):  # it should  take the player's info automatically and add it with a monster
        vowels = ["a", "e", "i", "o", "u"]
        if enemy.name[0:1] in vowels:  # grammar is good
            grammar = "an"
        else:
            grammar = "a"
        print(f'You have encountered {grammar} {enemy.name}!')

        while enemy.health or self.status["health"] > 0:  # loops till fight is over
            choice = combat_choice()  # lets you choose your next move

            if choice == "attack":
                enemy.health = basic_attack(self.stat_ability["str_ability"], enemy.ac, enemy.health)
                if enemy.health < 1:
                    print(f'You defeated the {enemy.name}')
                    return
                print(f'The {enemy.name} has {enemy.health} health left.')

            elif choice == "flee":
                escape = flee(self.stat_ability["dex_ability"], enemy.dex)
                if escape:
                    print(f'You escaped the {enemy.name}')
                    return
                else:
                    print("You failed to escape!")

            if self.status["poison"]:
                self.status["health"] = self.status["health"] - 1
                print("You took one poison damage!")
                self.status["poison"] -= 1

            if self.status["health"] < 1:
                print("You have died. Game over!")
                exit()

            print(f'The {enemy.name} attacks you!')
            self.status["health"], self.status["poison"] = enemy.combat_choice(self)  # goes into the enemy class
            print(f'You have {self.status["health"]} health left.')

            if self.status["health"] < 1:
                print("You have died. Game over!")
                exit()


def ability_modifier_maker():  # takes the numbers from stats and transforms them into ability modifiers.
    keys = []
    for key in player.stat_ability.keys():
        keys.append(key)
    values = []
    for value in player.stats.values():
        values.append(value)
    for v in range(len(values)):
        values[v] = (values[v] - 10) // 2
    for r in range(len(player.stat_ability)):
        player.stat_ability[keys[r]] = values[r]


def d20():  # a basic d20 that also tells for critical fails/successes.
    d20_roll = random.randint(1, 20)
    if d20_roll == 1:
        print("Critical fail!")
        return d20_roll
    elif d20_roll == 20:
        print("Critical success!")
        return d20_roll
    else:
        return d20_roll


def stat_saver():  # will save the player info to text files

    for name, lists in player.__dict__.items():
        if isinstance(lists, dict):  # checks to see if it is a dictionary to know to load it in  that way

            save = open(f'{name}.txt', "w")  # opens dict
            nl = "\n"

            for j in range(len(player.__dict__[name])):  # cycles however many entries are in loaded dict
                stat_items = []

                for value in (player.__dict__[name]).values():  # adds the values of said dict to a list
                    stat_items.append(value)
                value = stat_items[j]  # picks one specific value for a loop

                if j == len(player.__dict__[name]) - 1:  # gets rid of nl when last value
                    nl = ""
                save.write(f'{value}{nl}')  # saves one value on one line, then repeats till range is done
            save.close()

        elif isinstance(lists, list):  # does the same system but with lists
            nl = "\n"
            save = open(f'{name}.txt', "w+")  # loads dictionary

            for list_values in range(len(player.__dict__[name])):  # gets the number in the list so it can cycle
                if list_values == len(player.__dict__[name]) - 1:
                    nl = ""
                save.write(f'{lists[list_values]}{nl}')  # saves one line per cycle
            save.close()


def stat_roll():   # Rolls all the dice needed for one stat.
    dice1, dice2, dice3, dice4 = random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
    num = [dice1, dice2, dice3, dice4]
    num.sort()
    num.pop(0)
    total = 0
    for a in num:
        total += a
    return total


def stat_maker():
    st, d, c, w, i, ch = stat_roll(), stat_roll(), stat_roll(), stat_roll(), stat_roll(), stat_roll()
    raw_nums = [st, d, c, w, i, ch]
    empty = []
    print(f'{st}, {d}, {c}, {w}, {i}, and {ch} are your stats')

    for s in player.stats:
        a = "a"
        while a not in raw_nums:
            x_temp = input(f"What do you want to assign to {s}?\n")
            try:
                x_temp = int(x_temp)
                if x_temp not in raw_nums:
                    print("That's not an option!")
                else:
                    a = x_temp
                    player.stats[s] = a
            except ValueError:
                print("That's not an option!")
        raw_nums.remove(player.stats[s])
        if raw_nums != empty:
            print(raw_nums)

    ability_modifier_maker()  # creates rest of player stats
    player.knownMonsters.clear()
    player.knownMonsters.append("slime")
    player.stat_reset()


def loading_system():
    filed = open("stats.txt", "r+")
    file_tester = filed.read()

    if file_tester:
        dict_list = []
        list_list = []

        for name, lists in player.__dict__.items():
            if isinstance(lists, dict):  # checks to see if it is a dictionary to know to load it in  that way.
                dict_list.append(name)

                for dict_name in dict_list:  # cycles through dictionaries and opens their file
                    filer = open(f'{dict_name}.txt', "r+")
                    dict_file = filer.read()
                    dict_file = dict_file.split("\n")
                    dict_key = getattr(player, dict_name)
                    key_list = []
                    for key in dict_key:
                        key_list.append(key)

                    for j in range(len(dict_key)):  # will go for as many items there are in dictionary and load
                        key_list_final = key_list[j]
                        try:
                            player.__dict__[dict_name][key_list_final] = int(dict_file.pop(0))
                        except ValueError:
                            player.__dict__[dict_name][key_list_final] = (dict_file.pop(0))
                    filer.close()

            elif isinstance(lists, list):
                list_list.append(name)  # is used for lists instead of dictionaries. Way easier.
                player.knownMonsters.clear()

                for list_name in list_list:  # will go for as many list types are in player
                    filer = open(f'{list_name}.txt', "r+")
                    list_file = filer.read()
                    list_file = list_file.split("\n")

                    for item in list_file:  # will add as many items as are in the
                        player.__dict__[list_name].append(item)
                    filer.close()  # closes

        answer_options = ["yes", "no"]  # gives you the option to either load your stats or start from scratch.
        file_answer = 0
        print(f'Do you want to load your old save with stats:\n{player.stats} \nYes/No')
        while file_answer not in answer_options:
            x = input()
            if str.lower(x) in answer_options:
                file_answer = str.lower(x)
            else:
                print("please enter \'yes\' or \'no\'")

        if file_answer != "yes":
            stat_maker()  # new load out!
    else:
        stat_maker()  # new load out!


def basic_attack(mod, mod2, hp):  # calculates the damage and gives info to the player.
    d20roll = d20()
    attack_roll = d20roll + mod - mod2
    damage = (random.randint(1, 6) + mod)
    if d20roll == 1:
        return hp
    elif d20roll == 20:
        hp -= damage
        print(f"{damage} damage!")
        return hp
    elif attack_roll > 0:
        hp -= damage
        print(f"{damage} damage!")
        return hp
    else:
        print("Miss!")
        return hp


def combat_choice():  # A program to let player decide what move to do
    choices = []
    for keys, values in player.skills.items():  # takes all values in skills that are True and puts in list
        if values:
            choices.append(keys)
    choice = 0

    print(f'What do you want to do?\n')
    for x in choices:  # asks you what skill you want to use, if it isn't in your allowed skills it retries.
        print(x)
    while choice not in choices:
        choice = input()
        choice = choice.lower()
        if choice not in choices:
            print("Please choose a valid option.")
            for x in choices:
                print(x)

    return choice  # returns the choice so that other programs can use it


def flee(mod1, mod2):  # like basic attack, but with fleeing.
    d20roll = d20()
    escape_roll = (d20roll + mod1) - mod2

    if d20roll == 1:
        return False
    elif d20roll == 20:
        return True
    elif escape_roll > 0:
        return True


player = Player()
loading_system()

randMon = enemies.Monster(player.knownMonsters[0])
encounters.old_man(player, randMon)
print("")
random.shuffle(player.knownMonsters)
randMon = enemies.Monster(player.knownMonsters[0])
player.basic_combat(randMon)

# level = 1
# while player.status["health"] > 0:
#     level += 1
#     randMon = enemies.Monster("slime", level)
#     basic_combat(player, randMon)
stat_saver()

player.status.update(player.status)
