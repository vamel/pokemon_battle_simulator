import tkinter as tk
import sys
from statshower import StatShower
from game import ComGame, PlayGame


# main window that contains main menu
class Window(object):
    def __init__(self):
        self.window = tk.Tk()
        # set the title and size of the window
        self.window.title("Pokemon Battle Simulator")
        self.window.geometry("800x600")
        # create text widget that show the action
        self.create_text_widget()
        self.create_buttons()
        # window will run until closed
        self.window.mainloop()

    # create main menu buttons
    def create_buttons(self):
        self.button1 = tk.Button(self.window, text="Show Pokemon stats", width=19, command=self.create_stat_shower)
        self.button1.place(x=10, y=500)
        self.playbutton1 = tk.Button(self.window, text="Play against computer", width=19, command=lambda: self.main_menu(False))
        self.playbutton1.place(x=210, y=500)
        self.playbutton2 = tk.Button(self.window, text="Play against other player", width=19, command=lambda: self.main_menu(True))
        self.playbutton2.place(x=410, y=500)
        self.exitbutton = tk.Button(self.window, text="End simulation", width=19, command=self.exit)
        self.exitbutton.place(x=610, y=500)

    # create text widget that welcoms the user and shows "simulation ended" message after exiting the program using button
    def create_text_widget(self, text="Welcome to Pokemon Battle Simulator!\nClick one of the buttons below to choose an option."):
        self.text = tk.Text(self.window, height=25, width=80)
        self.text.place(x=70, y=1)
        if text:
            self.text.tag_configure("center", justify="center")
            self.text.insert(tk.END, text, "center")
            self.text.tag_add("center", "1.0", "end")

    # delete content of the text widget
    def empty_textbox(self):
        self.text.delete('1.0', tk.END)
        
    # exit program
    def exit(self):
        self.empty_textbox()
        self.create_text_widget("Simulation ended")
        self.window.after(1000, sys.exit)

    # create window that allows to see pokemon stats
    def create_stat_shower(self):
        StatShower()

    # start the battle against computer or against other player
    def main_menu(self, player):
        f = open("log.txt", "w")
        f.close()
        if player:
            PlayGame()
        else:
            ComGame()

Window()