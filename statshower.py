import tkinter as tk
from pokemon_battle_sim import get_pokedex, gui_pokemon_stats


# window which shows pokemon stats
class StatShower(object):
    def __init__(self):
        self.statshower = tk.Toplevel()
        # set the name and size of the window
        self.statshower.title("Pokemon Stat Shower")
        self.statshower.geometry("400x330")
        # get list of all pokemons sorted alphabetically
        self.pokemons = sorted(get_pokedex())
        # create text widget that will show stats of choosen pokemon
        self.txt = tk.Text(self.statshower, height=19, width=32)
        self.txt.place(x=0, y=0)
        # create listbox that will contain names of all pokemons
        self.listbox = tk.Listbox(self.statshower, height=17, width=15)
        # insert all pokemon names into the listbox
        self.insert_pokemons()
        # select pokemon with doubleclick to show its stats
        self.listbox.bind('<Double-1>', self.print_stats)
        self.listbox.place(x=260, y=24)
        # create a scrollbar to help navigate through listbox
        self.scrollbar = tk.Scrollbar(self.statshower, orient='vertical', command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        # create search bar to help find pokemons
        self.create_search_bar()
        # run the window until closed
        self.statshower.mainloop()

    # creating search bar that will help user enter correct pokemons
    def create_search_bar(self):
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(self.statshower, textvariable=self.search_var, width=15)
        self.entry.place(x=260, y=0)

    # update list when searching for a pokemon
    def update_list(self, *args):
        search_term = self.search_var.get()
        # delete all elements in a list
        self.listbox.delete(0, tk.END)
        for item in self.pokemons:
                # insert the pokemon name if it matches entered string
                if search_term.title() in item.title():
                    self.listbox.insert(tk.END, item)

    # insert all pokemon names to the listbox
    def insert_pokemons(self):
        for i in range(len(self.pokemons)):
            self.listbox.insert('end', self.pokemons[i])

    # show pokemon's stats in a text widget
    def print_stats(self, evt):
        self.txt.delete('1.0', tk.END)
        value=str((self.listbox.get(tk.ACTIVE)))
        self.txt.insert(tk.END, gui_pokemon_stats(value))