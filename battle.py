from os import write
import random
import json
from pokemon_class import Pokemon
from time import sleep
from colorama import Fore, Style

# turn counter
turn_count = 1

# battle loop used when battling with a computer or a second player
# first_party - player's party/first player's party
# second_party - computer's party/second player's party
# computer - 
def battle_main_loop(first_party, second_party, computer=True):
    # open file to delete all logs from log.txt file
    f = open("log.txt", "w")
    # show this to tell player the order of the pokemon in first turn
    show_enter_msg(first_party.get_first(), second_party.get_first())
    # this loop continues until either player or computer loses all pokemon
    while first_party and second_party:
        # current first pokemon in player's party
        curr1 = first_party.get_first()
        # current first pokemon in computer's party
        curr2 = second_party.get_first()
        # pokemon_returned - defeated pokemon
        if computer:
            # use fight_loop when playing against computer
            pokemon_returned = fight_loop(curr1, curr2, first_party, second_party)          
        else:
            # use fight_loop when playing against other player
            pokemon_returned = fight_loop_two_players(curr1, curr2, first_party, second_party)
            # check in which party defeated pokemon is
        if pokemon_returned in first_party:
            # message to display after the game ends
            if computer: msg = "The computer has won!"
            else: msg ="Second player has won!"
            # swap pokemons, remove defeated one from the party
            swap_pokemons(first_party) 
            first_party.remove_from_party(pokemon_returned)
            # if currently there are no pokemons in player party, end game
            if len(first_party) == 0:
                write_log(msg)
                return
        elif pokemon_returned in second_party:
            if computer:
                # remove defeated pokemon from the party
                second_party.remove_from_party(pokemon_returned)
                # if no pokemomons in a party, end game
                if len(second_party) == 0:
                    msg = "You won!"
                    write_log(msg)
                    return
                # else, computer swaps pokemons
                if len(second_party) > 1:
                    swap_computer(second_party)
            else:
                swap_pokemons(second_party)
                second_party.remove_from_party(pokemon_returned)
                # if no pokemomons in a party, end game
                if len(second_party) == 0:
                    msg = "First player has won!"
                    write_log(msg)
                    return

# fight loop used until either current pokemon (that are first in it's team's position) is defeated during battle with computer
# pok1 - first pokemon from player's party
# pok2 - first pokemon from computer's party
# player_party, com_party - player's and computer's parties
def fight_loop(pok1, pok2, player_party, com_party):
    global turn_count
    menu = "1 - normal attack\n2 - special attack\n3 - raise defense\n4 - swap pokemon"     # print menu
    while pok1._hp > 0 and pok2._hp > 0:
        print(f"{Fore.GREEN}---------------Turn {turn_count}---------------{Style.RESET_ALL}")
        write_log(f"---------------Turn {turn_count}---------------", False)
        # show opponent's pokemon
        opponent = f"The opposing pokemon is {pok2.name}!"
        # write log to a file
        write_log(opponent)
        # increment turn count
        turn_count += 1
        # let computer move first if it's pokemon is faster
        if pok2._speed > pok1._speed:
            # computer decides about its move
            computer_move(pok1, com_party)
            # get current first pokemon if computer switched pokemons
            pok2 = com_party.get_first()
            # if computer's pokemon attacks, check the health of player's current pokemon
            if pok1._hp <= 0: 
                return pok1
        print(menu)
        attack = f"{pok1.name} attacks!"
        write_log(attack)
        # let player attack
        player_move(pok2, player_party)
        # get player's current first pokemon if player switched pokemons
        pok1 = player_party.get_first()
        # if player attacked, check health of computer's current pokemon
        if pok2._hp <= 0:
            return pok2
        # pokemon moves now if it's current pokemon is slower than player's
        if pok2._speed < pok1._speed:
            computer_move(pok1, com_party)
            # get computer's current pokemon if switched
            pok2 = com_party.get_first()
            # if computer's pokemon attacks, check the health of player's current pokemon
            if pok1._hp <= 0:
                return pok1

# fight loop used until either current pokemon (that are first in it's team's position) is defeated during battle with another player
# pok1 - first pokemon from first player's party
# pok2 - first pokemon from second player's party
# first_party, second_party - first and second's players parties respectively
def fight_loop_two_players(pok1, pok2, first_party, second_party):
    global turn_count
    menu = "1 - normal attack\n2 - special attack\n3 - raise defense\n4 - swap pokemon"
    # get order of fighting pokemons
    order = compare_speeds(pok1, pok2)
    while order[0]._hp > 0 and order[1]._hp > 0:
        print(f"{Fore.GREEN}---------------Turn {turn_count}---------------{Style.RESET_ALL}")
        write_log(f"---------------Turn {turn_count}---------------", False)
        # party variable is used to get current player's turn
        # if first player moves first, party is set to first player's party 
        party = first_party
        # else, party variable is set to second player's party
        if order[0] in second_party:
            party = second_party
        # increment tour count
        turn_count += 1
        # temp_value variable is used to make sure that both player can move
        temp_value = 1
        # iterate twice and let both player move
        for i in range (0, 2):
            if i == 1: 
                temp_value = 0
                if party == first_party:
                    party = second_party
                else:
                    party = first_party
            # get current opponent for player that currently moves
            opponent = f"The opposing pokemon is {order[temp_value].name}!"
            write_log(opponent)
            # print menu
            print(menu)
            attack = f"{order[i].name} attacks!"
            write_log(attack)
            # player moves and chooses from the menu move choice
            player_move(order[temp_value], party)
            # swap current pokemon for the second one after previous player move
            order[i] = party.get_first()
            # if pokemon is defeated, return it
            if order[temp_value]._hp <= 0:
                return order[temp_value]

# print order of the pokemon in first turn
def show_enter_msg(pok1, pok2):
    global turn_count
    # increment tour count
    turn_count = 1
    # get order in which players will move
    order = compare_speeds(pok1, pok2)
    write_log(f"The first pokemon to strike is {order[0].name}. It has {order[0].hp()} HP.")
    write_log(f"The second pokemon to strike is {order[1].name}. It has {order[1].hp()} HP.")

# player moves
def player_move(pok2, player_party):
    # get current player's current pokemon
    pok1 = player_party.get_first()
    while True:
        try:
            # choose move from the menu option
            choice = int(input("Choose what you want to do: "))
            if choice == 1:
                # deal normal damage
                deal_normal_damage(pok1, pok2)
                break
            elif choice == 2:
                # deal special damage
                deal_special_damage(pok1, pok2)
                break
            elif choice == 3:
                # raise current pokemon's defense
                raise_defense(pok1)
                break
            elif choice == 4:
                if len(player_party) > 1:
                    # swap current player's pokemons
                    player_party = swap_pokemons(player_party)
                    pok1 = player_party.get_first()
                    break
                # special case - current player's party has only one pokemon
                else:
                    print("No available pokemons to swap!") # and choose again
        # exception handling
            else:
                print("Invalid choice!")
        except (ValueError):
            print("Enter a number!")

# computer chooses its move
def computer_move(pok1, com_party):
    # there is a loop, because there is a possibility of needing to randomise number again
    while True:
        choice = random.randint(1, 11)
        # computer uses normal attack
        if choice <= 3:
            write_log(f"{com_party.get_first()} used a normal attack")
            pok1.receive_normal_damage(com_party.get_first()._attack)
            break
        # computer chooses a type from current pokemon ones and uses special attack
        elif choice <= 6:
            write_log(f"{com_party.get_first()} used a special attack")
            computer_deal_special_damage(pok1, com_party.get_first())
            break
        # computer raises defense of its current pokemon
        elif choice <= 9:
            com_party.get_first().raise_defense()
            break
        # if computer has only one pokemon in its party, randomise again
        # else, computer swaps its pokemons randomly
        elif choice > 9 and len(com_party) > 1:
            swap_computer(com_party)
            write_log(f"Pokemon switched! The new opponent is {com_party.get_first()}!")
            break

# used in a GUI interface to choose computer's move
def computer_choose_move(com_party):
    choice = random.randint(1, 11)
    # normal attack
    if choice <= 3:
        return 1
    # special attack choose attack's type later
    elif choice <= 6:
        return 2
    # raise defense of current pokemon
    elif choice <= 9:
        return 3
    # swap pokemons
    elif choice > 9 and len(com_party) > 1:
        return 4
    # if computer has chosen to swap pokemons but has only one pokemon, randomise again (GUI does not allow other infinite loops)
    else: return computer_choose_move(com_party)

# compare 
def compare_speeds(pok1, pok2):
    if pok1.speed() > pok2.speed():
        return [pok1, pok2]
    elif pok1.speed() == pok2.speed():
        return random.sample([pok1, pok2], 2)
    else:
        return [pok2, pok1]

# second pokemon receives normal damage, without any multipliers
def deal_normal_damage(pok1, pok2):
    pok2.receive_normal_damage(pok1._attack)

# second pokemon receives special damage which damage depends on type effectiveness
def deal_special_damage(pok1, pok2):
    menu_choice = 0                     # move's type choice, there can only be available one or two move types
    move_type = ""
    print("Choose a type to attack with from ones below:")
    while menu_choice < len(pok1.types()):
        print(f'{str(menu_choice+1)}: {pok1.types()[menu_choice]}')          # print menu containing available move types 
        menu_choice += 1
    while(True):
        try:
            # choose move's type
            choice = int(input("Type choosen: "))
            if choice >= 1 and choice <= len(pok1.types()):
                move_type = pok1.types()[choice-1]
                multiplier = get_attack_multiplier(move_type, pok2)          # get attack's multiplier
                # attacked pokemon is immune to choosen move type
                if multiplier == 0:
                    write_log(f'{pok1.name} attacked, but the move had no effect on {pok2.name}!')
                    break
                # attacked pokemon resists (but is not immune to) choosen move type
                elif multiplier < 1:
                    write_log(f'{pok1.name} attacked!\nIt\'s not very effective against opposing {pok2.name}!')
                # attacked pokemon is weak to choosen move type
                elif multiplier >= 2:
                    write_log(f'{pok1.name} attacked {pok2.name}!\nIt was super effective!')
                # attacked pokemon does not resist nor is weak to choosen move type
                pok2.receive_special_damage(pok1._attack*multiplier)
                break
        # exception handling
            else:
                print("Incorrect type!")
        except (ValueError):
            print("Enter a number!")
            continue

# computer used special attack
def computer_deal_special_damage(pok1, pok2):
    # choose move_type randomly from pokemon's ones
    move_type = random.choice(pok2.types())
    # get attack's multiplier
    multiplier = get_attack_multiplier(move_type, pok1)
    write_log(f"{pok2.name}'s has used {move_type} type.")
    # pokemon attacked is immune to choosen type
    if multiplier == 0:
        write_log(f'{pok2.name} attacked, but the move had no effect on {pok1.name}!')
    # pokemon attacked resists (but is not immune to) choosen type
    elif multiplier < 1:
        write_log(f'{pok2.name} attacked!\nIt\'s not very effective against opposing {pok1.name}!')
    # pokemon attacked is weak to choosen type
    elif multiplier >= 2:
        write_log(f'{pok2.name} attacked {pok1.name}!\nIt was super effective!')
    # pokemon attacked does not resist nor is weak to choosen type
    pok1.receive_special_damage(pok2._attack*multiplier)

# get attack's multiplier
# move_type - used type of the special attack
# pokemon_attacked - attacked pokemon which types are used during multiplier calculation
def get_attack_multiplier(move_type, pokemon_attacked):
    # get each type strength, weaknesses and immunities
    with open('typings.json') as types:
        data = json.load(types)
    # set multiplier to 1
    multiplier = 1
    typ1 = {}
    typ2 = {}
    # get attacked pokemon's types
    for typing in data:
        if typing['Name'] == pokemon_attacked._types[0]:
            typ1 = typing
            break
    # set multiplier to 0 if pokemon is immune to that move type
    if 'Immunities' in typ1 and move_type in typ1['Immunities']:
        multiplier = 0
    # halve multiplier if pokemon resists that move type
    elif 'Resistances' in typ1 and move_type in typ1['Resistances']:
        multiplier *= 0.5
    # double multiplier if pokemon is weak to that type
    elif 'Weaknesses' in typ1 and move_type in typ1['Weaknesses']:
        multiplier *= 2
    # do the same for attacked pokemon's second type (if it has second type)
    if len(pokemon_attacked._types) == 2:
        for typing in data:
            if typing['Name'] == pokemon_attacked._types[1]:
                typ2 = typing
                break
    if 'Immunities' in typ2 and move_type in typ2['Immunities']:
        multiplier = 0
    elif 'Resistances' in typ2 and move_type in typ2['Resistances']:
        multiplier *= 0.5
    elif 'Weaknesses' in typ2 and move_type in typ2['Weaknesses']:
        multiplier *= 2
    # special case, this pokemon works differently than other ones due to it's 1hp gimmick
    if pokemon_attacked.name == "Shedinja":
        # if move type is one listed below, multiplier is set to 0
        if move_type not in ["Fire", "Ghost", "Flying", "Dark", "Rock"]:
            multiplier = 0
    return multiplier

# raise pokemon's defense
def raise_defense(pok):
    pok.raise_defense()

# player swaps pokemons
def swap_pokemons(party):
    # if there is only one pokemon in a party, do nothing because we can't swap pokemons
    if len(party) == 1:
        return party
    menu = "Choose a pokemon to swap:"
    print(menu)
    party_amount = len(party)
    # print available pokemons to swap
    for i in range (1, party_amount):
        print(f'{i} - {party.get_pokemon(i)}')
    while True:
        try:
            # choose pokemon to swap
            choice = int(input("Pokemon chosen: "))
            if choice >= 1 and choice <= len(party)-1:
                party.swap_pokemons(0, choice)
                write_log(f'Pokemon swapped! Go {party.get_first().name}!')
                return party
        # exception handling
            else:
                print("Invalid choice")
        except (ValueError):
            print("Enter a number")

# swap computer's pokemons
def swap_computer(party):
    party_amount = len(party)
    # get swapped pokemon's index
    swapped = random.randint(1, party_amount-1)
    party.swap_pokemons(0, swapped)
    return party.get_first()

# write log to a file
def write_log(text, print_text=True):
    # append mode, we don't want to delete file's content
    f = open("log.txt", "a")
    # if print_text == True, print the text to the terminal's console
    if print_text:
        print(text)
    f.write(text+'\n')
    f.close()