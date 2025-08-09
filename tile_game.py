import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random
import math

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Herní konfigurátor")
        self.root.geometry("1600x900")
        self.tilesize = 60
        self.tiles = {}
        self.player_colors = ["blue", "red", "yellow", "green"]
        self.player_names = ["Faolin", "Nalia", "Kappa", "Teemur"]
        self.enemy_weapons = ["1k2", "1k4", "1k6", "1k8", "1k10"]
        self.enemy_armor = ["žádná", "lehká", "střední", "těžká"]
        self.enemy_color = "grey"
        self.rows = 0
        self.cols = 0
        self.no_of_players = {}
        self.selected_o = {}
        self.selected_tile = []


        self.setup_layout()
        self.create_left_panel()
        self.create_right_panel()
        self.create_grid_input_section()
        self.player_numbers()
        self.enemy_numbers()
        


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
            if rows < 4 and cols < 2:
                messagebox.showinfo("Error", "Řádky musí být minimálně 4 a sloupce 2")
                return
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
                tile = tk.Label(inner_frame, width=4, height=2, bg="white", relief="ridge", borderwidth=3, padx=self.tilesize, pady=self.tilesize)
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


    def enemy_numbers(self):
        tk.Label(self.left_frame, text="Počet nepřátel:").pack(pady=(10, 0),)
        self.entry_enemy_no = tk.Entry(self.left_frame)
        self.entry_enemy_no.pack()

        tk.Button(self.left_frame, text="Umísti nepřátele", command=self.random_enemy_placement).pack(pady=10)            

    def on_tile_click(self, row, col):
        bg = self.tiles[(row,col)].cget("bg")
        play_names = self.tiles[(row,col)].cget("text")
        if bg != "white" and not self.selected_tile:
            self.tiles[(row,col)].config(highlightbackground="blue", highlightthickness=0, borderwidth=3,relief="solid")
            self.selected_tile = [bg, row, col, play_names]
            print(self.selected_tile)
        elif self.selected_tile and bg == "white":
            stored_bg = self.selected_tile[0]
            former_row = self.selected_tile[1]
            former_col = self.selected_tile[2]
            stored_play_names = self.selected_tile[3]
            self.tiles[(row,col)].config(bg=stored_bg, text=stored_play_names)
            self.tiles[(former_row,former_col)].config(bg="white",highlightbackground="white",borderwidth=3,relief="ridge",text="")
            self.selected_tile = []
        elif self.selected_tile and bg != "white":
            return

    def random_players_placement(self):
        try:
            for x in range(self.rows):
                for y in range(math.ceil(self.cols/2)):
                    if self.tiles[(x,y)].cget("bg") != 'white':
                        self.tiles[(x,y)].config(bg='white', text='')

            for i in range(int(self.selected_o.get())):
                while True: 
                    random_x = random.randint(0, self.rows-1)
                    random_y = random.randint(0, math.ceil(self.cols/2)-1)
                    if self.tiles[(random_x,random_y)].cget("bg") == 'white':
                        self.tiles[(random_x,random_y)].config(bg=self.player_colors[i],text=self.player_names[i])
                        break

        except (TypeError,ValueError):
            return
        
    def random_enemy_placement(self):
        if int(self.entry_enemy_no.get()) > ((math.floor(self.cols/2))*(self.rows)):
            messagebox.showinfo("error", "moc nepřátel, zkus méně")
            return
        else:
            try:
                for x in range(self.rows):
                    for y in range(math.ceil(self.cols/2), self.cols):
                        if self.tiles[(x,y)].cget("bg") != 'white':
                            self.tiles[(x,y)].config(bg='white', text='')

                for i in range(int(self.entry_enemy_no.get())):
                    while True: 
                        random_x_enemy = random.randint(0, self.rows-1)
                        random_y_enemy = random.randint(math.ceil(self.cols/2), self.cols-1)
                        if self.tiles[(random_x_enemy,random_y_enemy)].cget("bg") == 'white':
                            self.tiles[(random_x_enemy,random_y_enemy)].config(bg=self.enemy_color, text="Enemy no. " + str(i+1) + "\n" + self.enemy_weapons[random.randint(0, len(self.enemy_weapons)-1)]
                                        + "\n" + self.enemy_armor[random.randint(0, len(self.enemy_armor)-1)])
                            
                            break

            except (TypeError,ValueError):
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
