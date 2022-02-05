import tkinter as tk
from random import sample, randint, choice
from datetime import date
from pokemon_battle_sim import get_pokedex, gui_pokemon_stats, choose_a_pokemon
from battle import compare_speeds, computer_move, raise_defense, write_log, computer_choose_move, get_attack_multiplier
from pokemon_class import Pokemon
from pokemon_team import PokemonTeam
from statshower import StatShower


# window with fight against computer
# first_party - player's party
# second_party - computer's party
class ComGame(StatShower):
    def __init__(self):
        self.log_file_name = self.get_file_name()
        self.gamewindow = tk.Toplevel()
        # set name and size of the window
        self.gamewindow.title("Game against computer")
        self.gamewindow.geometry("800x585")
        # turn counter
        self.turn = 1
        # amount of pokemons in player's party
        self.first_amount = 0
        # create empty player's party
        self.first_party = PokemonTeam()
        # list containing player's pokemons names, it is used in a menu where player can choose a pokemon to swap
        self.first_list = []
        # create empty computer's party
        self.second_party = PokemonTeam()
        # create a checkbox that allows the player to choose amount of pokemon in their party
        self.create_amount_checkbox()
        # run the window until closed
        self.gamewindow.mainloop()

    # create listbox that lets the player to choose pokemon  that will be added to player's party
    def create_listbox(self):
        # get list with all pokemon names sorted alphabetically
        self.pokemons = sorted(get_pokedex())
        # create a text widget where all pokemon info will be shown
        self.txt = tk.Text(self.gamewindow, height=34, width=80)
        self.txt.place(x=0, y=0)
        self.txt.insert(tk.END, "Here are your pokemons:\n")
        # create listbox widget containing all pokemon names
        self.listbox = tk.Listbox(self.gamewindow, height=31, width=17)
        self.insert_pokemons()
        # after doubleclicking on a pokemon name, add it to the player party
        self.listbox.bind('<Double-1>', self.insert_to_party)
        self.listbox.place(x=646, y=24)
        # create scrollbar to help navigate through the listbox
        self.scrollbar = tk.Scrollbar(self.gamewindow, orient='vertical', command=self.listbox.yview)
        self.scrollbar.pack(side='right', fill='y')
        # create search bar to help find pokemons
        self.create_search_bar()
        self.listbox.config(yscrollcommand=self.scrollbar.set)

    # creating search bar that will help user enter correct pokemons
    def create_search_bar(self):
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(self.gamewindow, textvariable=self.search_var, width=17)
        self.entry.place(x=646, y=0)

    # update list when searching for a pokemon
    def update_list(self, *args):
        search_term = self.search_var.get()
        # delete all elements in a list
        self.listbox.delete(0, tk.END)
        for item in self.pokemons:
                # insert the pokemon name if it matches entered string
                if search_term.title() in item.title():
                    self.listbox.insert(tk.END, item)        

    # insert a pokemon to the party
    def insert_to_party(self, evt):
        if len(self.first_party) < self.first_amount:
            # get the pokemon name from the doubleclick event
            value=str((self.listbox.get(tk.ACTIVE)))
            # if pokemon is not at the party, add it, else do nothing
            if value not in self.first_list:
                self.first_party.add_to_party(choose_a_pokemon(value))
                self.first_list.append(value)
                self.txt.insert(tk.END, f'{len(self.first_party)}: {value}\n')
            # after all pokemons have been chosen, computer chooses randomly the same amount of pokemons
            if len(self.first_party) == self.first_amount:
                temp = sample(get_pokedex(), self.first_amount)
                for pokemon in temp:
                    self.second_party.add_to_party(choose_a_pokemon(pokemon))
                # show both player's and computer's parties
                self.txt.insert(tk.END, "\n\nThese are computer's pokemons:\n")
                for i in range(1, self.first_amount+1):
                    self.txt.insert(tk.END, f'{i}: {temp[i-1]}\n')
                # after 5 seconds, continue the game
                self.gamewindow.after(5000, self.create_battle)

    # destroy all current widgets in a window and create battle interface
    def create_battle(self):
        self.txt.destroy()
        self.listbox.destroy()
        self.scrollbar.destroy()
        # create text widget where all informations about battle are shown
        self.txt = tk.Text(self.gamewindow, height = 25, width = 99)
        self.txt.place(x=0, y=0)
        # get order in which player and computer move in the first turn
        self.get_order(self.first_party.get_first(), self.second_party.get_first())
        # create buttons that allow the player to move
        self.create_battle_buttons()

    # write current turn number
    def write_turn(self):
        self.turn += 1
        self.write(f"---------------Turn {self.turn}---------------")

    # player uses normal attack
    # pok1 - current player's pokemon
    # pok2 - current computer's pokemon
    # temp_hp1/temp_hp2 - stores value of current pokemons' hp value, used to calculate damage dealt
    def player_normal_attack(self):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        temp_hp1 = pok1.hp()
        temp_hp2 = pok2.hp()
        # get order in which computer and player move
        self.order = compare_speeds(pok1, pok2)
        # player moves first
        if pok1 == self.order[0]:
            # computer's current pokemon receives damage
            self.write(f'{pok1.name} used normal attack!')
            pok2.receive_normal_damage(pok1.attack())
            # if it survives, computer now moves
            if pok2.hp() > 0:
                self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
                self.computer_move()
                # if after computer move, the player's pokemon is defeated, force the player to switch pokemon
                if pok1.hp() <= 0:
                    # however if the player had only one pokemon, end game instead
                    if len(self.first_party) == 1:
                        self.show_winner("computer")
                        return
                    self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                    self.force_player_swap()
            else:
                # if after player's move computer's current pokemon is defeated, force computer to swap
                self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                # if computer had only one pokemon, end game instead
                if len(self.second_party) == 1:
                    self.show_winner("player")
                    return
                self.computer_swap()
                self.second_party.remove_from_party(pok2)
        # computer moves first
        else:
            self.computer_move()
            # get current computer's pokemon again, because it could swap pokemons
            pok2 = self.second_party.get_first()
            temp_hp2 = pok2.hp()
            # if player's pokemon survives, let it attack computer's pokemon
            if pok1.hp() > 0:
                self.write(f'{pok1.name} used normal attack!')
                pok2.receive_normal_damage(pok1.attack())
                # if computer's pokemon is defeated, force computer to swap
                if pok2.hp() <= 0:
                    self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                    # unless computer has only one pokemon, in that case just end the battle
                    if len(self.second_party) == 1:
                        self.show_winner("player")
                        return
                    self.computer_swap()
                    self.second_party.remove_from_party(pok2)
                else:
                    self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                    self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
            # computer's pokemon has defated current player's pokemon
            else:
                # if player has only one pokemon, end battle
                if len(self.first_party) == 1:
                    self.show_winner("computer")
                    return
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                self.force_player_swap()
        self.write_turn()

    # player uses special attack, this function works similarly to deal normal attack, but takes pokemons types into account
    # pok1 - current player's pokemon
    # pok2 - current computer's pokemon
    # temp_hp1/temp_hp2 - stores value of current pokemons' hp value, used to calculate damage dealt
    # move_type - move's type choosen by the player
    def player_special_attack(self, evt):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        move_type = self.tktypes.get()
        temp_hp1 = pok1.hp()
        temp_hp2 = pok2.hp()
        # get order in which computer and player move
        self.order = compare_speeds(pok1, pok2)
        # player attacks first
        if pok1 == self.order[0]:
            self.write(f'{pok1.name} used special {move_type} attack!')
            # get the multiplier used during damage calculation and write it to the text widget
            multiplier = get_attack_multiplier(move_type, pok2)
            self.write_dmg_mltp(pok1, pok2, multiplier)
            pok2.receive_special_damage(pok1.special_attack()*multiplier)
            # if computer's pokemon survives, let it move
            if pok2.hp() > 0:
                self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
                self.computer_move()
                # if computer's pokemon defeats player's pokemon, force player to swap pokemons
                if pok1.hp() <= 0:
                    # if player only has one pokemon, end the battle
                    if len(self.first_party) == 1:
                        self.show_winner("computer")
                        return
                    self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                    self.force_player_swap()
            # if player defeats computer's pokemon, force the computer to swap pokemons if it has more than 2 pokemons
            # if it has only one, end the batle
            else:
                self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                if len(self.second_party) == 1:
                    self.show_winner("player")
                    return
                self.computer_swap()
                self.second_party.remove_from_party(pok2)
        # computer moves first
        else:
            self.computer_move()
            pok2 = self.second_party.get_first()
            temp_hp2 = pok2.hp()
            # if player's pokemon survives, it attacks
            if pok1.hp() > 0:
                self.write(f'{pok1.name} used special {move_type} attack!')
                multiplier = get_attack_multiplier(move_type, pok2)
                self.write_dmg_mltp(pok1, pok2, multiplier)
                pok2.receive_special_damage(pok1.special_attack()*multiplier)
                # if it defeats computer's pokemon, force it to swap pokemons
                if pok2.hp() <= 0:
                    self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                    if len(self.second_party) == 1:
                        self.show_winner("player")
                        return
                    self.computer_swap()
                    self.second_party.remove_from_party(pok2)
                else:
                    self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                    self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
            # if player's pokemon is defeated, force player to swap pokemons unless player has only one pokemon
            else:
                if len(self.first_party) == 1:
                    self.show_winner("computer")
                    return
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                self.force_player_swap()
        self.write_turn()

    # method that writes message to the text widget according to special damage multiplier
    def write_dmg_mltp(self, pok1, pok2, mltpr):
        if mltpr == 0:
            self.write(f'{pok1.name} attacked, but the move had no effect on {pok2.name}!')
        elif mltpr < 1:
            self.write(f'It\'s not very effective against opposing {pok2.name}!')
        elif mltpr >= 2:
            self.write(f'It was super effective!')

    # raise player's pokemon's defense
    # pok1 - current player's pokemon
    # pok2 - current computer's pokemon
    # temp_hp1 - stores value of current player's pokemon's hp value, used to calculate damage dealt
    def player_raise_defense(self):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        temp_hp1 = pok1.hp()
        # get order of move
        self.order = compare_speeds(pok1, pok2)
        if pok1 == self.order[0]:
            # raise pokemon's defense
            pok1.raise_defense()
            self.write(f'{pok1.name} has raised it\'s defense!', False)
            # let computer move and force player to swap pokemons or end game if computer defeats player's pokemon
            self.computer_move()
            if pok1.hp() <= 0:
                if len(self.first_party) == 1:
                    self.show_winner("computer")
                    return
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                self.force_player_swap()
        # if computer moves first, check if it defeats player's pokemon
        else:
            self.computer_move()
            pok2 = self.second_party.get_first()
            if pok1.hp() > 0:
                pok1.raise_defense()
                self.write(f'{pok1.name} has raised it\'s defense!', False)
            # if it does, force player to swap or end the game
            else:
                if len(self.first_party) == 1:
                    self.show_winner("computer")
                    return
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                self.force_player_swap()
        self.write_turn()

    # player swaps pokemons
    def player_swap(self, evt):
        # firstly, check if player has only one pokemon
        if len(self.first_party) == 1:
            self.write("No pokemon to swap!", False)
        else:
            name = self.tkvarq.get()
            index = self.first_list.index(name)
            pok1 = self.first_party.get_first()
            pok2 = self.second_party.get_first()
            # get order in which player and computer will move
            self.order = compare_speeds(pok1, pok2)
            if pok1 == self.order[0]:
                # swap pokemons in player's party and player's party list
                self.first_party.swap_pokemons(0, index)
                self.first_list[0], self.first_list[index] = self.first_list[index], self.first_list[0]
                self.write(f'Pokemon swapped! Go {self.first_party.get_first().name}!')
                pok1 = self.first_party.get_first()
                self.update_swap_menu()
                # computer moves, if it defeats player, end game or force player to swap
                self.computer_move()
                if pok1.hp() <= 0:
                    if len(self.first_party) == 1:
                        self.show_winner("computer")
                        return
                    self.force_player_swap()
            else:
                # computer moves, if it does not defeat player's pokemon, let player switch pokemons
                self.computer_move()
                pok2 = self.second_party.get_first()
                # if it does defeat player's pokemons, player is forced to swap anyway
                if pok1.hp() <= 0:
                    if len(self.first_party) == 1:
                        self.show_winner("computer")
                        return
                    self.force_player_swap()
                else:
                    self.first_party.swap_pokemons(0, index)
                    self.first_list[0], self.first_list[index] = self.first_list[index], self.first_list[0]
                    self.write(f'Pokemon swapped! Go {self.first_party.get_first().name}!')
                    pok1 = self.first_party.get_first()
                    self.update_swap_menu()
        self.write_turn()

    # destroy buttons and create new menu where player is forced to choose a pokemon as a new current pokemon
    def force_player_swap(self):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        # if player has only one pokemon, it is game over
        if len(self.first_list) > 1:
            del self.first_list[0]
            self.tkvarq.set("Swap pokemon")
            self.forced_button = tk.OptionMenu(self.gamewindow, self.tkvarq, *self.first_list, command=self.forced_swap)
            self.forced_button.config(width=19)
            self.forced_button.place(x=300, y=500)

    # player's choosen pokemon becomes his new current pokemon
    def forced_swap(self, evt):
        name = self.tkvarq.get()
        # get defeated pokemon
        removed = self.first_party.get_pokemon(0)
        # get index of pokemon the player wants to swap
        index = self.first_list.index(name)
        self.first_party.swap_pokemons(0, index+1)
        # remove defeated pokemon from the party
        self.first_party.remove_from_party(removed)
        # destroy forced swap list and restore buttons to previous state
        self.forced_button.destroy()
        self.write(f'Pokemon swapped! Go {self.first_party.get_first().name}!')
        self.update_forced_swap_menu()
        self.create_battle_buttons()

    # update list of pokemons available to swap
    def update_forced_swap_menu(self):
        self.first_list.clear()
        self.first_list = [pokemon.name for pokemon in self.first_party]

    # update swap button and list of pokemons available to swap after hovering over the swap button
    def update_swap_menu(self):
        self.button4.destroy()
        self.tkvarq.set("Swap pokemon")
        party = self.first_list.copy()
        if len(party) > 1:
            del party[0]
            self.button4 = tk.OptionMenu(self.gamewindow, self.tkvarq, *party, command=self.player_swap)
            self.button4.config(width=19)
        else:
            self.button4 = tk.Button(self.gamewindow, text="No pokemon to swap!", width=19)
        self.button4.place(x=600, y=500)
        # update special attack button with types of current pokemon
        self.button2.destroy()
        self.tktypes.set("Special attack")
        self.button2 = tk.OptionMenu(self.gamewindow, self.tktypes, *self.first_party.get_first().types(), command=self.player_special_attack)
        self.button2.config(width=19)
        self.button2.place(x=200, y=500)

    # method that lets computer choose its move randomly
    def computer_move(self):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        move = computer_choose_move(self.second_party)
        # attack player's pokemon normally
        if move == 1:
            curr = pok1.hp()
            self.write(f'Computer\'s {pok2.name} used normal attack!')
            pok1.receive_normal_damage(pok2.attack())
            self.write(f'{pok1.name} has received {curr-pok1.hp()} damage!')
            self.write(f"Remaining {pok1.name}'s HP: {pok1.hp()}/{pok1.max_hp()}")
        # attack player's pokemon using special attack
        elif move == 2:
            curr = pok1.hp()
            # get random move type from computer's pokemon types
            move_type = choice(pok2.types())
            # get attack multiplier using choosen type
            multiplier = get_attack_multiplier(move_type, pok1)
            self.write(f'Computer\'s {pok2.name} used special {move_type} attack!')
            # write message according to the multiplier result
            if multiplier == 0:
                self.write(f'{pok2.name} attacked, but the move had no effect on {pok1.name}!')
            elif multiplier < 1:
                self.write(f'It\'s not very effective against opposing {pok1.name}!')
            elif multiplier >= 2:
                self.write(f'It was super effective!')
            pok1.receive_special_damage(pok2._attack*multiplier)
            self.write(f'{pok1.name} has received {curr-pok1.hp()} damage!')
            self.write(f"Remaining {pok1.name}'s HP: {pok1.hp()}/{pok1.max_hp()}")
        # raise defense of computer's pokemon
        elif move == 3:
            self.write(f'Computer\'s {pok2.name} has raised its defense!')
            pok2.raise_defense()
        # computer swaps pokemons
        elif move == 4:
            self.write(f'Computer has swapped its pokemons!')
            self.computer_swap()

    # method that allows computer to swap his current pokemon with the one chosen randomly from computer's party
    def computer_swap(self):
        party_amount = len(self.second_party)
        swapped = randint(1, party_amount-1)
        self.second_party.swap_pokemons(0, swapped)
        self.write(f"The opponent has switched its pokemon for a {self.second_party.get_first()}!")

    # get order in which player and computer move in the first turn
    def get_order(self, pok1, pok2):
        self.order = compare_speeds(pok1, pok2)
        # show player current pokemons from both parties, their hp and order of the attack
        self.write(f"The first pokemon to strike is {self.order[0].name}. It has {self.order[0].hp()} HP.")
        self.write(f"The second pokemon to strike is {self.order[1].name}. It has {self.order[1].hp()} HP.")
        self.write(f"---------------Turn {self.turn}---------------")

    # destroy checbox that allowed player to choose amount of pokemons
    def clear(self):
        self.first_amount = self.var1.get()
        self.labl.destroy()
        self.c1.destroy()
        self.c2.destroy()
        self.c3.destroy()
        self.c4.destroy()
        self.c5.destroy()
        self.c6.destroy()
        # create listbox that will allow to choose pokemons
        self.create_listbox()

    # create checkbox that will allow players to choose how many pokemons they want in their party, between 1 and 6
    def create_amount_checkbox(self):
        self.labl = tk.Label(self.gamewindow, text="Choose amount of pokemons in your party.")
        self.labl.pack()
        self.var1 = tk.IntVar()
        self.c1 = tk.Checkbutton(self.gamewindow, text='1',variable=self.var1, onvalue=1, offvalue=0, command=self.clear)
        self.c1.pack()
        self.c2 = tk.Checkbutton(self.gamewindow, text='2',variable=self.var1, onvalue=2, offvalue=0, command=self.clear)
        self.c2.pack()
        self.c3 = tk.Checkbutton(self.gamewindow, text='3',variable=self.var1, onvalue=3, offvalue=0, command=self.clear)
        self.c3.pack() 
        self.c4 = tk.Checkbutton(self.gamewindow, text='4',variable=self.var1, onvalue=4, offvalue=0, command=self.clear)
        self.c4.pack()
        self.c5 = tk.Checkbutton(self.gamewindow, text='5',variable=self.var1, onvalue=5, offvalue=0, command=self.clear)
        self.c5.pack()
        self.c6 = tk.Checkbutton(self.gamewindow, text='6',variable=self.var1, onvalue=6, offvalue=0, command=self.clear)
        self.c6.pack()

    # make buttons that allow player to move during the battle
    def create_battle_buttons(self):
        self.button1 = tk.Button(self.gamewindow, text="Normal attack", width=19, command=self.player_normal_attack)
        self.button1.place(x=10, y=500)
        self.tktypes = tk.StringVar(self.gamewindow)
        self.tktypes.set("Special attack")
        self.button2 = tk.OptionMenu(self.gamewindow, self.tktypes, *self.first_party.get_first().types(), command=self.player_special_attack)
        self.button2.config(width=19)
        self.button2.place(x=200, y=500)
        self.button3 = tk.Button(self.gamewindow, text="Raise defense", width=19, command=self.player_raise_defense)
        self.button3.place(x=410, y=500)
        self.tkvarq = tk.StringVar(self.gamewindow)
        self.tkvarq.set("Swap pokemon")
        party = self.first_list.copy()
        # swap pokemon button does not allow swapping into the same pokemon
        if len(party) > 1:
            del party[0]
            self.button4 = tk.OptionMenu(self.gamewindow, self.tkvarq, *party, command=self.player_swap)
            self.button4.config(width=19)
        else:
            self.button4 = tk.Button(self.gamewindow, text="No pokemon to swap!", width=19)
        self.button4.place(x=600, y=500)

    # print message to text widget during the battle and write it to the file if this option is chosen
    def write(self, text, log=True):
        self.txt.insert(tk.END, text+"\n")
        self.txt.see(tk.END)
        if log:
            f = open(f"{self.get_file_name}", "a")
            f.write(text+'\n')
            f.close()

    def get_file_name(self):
        dt = date.today()
        nums = str(randint(100000, 999999))
        self.get_file_name = f"logs/log_com_{dt}{nums}"
        return self.get_file_name

    # show winner of the battle
    def show_winner(self, winner):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        if winner == "player":
            self.write("You won!")
        elif winner == "computer":
            self.write("Computer has won!")
        elif winner == "player1":
            self.write("Player1 has won!")
        elif winner == "player2":
            self.write("Player2 has won!")
        self.gamewindow.after(5000, self.gamewindow.destroy)

class PlayGame(ComGame):
    def __init__(self):
        self.log_file_name = self.get_file_name()
        self.gamewindow = tk.Toplevel()
        # set window name and size
        self.gamewindow.title("Local game against other player")
        self.gamewindow.geometry("800x585")
        # flag starts at 0 and is used to determine which player's turn currently is
        self.flag = 0
        # amount of pokemons in both parties
        self.first_amount = 0
        self.second_amount = 0
        # names of pokemon from both parties
        self.first_list = []
        self.second_list = []
        # keep track of turn count
        self.turn = 1
        self.turn_count = 0
        # create empty parties for both players
        self.first_party = PokemonTeam()
        self.second_party = PokemonTeam()
        # create menu allowing to choose amount of pokemons
        self.create_amount_checkbox()
        # run window until closed
        self.gamewindow.mainloop()

    # destroy previous text widget and create new checkbox to allow second player to choose amount of pokemons
    def second_player_choices(self):
        self.txt.destroy()
        self.listbox.destroy()
        self.scrollbar.destroy()
        # increment the flag to make it possible to continue with simulation
        self.flag += 1
        # create new checkbox that will allow second player to choose amount of his/her pokemons
        self.create_amount_checkbox()

    # create checkbox that allow players to choose amount of pokemons
    def create_amount_checkbox(self):
        # show correct message depending on which player currently chooses
        if self.flag == 0: self.labl = tk.Label(self.gamewindow, text="First player now will choose amount of pokemons in their party.")
        else: self.labl = tk.Label(self.gamewindow, text="Now it's time for you second player to choose amount of pokemons in their party.")  
        self.labl.pack()
        self.var1 = tk.IntVar()
        self.c1 = tk.Checkbutton(self.gamewindow, text='1',variable=self.var1, onvalue=1, offvalue=0, command=self.clear)
        self.c1.pack()
        self.c2 = tk.Checkbutton(self.gamewindow, text='2',variable=self.var1, onvalue=2, offvalue=0, command=self.clear)
        self.c2.pack()
        self.c3 = tk.Checkbutton(self.gamewindow, text='3',variable=self.var1, onvalue=3, offvalue=0, command=self.clear)
        self.c3.pack() 
        self.c4 = tk.Checkbutton(self.gamewindow, text='4',variable=self.var1, onvalue=4, offvalue=0, command=self.clear)
        self.c4.pack()
        self.c5 = tk.Checkbutton(self.gamewindow, text='5',variable=self.var1, onvalue=5, offvalue=0, command=self.clear)
        self.c5.pack()
        self.c6 = tk.Checkbutton(self.gamewindow, text='6',variable=self.var1, onvalue=6, offvalue=0, command=self.clear)
        self.c6.pack()

    # destroy checkbox that allowed players to choose amount of pokemons in their parties
    def clear(self):
        if self.flag == 0: self.first_amount = self.var1.get()
        else: self.second_amount = self.var1.get()
        self.labl.destroy()
        self.c1.destroy()
        self.c2.destroy()
        self.c3.destroy()
        self.c4.destroy()
        self.c5.destroy()
        self.c6.destroy()
        # create listbox that will allow to choose pokemons
        self.create_listbox()

    # insert chosen pokemon to the player party, depending on which player chooses
    def insert_to_party(self, evt):
        # flag == 0 means that first player is choosing, flag != 0 means that second player is choosing
        if self.flag == 0:
            party = self.first_party
            party_list = self.first_list
            amount = self.first_amount
        else:
            party = self.second_party
            party_list = self.second_list
            amount = self.second_amount
        # each player chooses amount of pokemons they wanted to choose
        if len(party) < amount:
            value=str((self.listbox.get(tk.ACTIVE)))
            # if pokemon is not in the party, add it to the party, else don't do anything
            if value not in party_list: 
                party.add_to_party(choose_a_pokemon(value))
                party_list.append(value)
                self.txt.insert(tk.END, f'{len(party)}: {value}\n')
            if len(party) == amount:
                # after first player's choice let second player decide
                if self.flag == 0:
                    self.gamewindow.after(2000, self.second_player_choices)
                # after second player's choice, show pokemons that both players have chosen
                else:
                    self.gamewindow.after(2000, self.show_choosen_pokemons)

    # show pokemons that both players have chosen
    def show_choosen_pokemons(self):
        self.txt.destroy()
        self.txt = tk.Text(self.gamewindow, height=34, width=80)
        self.txt.place(x=0, y=0)
        self.txt.insert(tk.END, "Here are first player's pokemons:\n")
        # i is used to format list of pokemons in each player party
        i = 1
        for entry in self.first_list:
            self.txt.insert(tk.END, f'{i}: {entry}\n')
            i += 1
        self.txt.insert(tk.END, "\n\nHere are second player's pokemons:\n")
        i = 1
        for entry in self.second_list:
            self.txt.insert(tk.END, f'{i}: {entry}\n')
            i += 1
        # wait 5 seconds and create battle interface
        self.gamewindow.after(5000, self.create_battle)

    # create battle interface with text, listbox and scrollbar widget
    def create_battle(self):
        self.txt.destroy()
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.txt = tk.Text(self.gamewindow, height = 25, width = 99)
        self.txt.place(x=0, y=0)
        # get orden in which players will move during first turn
        self.get_order(self.first_party.get_first(), self.second_party.get_first())
        # change flag according to which player turn it is
        if self.order[0] == self.first_party.get_first():
            self.flag = 0
        else:
            self.flag = 1
        # create battle buttons that allow to use pokemon moves
        self.create_battle_buttons()

    # create buttons that will allow players to use their moves
    def create_battle_buttons(self):
        # when creating buttons we need to know which pokemon will go first, and we use flag to find out which player goes first
        if self.flag == 0:
            party = self.first_party
            party_list = self.first_list.copy()
        else:
            party = self.second_party
            party_list = self.second_list.copy()
        # create buttons
        self.button1 = tk.Button(self.gamewindow, text="Normal attack", width=19, command=self.normal_attack)
        self.button1.place(x=10, y=500)
        self.tktypes = tk.StringVar(self.gamewindow)
        self.tktypes.set("Special attack")
        self.button2 = tk.OptionMenu(self.gamewindow, self.tktypes, *party.get_first().types(), command=self.special_attack)
        self.button2.config(width=19)
        self.button2.place(x=200, y=500)
        self.button3 = tk.Button(self.gamewindow, text="Raise defense", width=19, command=self.raise_defense)
        self.button3.place(x=410, y=500)
        self.tkvarq = tk.StringVar(self.gamewindow)
        self.tkvarq.set("Swap pokemon")
        # create swap menu
        if len(party_list) > 1:
            del party_list[0]
            self.button4 = tk.OptionMenu(self.gamewindow, self.tkvarq, *party_list, command=self.swap_pokemon)
            self.button4.config(width=19)
        else:
            self.button4 = tk.Button(self.gamewindow, text="No pokemon to swap!", width=19)
        self.button4.place(x=600, y=500)

    # delete all previous buttons and create new in their place
    def remake_buttons(self):
        # if turn_count will go to 2, it means that this turn is over and we can start another one
        self.turn_count += 1
        if self.turn_count  >= 2:
            # after every turn, check pokemon order once again because it might have chainged
            self.order = compare_speeds(self.first_party.get_first(), self.second_party.get_first())
            if self.order[0] == self.first_party.get_first():
            # set flag according to the pokemon that will move first
                self.flag = 0
            else:
                self.flag = 1
            # reset turn_count and write which turn it is
            self.turn_count = 0
            self.write_turn()
        # destroy existing buttons and call method that will replace them
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.create_battle_buttons()

    # change flag to allowe the second player to move
    def change_flag(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    # player used normal attack
    # pok1 - current first player's pokemon
    # pok2 - current second player's pokemon
    # temp_hp1/temp_hp2 - stores value of current pokemons' hp value, used to calculate damage dealt
    def normal_attack(self):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        temp_hp1 = pok1.hp()
        temp_hp2 = pok2.hp()
        # check which player attacks
        if self.flag == 0:
            self.write(f'{pok1.name} used normal attack!')
            pok2.receive_normal_damage(pok1.attack())
            # second player's pokemon survives
            if pok2.hp() > 0:
                self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
                # change flag and remake buttons
                self.change_flag()
                self.remake_buttons()
            # second player's pokemon is defeated
            else:
                self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                # player had only one pokemon left, end game and show winner
                if len(self.second_party) == 1:
                    self.show_winner("player1")
                    return
                # change flag and force swap
                self.change_flag()
                self.force_swap()
        # second player moves first
        else:
            self.write(f'{pok2.name} used normal attack!')
            pok1.receive_normal_damage(pok2.attack())
            # first player's current pokemon survives 
            if pok1.hp() > 0:
                self.write(f"Pokemon {pok1.name} has received {temp_hp1-pok1.hp()} damage.")
                self.write(f"Remaining {pok1.name}'s HP: {pok1.hp()}/{pok1.max_hp()}")
                # change flag and remake buttons
                self.change_flag()
                self.remake_buttons()
            # first player's pokemon is defeated
            else:
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                # player had only one pokemon left, end game and show winner
                if len(self.first_party) == 1:
                    self.show_winner("player2")
                    return
                # change flag and force swap
                self.change_flag()
                self.force_swap()

    # player used special attack
    # pok1 - current player's pokemon
    # pok2 - current computer's pokemon
    # temp_hp1/temp_hp2 - stores value of current pokemons' hp value, used to calculate damage dealt
    # move_type - move's type choosen by the player
    def special_attack(self, evt):
        pok1 = self.first_party.get_first()
        pok2 = self.second_party.get_first()
        temp_hp1 = pok1.hp()
        temp_hp2 = pok2.hp()
        # get move type chosen by the player
        move_type = self.tktypes.get()
        # first player moves first
        if self.flag == 0:
            self.write(f'{pok1.name} used special {move_type} attack!')
            # get attack's damage multiplier that depends on chosen type and attacked pokemon's type(s)
            multiplier = get_attack_multiplier(move_type, pok2)
            # write message depending on multiplier got
            self.write_dmg_mltp(pok1, pok2, multiplier)
            pok2.receive_special_damage(pok1.special_attack()*multiplier)
            # second player's pokemon survives
            if pok2.hp() > 0:
                self.write(f"Pokemon {pok2.name} has received {temp_hp2-pok2.hp()} damage.")
                self.write(f"Remaining {pok2.name}'s HP: {pok2.hp()}/{pok2.max_hp()}")
                # change flag and remake buttons
                self.change_flag()
                self.remake_buttons()
            # second player's pokemon is defeated
            else:
                self.write(f"Pokemon {pok2.name} was dealt {temp_hp2-pok2.hp()} damage and has passed out! It is unable to battle again!", False)
                # player had only one pokemon left, end game and show winner
                if len(self.second_party) == 1:
                    self.show_winner("player1")
                    return
                self.change_flag()
                self.force_swap()
        # second player moves first
        else:
            self.write(f'{pok2.name} used special {move_type} attack!')
            multiplier = get_attack_multiplier(move_type, pok1)
            self.write_dmg_mltp(pok2, pok1, multiplier)
            pok1.receive_special_damage(pok2.special_attack()*multiplier)
            # first player's current pokemon survives 
            if pok1.hp() > 0:
                self.write(f"Pokemon {pok1.name} has received {temp_hp1-pok1.hp()} damage.")
                self.write(f"Remaining {pok1.name}'s HP: {pok1.hp()}/{pok1.max_hp()}")
                # change flag and remake buttons
                self.change_flag()
                self.remake_buttons()
            # first player's pokemon is defeated
            else:
                self.write(f"Pokemon {pok1.name} was dealt {temp_hp1-pok1.hp()} damage and has passed out! It is unable to battle again!", False)
                # player had only one pokemon left, end game and show winner
                if len(self.first_party) == 1:
                    self.show_winner("player2")
                    return
                # change flag and force swap
                self.change_flag()
                self.force_swap()  

    # raise pokemon's defense
    def raise_defense(self):
        # check which player's turn it is
        if self.flag == 0:
            self.first_party.get_first().raise_defense()
            self.write(f'{self.first_party.get_first().name} has raised it\'s defense!', False)
        else:
            self.second_party.get_first().raise_defense()
            self.write(f'{self.second_party.get_first().name} has raised it\'s defense!', False)
        # change flag and remake buttons
        self.change_flag()
        self.remake_buttons()

    def swap_pokemon(self, evt):
        if self.flag == 0:
            party = self.first_party
            party_list = self.first_list
        else:
            party = self.second_party
            party_list = self.second_list
        # swap current pokemon with the chosen one
        name = self.tkvarq.get()
        index = party_list.index(name)
        party.swap_pokemons(0, index)
        party_list[0], party_list[index] = party_list[index], party_list[0]
        self.write(f'Pokemon swapped! Go {party.get_first().name}!')
        # increment turn count
        self.turn_count += 1
        # remake buttons
        self.remake_buttons()

    # create force swap menu
    def force_swap(self):
        # check which player is making decision
        if self.flag == 0:
            party_list = self.first_list
        else:
            party_list = self.second_list
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        if len(party_list) > 1:
            del party_list[0]
            self.tkvarq.set("Swap pokemon")
            self.forced_button = tk.OptionMenu(self.gamewindow, self.tkvarq, *party_list, command=self.forced_swap)
            self.forced_button.config(width=19)
            self.forced_button.place(x=300, y=500)

    # force swap if any player's pokemon was knocked out
    def forced_swap(self, evt):
        # check which player should swap pokemons
        if self.flag == 0:
            party = self.first_party
            party_list = self.first_list
        else:
            party = self.second_party
            party_list = self.second_list
        # get name of chosen pokemon
        name = self.tkvarq.get()
        removed = party.get_pokemon(0)
        # get index of chosen pokemon in the party
        index = party_list.index(name)
        # swap pokemons and remove defeated one from the party
        party.swap_pokemons(0, index+1)
        party.remove_from_party(removed)
        # destroy forced_swap button and remake battle buttons
        self.forced_button.destroy()
        self.write(f'Pokemon swapped! Go {party.get_first().name}!')
        self.update_forced_swap_menu()
        # increment tour count
        self.turn_count += 1
        self.remake_buttons()
    
    # update list of available pokemon to swap for both players
    def update_forced_swap_menu(self):
        self.first_list.clear()
        self.first_list = [pokemon.name for pokemon in self.first_party]
        self.second_list.clear()
        self.second_list = [pokemon.name for pokemon in self.second_party]

    def write(self, text, log=True):
        self.txt.insert(tk.END, text+"\n")
        self.txt.see(tk.END)
        if log:
            f = open(f"{self.get_file_name}", "a")
            f.write(text+'\n')
            f.close()

    def get_file_name(self):
        dt = date.today()
        nums = str(randint(100000, 999999))
        self.get_file_name = f"logs/log_play_{dt}{nums}"
        return self.get_file_name