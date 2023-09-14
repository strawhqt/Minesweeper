import tkinter as tk
from tkinter import messagebox
from random import randint
import threading
from PIL import Image, ImageTk, ImageSequence
import winsound
import time


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.field = [[0] * 26 for i in range(1,27)]
        self.create_field()
        self.create_mines_numbers()
        self.create_layout()
        self.game_over = False
        self.colors = ['white', 'blue', 'green', 'red', 'purple', 'orange', 'pink', 'black', 'yellow']
        self.win = False

    def create_layout(self):
        reset_button = tk.Button(self, text="Restart", command= self.reset)
        reset_button.grid(row=0, column=0, columnspan=26, sticky='N' + 'W')
        exit_button = tk.Button(self, text = 'Exit', command = self.quit)
        exit_button.grid(row = 0, column = 0, columnspan = 26, sticky = 'N' + 'E')

    def create_field(self):
        self.buttons = [[] * 26 for i in range(1,27)]
        # x is 1 index, y is 0 index
        for x in range(1, 25):
            for y in range(1, 25):
                b = tk.Button(self, width=2, command=lambda x=x, y=y: self.show_button(x,y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.right_click(x,y))
                b.grid(row = x+1, column = y+1)
                self.buttons[x].append(b)

    def create_mines_numbers(self):
        for n in range(99):
            x = randint(1,25)
            y = randint(1,25)
            if self.field[x][y] != -1:
                self.field[x][y] = -1
        dx = [1, 0, -1]
        dy = [0, 1, -1]
        for i in range(1, 25):
            for j in range(1, 25):
                if not self.field[i][j] == -1:
                    for r in dx:
                        for c in dy:
                            if i+r <= 24 and i+r >= 0 and j+c <= 24 and j+c >= 0:
                                if self.field[i + r][j + c] == -1:
                                    self.field[i][j] += 1

    def show_button(self, n, m):
        if self.game_over:
            return
        if self.buttons[n][m-1]['text'] == 'X':
            return

        if self.buttons[n][m-1]['relief'] == 'sunken' and self.field[n][m] > 0:
            dx = [1, 0, -1]
            dy = [0, 1, -1]
            condition = True
            num_x = 0
            for r in dx:
                for c in dy:
                    if n + r <= 24 and n + r >= 1 and m + c <= 24 and m + c >= 1:
                        if self.buttons[n+r][m+c-1]['text'] == "X":
                            num_x += 1
                        if self.field[n+r][m+c] == -1 and self.buttons[n+r][m+c-1]['text'] == "X":
                            continue
                        elif self.field[n+r][m+c] == -1 and self.buttons[n+r][m+c-1]['text'] != "X":
                            condition = False

            if condition and num_x == self.field[n][m]:
                for r in dx:
                    for c in dy:
                        if n + r <= 24 and n + r >= 1 and m + c <= 24 and m + c >= 1:
                            self.buttons[n + r][m + c - 1]['text'] == " "
                            self.reveal_flag(n+r,m+c)

            if num_x == self.field[n][m] and not condition:
                self.game_over = True


        text = ""
        if self.field[n][m] == -1:
            text = "*"
            self.game_over = True
        elif self.field[n][m] != -1 and self.field[n][m] != 0:
            text = str(self.field[n][m])
        elif self.field[n][m] == 0:
            self.zero_recursion(n,m)
            return

        if not self.game_over:
            self.buttons[n][m-1].config(relief= 'sunken', fg = self.colors[self.field[n][m]])
        if self.game_over:
            self.buttons[n][m-1].config(relief = 'sunken')
        self.buttons[n][m-1]['text'] = text

        if self.game_over and not self.win:
            self.buttons[n][m-1].config(bg = 'red')
            self.game_finish()
        self.check_win()

    def reveal_flag(self, n, m):
        if self.buttons[n][m-1]['text'] != "X" and self.field[n][m] > 0:
            self.buttons[n][m-1].config(relief = 'sunken')
        text = ""
        if self.field[n][m] > 0:
            text = str(self.field[n][m])
        if self.field[n][m] == 0:
            self.zero_recursion(n,m)
            return
        if self.buttons[n][m-1]['text'] == "X":
            text = "X"

        self.buttons[n][m-1]['text'] = text
        if self.buttons[n][m-1]['text'] != "X":
            self.buttons[n][m-1].config(fg = self.colors[self.field[n][m]])
        self.check_win()


    def right_click(self, n, m):
        if self.buttons[n][m-1]['relief'] == 'sunken':
            return
        if self.buttons[n][m-1]['text'] == "X":
            self.buttons[n][m-1]['text'] = " "
        else:
            self.buttons[n][m-1]['text'] = "X"
        self.check_win()

    def zero_recursion(self, n, m):
        if self.buttons[n][m-1]['relief'] == 'sunken':
            return
        if self.field[n][m] != 0:
            self.buttons[n][m-1]['text'] = str(self.field[n][m])
            self.buttons[n][m - 1].config(relief='sunken', fg = self.colors[self.field[n][m]])
        else:
            self.buttons[n][m-1]['text'] = " "
            self.buttons[n][m - 1].config(relief='sunken')


        if self.field[n][m] == 0:
            dx = [1, 0, -1]
            dy = [0, 1, -1]
            for r in dx:
                for c in dy:
                    if n+r <= 24 and n+r >= 1 and m+c-1 >= 0 and m+c-1 <= 23:
                        self.zero_recursion(n + r, m + c)

    def check_win(self):
        if self.game_over:
            return
        win = True
        for i in range(1,25):
            for j in range(1,25):
                if self.field[i][j] != -1 and self.buttons[i][j-1]['relief'] != 'sunken':
                    win = False
        if win:
            self.win = True
            self.game_over = True
            response = tk.messagebox.askyesno(title = "You Won!", message = "Congratulations, you won! Would you like to try again?")
            if response == 1:
                self.reset()
            else:
                self.quit()

    def game_finish(self):
        response  = tk.messagebox.askyesno(title="Game Over!", message="You Lost! Do you wish to try again?")
        if response == 1:
            self.reset()
        else:
            self.quit()

    def reset(self):
        self.field = [[0] * 26 for i in range(1, 27)]
        self.create_field()
        self.create_mines_numbers()
        self.game_over = False
        self.win = False




main_window = tk.Tk()
main_window.state("zoomed")
main_window.title("Minesweeper")
main_window.geometry("{}x{}+0+0".format(main_window.winfo_screenwidth(), main_window.winfo_screenheight()))
app = App(main_window)
main_window.mainloop()

