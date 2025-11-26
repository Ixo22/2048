import tkinter as tk
from tkinter import messagebox
import random
import os

class Juego2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("2048 Pro + Deshacer")
        self.master.geometry("600x750") # Un poco más alto para los botones
        self.master.minsize(400, 500)
        
        # --- CONFIGURACIÓN RESPONSIVA ---
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky="nsew")

        self.rowconfigure(0, weight=1) 
        self.rowconfigure(1, weight=20) 
        self.columnconfigure(0, weight=1)

        # --- VARIABLES DE ESTADO ---
        self.score = 0
        self.high_score = self.cargar_high_score()
        self.ya_gane = False
        
        # --- SISTEMA DE DESHACER (NUEVO) ---
        self.historial = []       # Aquí guardaremos los tableros anteriores
        self.undos_maximos = 5
        self.undos_restantes = self.undos_maximos
        
        # --- CONTROLES ---
        self.master.bind("<Left>", self.left); self.master.bind("a", self.left)
        self.master.bind("<Right>", self.right); self.master.bind("d", self.right)
        self.master.bind("<Up>", self.up); self.master.bind("w", self.up)
        self.master.bind("<Down>", self.down); self.master.bind("s", self.down)
        self.master.bind("<Configure>", self.al_cambiar_tamano)
        # Atajo de teclado para deshacer (Ctrl+Z)
        self.master.bind("<Control-z>", lambda event: self.deshacer_movimiento())

        self.colores = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
            'super': "#3c3a32"
        }
        
        self.celdas = []
        self.construir_interfaz()
        self.iniciar_juego()
        self.mainloop()

    # --- PERSISTENCIA ---
    def cargar_high_score(self):
        if not os.path.exists("highscore.txt"): return 0
        try:
            with open("highscore.txt", "r") as f: return int(f.read())
        except: return 0

    def guardar_high_score(self):
        with open("highscore.txt", "w") as f: f.write(str(self.high_score))

    # --- INTERFAZ GRÁFICA ---
    def construir_interfaz(self):
        # HEADER
        self.header = tk.Frame(self, bg="#bbada0")
        self.header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        for i in range(4): self.header.columnconfigure(i, weight=1) # 4 columnas ahora

        estilo_lbl = {"font": ("Verdana", 12, "bold"), "bg": "#bbada0", "fg": "white"}
        
        self.lbl_score = tk.Label(self.header, text="Score: 0", **estilo_lbl)
        self.lbl_score.grid(row=0, column=0, pady=10)

        self.lbl_best = tk.Label(self.header, text=f"Best: {self.high_score}", **estilo_lbl)
        self.lbl_best.grid(row=0, column=1, pady=10)

        # --- BOTÓN DESHACER (NUEVO) ---
        self.btn_undo = tk.Button(self.header, text=f"Deshacer ({self.undos_restantes})", 
                                  font=("Verdana", 9, "bold"), command=self.deshacer_movimiento, 
                                  bg="#f65e3b", fg="white", activebackground="#e04d2b", 
                                  relief="flat", cursor="hand2")
        self.btn_undo.grid(row=0, column=2, pady=10, padx=5)

        self.btn_reset = tk.Button(self.header, text="Reiniciar", font=("Verdana", 9, "bold"), 
                                   command=self.confirmar_reinicio, bg="#8f7a66", fg="white", 
                                   activebackground="#9e8b7a", relief="flat", cursor="hand2")
        self.btn_reset.grid(row=0, column=3, pady=10, padx=5)

        # ZONA DE JUEGO
        self.zona_juego = tk.Frame(self, bg="#faf8ef")
        self.zona_juego.grid(row=1, column=0, sticky="nsew")

        # TABLERO
        self.tablero = tk.Frame(self.zona_juego, bg="#bbada0")
        for i in range(4):
            self.tablero.rowconfigure(i, weight=1, uniform="row_group")
            self.tablero.columnconfigure(i, weight=1, uniform="col_group")

        self.celdas = []
        for i in range(4):
            fila = []
            for j in range(4):
                marco_celda = tk.Frame(self.tablero, bg=self.colores[0])
                marco_celda.grid(row=i, column=j, sticky="nsew", padx=4, pady=4)
                marco_celda.rowconfigure(0, weight=1)
                marco_celda.columnconfigure(0, weight=1)

                lbl = tk.Label(master=marco_celda, text="", bg=self.colores[0], 
                               justify=tk.CENTER, font=("Helvetica", 20, "bold"))
                lbl.grid(sticky="nsew")
                fila.append(lbl)
            self.celdas.append(fila)

    def al_cambiar_tamano(self, event):
        if event.widget == self.master:
            w = self.master.winfo_width()
            h = self.master.winfo_height()
            h_disponible = h - 100
            lado = min(w, h_disponible) - 30
            if lado < 300: lado = 300
            self.tablero.place(relx=0.5, rely=0.5, anchor="center", width=lado, height=lado)
            
            tamano_celda = lado // 4
            font_size = int(tamano_celda / 2.2)
            nueva_fuente = ("Helvetica", font_size, "bold")
            for fila in self.celdas:
                for lbl in fila:
                    lbl.configure(font=nueva_fuente)

    # --- LÓGICA DEL JUEGO ---
    def iniciar_juego(self):
        self.matriz = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.ya_gane = False
        
        # Resetear sistema de Undo
        self.historial = [] 
        self.undos_restantes = self.undos_maximos
        
        self.agregar_nuevo_tile()
        self.agregar_nuevo_tile()
        self.actualizar_ui()
        self.focus_set()

    def confirmar_reinicio(self):
        if messagebox.askyesno("2048", "¿Seguro que quieres reiniciar?"):
            self.iniciar_juego()

    # --- LÓGICA DE DESHACER (UNDO) ---
    def guardar_estado(self):
        # Creamos una copia profunda manual de la matriz
        matriz_copia = [fila[:] for fila in self.matriz]
        # Guardamos la tupla (matriz, score)
        self.historial.append((matriz_copia, self.score))

    def deshacer_movimiento(self):
        if self.undos_restantes > 0 and len(self.historial) > 0:
            # Recuperamos el último estado
            matriz_anterior, score_anterior = self.historial.pop()
            
            # Restauramos
            self.matriz = matriz_anterior
            self.score = score_anterior
            
            # Restamos un uso
            self.undos_restantes -= 1
            
            self.actualizar_ui()
        elif self.undos_restantes == 0:
            messagebox.showinfo("Ups", "¡Te has quedado sin movimientos de deshacer!")

    def actualizar_ui(self):
        # Actualizar Tablero
        for i in range(4):
            for j in range(4):
                val = self.matriz[i][j]
                lbl = self.celdas[i][j]
                if val == 0:
                    lbl.configure(text="", bg=self.colores[0])
                    lbl.master.configure(bg=self.colores[0])
                else:
                    color_txt = "#776e65" if val < 8 else "#f9f6f2"
                    color_bg = self.colores.get(val, self.colores['super'])
                    lbl.configure(text=str(val), bg=color_bg, fg=color_txt)
                    lbl.master.configure(bg=color_bg)
        
        self.lbl_score.configure(text=f"Score: {self.score}")
        self.lbl_best.configure(text=f"Best: {self.high_score}")
        
        # Actualizar texto y estado del botón Undo
        texto_undo = f"Deshacer ({self.undos_restantes})"
        self.btn_undo.configure(text=texto_undo)
        
        if self.undos_restantes == 0 or len(self.historial) == 0:
            self.btn_undo.configure(state="disabled", bg="#dbaea4") # Color apagado
        else:
            self.btn_undo.configure(state="normal", bg="#f65e3b")

        self.update_idletasks()

    # --- MATEMÁTICAS ---
    def comprimir(self):
        changed = False
        nueva_matriz = [[0]*4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.matriz[i][j] != 0:
                    nueva_matriz[i][pos] = self.matriz[i][j]
                    if j != pos: changed = True
                    pos += 1
        self.matriz = nueva_matriz
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
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.guardar_high_score()
                    if self.matriz[i][j] == 2048 and not self.ya_gane:
                        self.ya_gane = True
                        self.actualizar_ui()
                        messagebox.showinfo("¡Victoria!", "¡Has conseguido el 2048!")
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

    # --- MOTOR DE MOVIMIENTO ---
    def mover(self, key):
        # 1. Guardamos el estado ACTUAL antes de intentar mover
        # Hacemos una copia temporal por si el movimiento no es válido
        matriz_temp = [fila[:] for fila in self.matriz]
        score_temp = self.score
        
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
            # 2. Si hubo cambio real, guardamos el estado anterior en el historial
            self.historial.append((matriz_temp, score_temp))
            
            # 3. Añadimos el nuevo número y seguimos
            self.agregar_nuevo_tile()
            self.actualizar_ui()
            self.check_game_over()
        # Si no hubo cambio, no guardamos nada en el historial ni gastamos memoria

    def agregar_nuevo_tile(self):
        vacios = [(r,c) for r in range(4) for c in range(4) if self.matriz[r][c] == 0]
        if vacios:
            r, c = random.choice(vacios)
            self.matriz[r][c] = 2 if random.random() < 0.9 else 4

    def check_game_over(self):
        if any(0 in fila for fila in self.matriz): return
        for i in range(4):
            for j in range(3):
                if self.matriz[i][j] == self.matriz[i][j+1]: return
        for i in range(3):
            for j in range(4):
                if self.matriz[i][j] == self.matriz[i+1][j]: return
        
        if messagebox.askyesno("Game Over", f"¡Juego Terminado!\nScore: {self.score}\n¿Reiniciar?"):
            self.iniciar_juego()
        else:
            self.master.destroy()

    def left(self, e): self.mover('Left')
    def right(self, e): self.mover('Right')
    def up(self, e): self.mover('Up')
    def down(self, e): self.mover('Down')

if __name__ == "__main__":
    app = Juego2048()