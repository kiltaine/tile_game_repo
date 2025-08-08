import tkinter as tk
from tkinter import messagebox
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Herní konfigurátor")
        self.root.geometry("800x600")
        self.tilesize = 30
        self.tiles = {}
        self.player_colors = ["white", "red", "yellow", "green"]
        self.enemy_color = "grey"
        self.rows = {}
        self.cols = {}
        self.no_of_players = {}
        self.selected_o = {}

        self.setup_layout()
        self.create_left_panel()
        self.create_right_panel()
        self.create_grid_input_section()
        self.player_numbers()


    def setup_layout(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)

    def create_left_panel(self):
        self.left_frame = tk.Frame(self.root, bg="lightgray")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_propagate(False)
        self.left_frame.config(width=150)

    def create_right_panel(self):
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")


    def create_grid_input_section(self):
        tk.Label(self.left_frame, text="Řádky (X):").pack(pady=(10, 0),)
        self.entry_x = tk.Entry(self.left_frame)
        self.entry_x.pack()
        

        tk.Label(self.left_frame, text="Sloupce (Y):").pack(pady=(10, 0),)
        self.entry_y = tk.Entry(self.left_frame)
        self.entry_y.pack()

        tk.Button(self.left_frame, text="Vytvořit pole", command=self.create_grid).pack(pady=10)
        tk.Button(self.left_frame, text="Vymaž pole", command=self.destroy_grid).pack(pady=10)

    def create_grid(self):
        try:
            rows = int(self.entry_x.get())
            cols = int(self.entry_y.get())
        except ValueError:
            print("Zadej platná čísla")
            return
        self.rows = rows
        self.cols = cols    

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        inner_frame = tk.Frame(self.right_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        for i in range(rows):
            for j in range(cols):
                tile = tk.Label(inner_frame, width=4, height=2, bg="white", relief="ridge", borderwidth=1, padx=self.tilesize, pady=self.tilesize)
                tile.grid(row=i, column=j, padx=1, pady=1)
                tile.bind("<Button-1>", lambda e, r=i, c=j: self.on_tile_click(r, c))
                self.tiles[(i,j)] = tile


    def player_numbers(self):
        no_players = [1,2,3,4]
        selected_option = tk.StringVar(value=no_players[0])
        tk.Label(self.left_frame, text="Počet hráčů").pack(pady=(10, 5),)
        self.entry_no_players = tk.OptionMenu(self.left_frame,selected_option,*no_players)
        self.entry_no_players.pack()
        

        tk.Button(self.left_frame, text="OK", command=self.random_players_placement).pack()
        self.selected_o = selected_option

    def on_tile_click(self, row, col):
        bg = self.tiles[(row,col)].cget("bg")
        if bg != "white":
            self.tiles[(row,col)].config(bg="white")
        else:
            self.tiles[(row,col)].config(bg="red")
        
    def random_players_placement(self):
        try:
            random_x = random.randint(1, self.rows - 1)
            random_y = random.randint(1, self.cols - 1)
            self.tiles[(random_x,random_y)].config(bg="red")
            print(self.selected_o.get())
        except TypeError:
            return
        
                   
    
    def destroy_grid(self):
        if self.right_frame.winfo_children():
            for widget in self.right_frame.winfo_children():
                widget.destroy()
        else: 
            messagebox.showinfo(title="Error", message="Nic tu není")
            return



# ------------------------------
# Hlavní část programu
# ------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
