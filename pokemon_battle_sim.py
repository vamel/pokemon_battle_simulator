from pokemon_class import Pokemon
from pokemon_team import PokemonTeam
from battle import battle_main_loop
from colorama import Fore, Style
import json
import random
from sys import exit


def make_pokemon(pokemon):
    # create Pokemon class object from given data 
    # first, read data from json file containing all pokemons and their statistics
    pokemon_name = pokemon['Name']
    types = pokemon['Types']
    hp = pokemon['HP']
    attack = pokemon['Attack']
    defense = pokemon['Defense']
    special_attack = pokemon['Special Attack']
    special_defense = pokemon['Special Defense']
    speed = pokemon['Speed']
    ID = pokemon['ID']
    # now, create Pokemon class object
    pokemon_as_a_class = Pokemon(pokemon_name, hp, attack, defense, special_attack, special_defense, speed, ID, types)
    # and return it
    return pokemon_as_a_class

# get all pokemons' names from json file containing pokemons' stats
def get_pokedex():
    # list containing all pokemons names
    pokedex = []
    # open json file
    with open('pokemon.json', 'r') as file_handle:
        pokemons = json.load(file_handle)
        # add name of every pokemon to the list
        for entry in pokemons:
            name = entry["Name"]
            pokedex.append(name)
    # and return this list
    return pokedex

# choose pokemons that will be used during simulation
def choose_your_pokemons():
    # get every pokemon name
    pokedex = get_pokedex()
    # create empty party to which pokemons will be added
    player_party = PokemonTeam()
    # create empty list that will contain only pokemons' names
    player_pokemons = []
    while (True):
        try:
            # enter amount of pokemons that will be in a team controlled by player
            amount = int(input("Choose an amount of pokemons. You can choose between 1 and 6 pokemons: "))
            break
        # exception handling
        except (ValueError):
            print("Invalid value.")
    temp_amount = amount
    while temp_amount > 0:
        # player enters names of pokemons he/she wants to use, entries like pIKACHU, Pikachu, pikachu, PIKACHU, etc. will yield exact same result
        pokemon_choosen = input('Choose a pokemon: ')
        # player entered name of non-existent pokemon
        if pokemon_choosen.title() not in pokedex:
            print("Unknown pokemon! Choose a known one!")
            continue
        # player entered name of existing pokemon, but it already is in player's party
        elif pokemon_choosen.title() in player_pokemons:
            print("You have choosen this pokemon already! You can\'t have two of the same ones in your party.")
            continue
        # if player entered name of existing pokemon and has not chosen it before, add it to the party
        else:
            player_party.add_to_party(choose_a_pokemon(pokemon_choosen.title()))
            player_pokemons.append(pokemon_choosen.title())
            temp_amount -= 1
    # return party created by the player
    return player_party

# open json file containing all pokemon data
def open_json_file():
    with open('pokemon.json', 'r') as database:
        data = json.load(database)
    return data

# choose a pokemon and add it to the party
def choose_a_pokemon(choice):
    database = open_json_file()
    pokem = next(poke for poke in database if poke['Name'] == choice)
    # choosen pokemon name is used to create Pokemon object based on entered name
    Choosen_pokemon = make_pokemon(pokem)
    return Choosen_pokemon

# show all names of the pokemon that are currently in player's party
def show_player_pokemons(party):
    for pokemon in party:
        print(pokemon)

# after choosing all pokemons, start the battle with computer
def battle_menu(player_party, computer_party, computer=True):
    winner = battle_main_loop(player_party, computer_party, computer)
    return winner

# menu where player chooses all pokemons
def choice_menu():
    print("\nOkay, so now you have to choose pokemons!")
    # choose pokemons
    player_party = choose_your_pokemons()
    print("\nThese are your pokemons: ")
    # show all pokemons choosen by player
    show_player_pokemons(player_party)
    # computer will choose the same amount of pokemon that player has chosen
    print("\nComputer will choose the same amount of pokemons.")
    # computer chooses its pokemons randomly
    computer_pokemons = random.sample(get_pokedex(), player_party.get_amount())
    computer = []
    for mon in computer_pokemons:
        computer.append(choose_a_pokemon(mon))
    print("The computer has chosen these pokemons: ")
    # show pokemons choosen by the computer
    show_player_pokemons(computer)
    computer_party = PokemonTeam(computer)
    # start the battle in which player fights with a computer
    winner = battle_menu(player_party, computer_party)
    return winner

# menu where both player choose their pokemons, order of choosing does not affect the order in which both players move
def choice_menu_two_players():
    # firstly, let the first player choose pokemons
    print("\nOkay, so now you have to choose pokemons!")
    player_party1 = choose_your_pokemons()
    # secondly, let the second player choose their pokemons
    print("\nNow second player will choose pokemons!")
    player_party2 = choose_your_pokemons()
    # print both players' pokemons
    print("\nThese are first player's pokemons: ")
    show_player_pokemons(player_party1)
    print("\n\nThese are second player's pokemons: ")
    show_player_pokemons(player_party2)
    # start the battle in which two players fight
    winner = battle_menu(player_party1, player_party2, False)
    return winner

# show pokemon stats in a terminal
def show_pokemon_stats():
    print("\nHere you can see stats of your pokemon.")
    pokedex = get_pokedex()
    while(True):
        # enter name of pokemon which stats we want to see
        poke_name = input("Enter the name of pokemon you want to see: ")
        if poke_name.title() in pokedex:
            pokemon = choose_a_pokemon(poke_name.title())
            print("\nThese are stats of your chosen pokemon:")
            print(f'{Fore.CYAN}Name{Style.RESET_ALL}: {pokemon.name}')
            print(f'{Fore.MAGENTA}Typing{Style.RESET_ALL}: {pokemon.print_types()}')
            print(f'{Fore.RED}HP{Style.RESET_ALL}: {pokemon._hp}')
            print(f'{Fore.BLUE}Attack{Style.RESET_ALL}: {pokemon._attack}')
            print(f'{Fore.GREEN}Defense{Style.RESET_ALL}: {pokemon._defense}')
            print(f'{Fore.BLUE}Special Attack{Style.RESET_ALL}: {pokemon._special_attack}')
            print(f'{Fore.GREEN}Special Defense{Style.RESET_ALL}: {pokemon._special_defense}')
            print(f'{Fore.YELLOW}Speed{Style.RESET_ALL}: {pokemon._speed}')
            break
        # if player enters incorrent pokemon's name, let the player enter the name again
        else:
            print("Incorrect pokemon's name. Try again.")

# show stats of choosen pokemon in GUI
def gui_pokemon_stats(poke_name):
    stats = ""
    pokemon = choose_a_pokemon(poke_name.title())
    stats += f'Name: {pokemon.name}\nTyping: {pokemon.print_types()}\nHP: {pokemon._base_hp}\nAttack: {pokemon._attack}\nDefense: {pokemon._defense}\n'
    stats += f'Special Attack: {pokemon._special_attack}\nSpecial Defense: {pokemon._special_defense}\nSpeed: {pokemon._speed}' 
    return stats

# player decide about returning to main menu
def play_again():
    print("Do you want to play again?")
    decision = str(input("Enter Y or Yes if you want to: "))
    if decision.upper() not in ["Y", "YES"]:
        print("Simulation ended.")
        exit()

# main menu, where players can choose what they want to do
def main_menu():
    menu_text = '''
    Welcome to our Pokemon Battle Simulator!
    You can play against randomised pokemon team.
    Below you can see available options:
    0 - Exit the game
    1 - Play against computer
    2 - Play against other player locally
    3 - Show pokemon stats
    '''
    while True:
        # choose a menu option
        print(menu_text)
        choice = input("Choose an option: ")
        if choice == "0":
            # end simulation
            print("Simulation ended.")
            exit()
        elif choice == "1":
            # battle against computer
            winner = choice_menu()
            # show who has won, computer or the player
            print(winner)
            play_again()
        elif choice == "2":
            # battle against other player
            winner = choice_menu_two_players()
            # show which player has won
            print(winner)
            play_again()
        elif choice == "3":
            # choose a pokemon and show its stats
            show_pokemon_stats()
        else:
            # exception handling
            print("Invalid option!")

def main():
    main_menu()

if __name__ == "__main__":
    main()