from random import randint
from colorama import Fore, Style

class Pokemon:
    def __init__(self, name, hp, attack, defense, special_attack, special_defense, speed, ID, *types):
        self.name = name.capitalize()
        if self.name == "Shedinja":                        # special case, this pokemon has hard-coded 1 hp
            self._max_hp = 1
            self._base_hp = 1
            self._hp = 1
        else:
            self._base_hp = hp                             # also constant that is never changed, containt hp value before any modifiers
            self._max_hp = 2*hp + 110 + randint(0, 15)     # constant, this one will never be changed
            self._hp = self._max_hp                        # hp stat is equal to this formula: 2*base hp (hp is a paramether) + 110 + random value
        self._attack = attack                              # attack stat value
        self._defense = defense                            # defense stat value (changed during battle)
        self._base_defense = defense                       # base defense contains a value of base defense, constant 
        self._special_attack = special_attack              # special attack stat value
        self._special_defense = special_defense            # special defense stat value
        self._base_spdefense = special_defense             # base special defense contains a value of base special defense, constant
        self._boost_defense = 0.25 * self._defense         # constant, pokemon boosts its defense by this value
        self._boost_spdefense = 0.25 * self._special_defense  # another constant, pokemon boosts its special defense by this value
        self._speed = speed                                # speed stat value
        self.id = ID                                       # pokemon's id number
        self._types = types[0]                             # container that stores pokemon's types

    # getters

    def name(self):
        return self.name

    def id(self):
        return self._id

    def hp(self):
        return self._hp

    def base_hp(self):
        return self._base_hp

    def max_hp(self):
        return self._max_hp

    def types(self):
        return self._types

    def attack(self):
        return self._attack

    def defense(self):
        return self._defense

    def special_attack(self):
        return self._special_attack

    def special_defense(self):
        return self._special_defense

    def speed(self):
        return self._speed

    # return pokemon's types
    def print_types(self):
        new_types = list(self._types)
        return new_types

    # this method is called when pokemon is dealt damage (dmg) by a normal attack
    def receive_normal_damage(self, dmg):
        # if pokemons was dealt no damage, receive no damage
        if dmg == 0:
            self._hp -= 0
        else:
            dmg = int(40*(dmg/self._defense)*randint(85, 115)/100)          # formula used to calculate damage taken (based on real games)
            crit_chance = randint(0, 100)                                   # get crit chance, there is 4% chance for a hit to be critical
            if crit_chance < 5:
                print(Fore.YELLOW + "A critical hit!", Style.RESET_ALL)
                self.write_log("A critical hit!", False)
                dmg = int(dmg*1.5)                                          # multiply damage received by 1.5
            dmg = max(dmg, 1)                                               # deal at least one damage
            self._hp -= dmg                                                 # receive damage
        if max(self._hp, 0) == self._hp:                                    # check if pokemon was defeated
            print(f"Pokemon {self.name} has received {dmg} damage.")        # if not, show remaining hp
            self.show_remaining_HP()
            return self._hp
        else:                                                               # if defeated, remove it from the team
            self._hp = 0
            self.write_log(f"Pokemon {self.name} was dealt {dmg} damage and has passed out! It is unable to battle again!")
            self.delete()

    # this method is called when pokemon is dealt damage (dmg) by a special attack
    def receive_special_damage(self, dmg):
        # if pokemons was dealt no damage, receive no damage
        if dmg == 0:
            self._hp -= 0
        else:
            # formula used to calculate damage taken (based on real games, including same-type-attack-bonus)
            dmg = int(1.2*40*(dmg/self._special_defense)*randint(85, 115)/100)
            crit_chance = randint(0, 100)
            if crit_chance < 5:                                             # get crit chance, there is 4% chance for a hit to be critical
                print(Fore.YELLOW + "A critical hit!", Style.RESET_ALL)
                self.write_log("A critical hit!", False)
                dmg = int(dmg*1.5)                                          # multiply damage received by 1.5
            dmg = max(dmg, 1)                                               # deal at least one damage
            self._hp -= dmg                                                 # receive damage  
        if max(self._hp, 0) == self._hp:                                    # check if pokemon was defeated
            print(f"Pokemon {self.name} has received {dmg} damage.")        # if not, show remaining hp
            self.show_remaining_HP()
            return self._hp
        else:                                                               # if defeated, remove it from the team
            self._hp = 0
            self.write_log(f"Pokemon {self.name} was dealt {dmg} damage and has passed out! It is unable to battle again!")
            self.delete()

    # raise pokemon's defense
    def raise_defense(self):
        self.write_log(f'{self.name} has raised it\'s defense!', False)
        self._defense = int(self._defense + self._boost_defense)            # boosted defense
        self._special_defense = int(self._special_defense + self._boost_spdefense)      # boosted special defense     

    # reset defense and special defense stats to base values
    def reset_stat_changes(self):
        self._defense = self._base_defense
        self._special_defense = self._base_spdefense

    # show remaining pokemon's HP
    def show_remaining_HP(self):
        print(f"Remaining {self.name}'s HP: {self._hp}/{self._max_hp}")

    # write to a log file what was happening during the battle
    def write_log(self, text, print_text=True):
        f = open("log.txt", "a")
        if print_text:
            print(text)
        f.write(text+'\n')
        f.close()

    # delete a pokemons
    def delete(self):
        del self

    # define __str__ special method
    def __str__(self):
        pokemon_data = f"{self.name}"
        return pokemon_data
