import tkinter as tk
from tkinter import messagebox
import random

class Juego2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("2048 Python Edition")
        self.master.geometry("600x700")
        self.grid(sticky="nsew")
        
        # Controles
        self.master.bind("<Left>", self.left); self.master.bind("a", self.left)
        self.master.bind("<Right>", self.right); self.master.bind("d", self.right)
        self.master.bind("<Up>", self.up); self.master.bind("w", self.up)
        self.master.bind("<Down>", self.down); self.master.bind("s", self.down)

        self.colores = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
            'super': "#3c3a32"
        }
        
        self.construir_interfaz()
        self.iniciar_juego()
        self.mainloop()

    def construir_interfaz(self):
        self.zona_juego = tk.Frame(self, bg="#faf8ef")
        self.zona_juego.grid(row=0, column=0, sticky="nsew")
        self.tablero = tk.Frame(self.zona_juego, bg="#bbada0")
        self.tablero.pack(fill="both", expand=True, padx=20, pady=20)

        self.celdas = []
        for i in range(4):
            fila = []
            frame_fila = tk.Frame(self.tablero, bg="#bbada0")
            frame_fila.pack(fill="both", expand=True)
            for j in range(4):
                lbl = tk.Label(frame_fila, text="", bg=self.colores[0],
                               font=("Helvetica", 24, "bold"), width=4, height=2)
                lbl.pack(side="left", fill="both", expand=True, padx=5, pady=5)
                fila.append(lbl)
            self.celdas.append(fila)

    def iniciar_juego(self):
        self.matriz = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.agregar_nuevo_tile()
        self.agregar_nuevo_tile()
        self.actualizar_ui()

    def actualizar_ui(self):
        for i in range(4):
            for j in range(4):
                val = self.matriz[i][j]
                lbl = self.celdas[i][j]
                if val == 0:
                    lbl.configure(text="", bg=self.colores[0])
                else:
                    color_txt = "#776e65" if val < 8 else "#f9f6f2"
                    color_bg = self.colores.get(val, self.colores['super'])
                    lbl.configure(text=str(val), bg=color_bg, fg=color_txt)
        self.update_idletasks()

    # --- LÓGICA MATEMÁTICA ---
    def comprimir(self):
        changed = False
        nueva = [[0]*4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.matriz[i][j] != 0:
                    nueva[i][pos] = self.matriz[i][j]
                    if j != pos: changed = True
                    pos += 1
        self.matriz = nueva
        return changed

    def fusionar(self):
        changed = False
        for i in range(4):
            for j in range(3):
                if self.matriz[i][j] != 0 and self.matriz[i][j] == self.matriz[i][j+1]:
                    self.matriz[i][j] *= 2
                    self.matriz[i][j+1] = 0
                    self.score += self.matriz[i][j]
                    changed = True
        return changed

    def reversa(self):
        nuevo = []
        for i in range(4):
            nuevo.append([])
            for j in range(4):
                nuevo[i].append(self.matriz[i][3-j])
        self.matriz = nuevo

    def transponer(self):
        nuevo = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                nuevo[i][j] = self.matriz[j][i]
        self.matriz = nuevo

    def agregar_nuevo_tile(self):
        vacios = [(r,c) for r in range(4) for c in range(4) if self.matriz[r][c] == 0]
        if vacios:
            r, c = random.choice(vacios)
            self.matriz[r][c] = 2 if random.random() < 0.9 else 4

    def mover(self, key):
        cambio = False
        if key == 'Left':
            c1, c2, c3 = self.comprimir(), self.fusionar(), self.comprimir()
            cambio = c1 or c2 or c3
        elif key == 'Right':
            self.reversa()
            c1, c2, c3 = self.comprimir(), self.fusionar(), self.comprimir()
            self.reversa()
            cambio = c1 or c2 or c3
        elif key == 'Up':
            self.transponer()
            c1, c2, c3 = self.comprimir(), self.fusionar(), self.comprimir()
            self.transponer()
            cambio = c1 or c2 or c3
        elif key == 'Down':
            self.transponer(); self.reversa()
            c1, c2, c3 = self.comprimir(), self.fusionar(), self.comprimir()
            self.reversa(); self.transponer()
            cambio = c1 or c2 or c3

        if cambio:
            self.agregar_nuevo_tile()
            self.actualizar_ui()
            # Aquí iría el Game Over check

    def left(self, e): self.mover('Left')
    def right(self, e): self.mover('Right')
    def up(self, e): self.mover('Up')
    def down(self, e): self.mover('Down')

if __name__ == "__main__":
    app = Juego2048()