import tkinter as tk
import random

class Juego2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("2048 Python Edition")
        self.master.geometry("600x700")
        self.grid(sticky="nsew")

        # Configuración de colores (Oficiales del 2048)
        self.colores = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
            'super': "#3c3a32"
        }
        
        self.construir_interfaz()
        self.mainloop()

    def construir_interfaz(self):
        # Frame Principal
        self.zona_juego = tk.Frame(self, bg="#faf8ef")
        self.zona_juego.grid(row=0, column=0, sticky="nsew")
        
        # Tablero de 4x4
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

if __name__ == "__main__":
    app = Juego2048()