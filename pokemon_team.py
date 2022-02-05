from pokemon_class import Pokemon

class PokemonTeam():
    def __init__(self, party=None):
        if party is None:
            self._party = []                # create empty party
        else:
            for pokemon in party:
                if not isinstance(pokemon, Pokemon):    # if any pokemon in a party is not a Pokemon class object, create empty party
                    self._party = []
                    break
            self._party = party                         # else, create party with given pokemon
        self._amount = len(self._party)                 # store amount of pokemons

    # getters

    def get_party(self):
        return self._party

    def get_amount(self):
        return self._amount

    def get_first(self):
        return self._party[0]

    def get_pokemon(self, position):
        return self._party[position]

    # add a pokemon to a party
    def add_to_party(self, pokemon):
        if isinstance(pokemon, Pokemon):                # check if it's a Pokemon object
            self._party.append(pokemon)                 # add a pokemon to the party
            self._amount += 1                           # increment self._amount attribute
        return self._party

    # remove a pokemon from a party
    def remove_from_party(self, pokemon):
        if isinstance(pokemon, Pokemon):                # check if it's a Pokemon object
            self._party.remove(pokemon)                 # remove a pokemon from the party
            self._amount -= 1                           # decrement self._amount attribute
        return self._party

    # swap pokemons in a party
    def swap_pokemons(self, pos1, pos2):
        # reset both pokemon's defense and special defense stat raises
        self._party[pos1].reset_stat_changes()
        self._party[pos2].reset_stat_changes()
        # swap pokemons in a list
        self._party[pos1], self._party[pos2] = self._party[pos2], self._party[pos1]
        return self._party

    # show pokemon party
    def show_party(self):
        repr = ""
        for pokemon in self._party:
            repr += str(pokemon) + " "
        return repr

    # define __bool__ attribute to return True if there is any pokemon in a party
    def __bool__(self):
        if self._amount == 0:
            return False
        return True

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self._amount:
            result = self._party[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    # define __len__ attribute to get length of the pokemon team
    def __len__(self):
        return self._amount

    # define __str__ attribute to make it possible to print pokemons in a party
    def __str__(self):
        repr = ""
        for pokemon in self._party:
            repr += str(pokemon) + " "
        return repr