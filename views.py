# Capa de Interfaz Gráfica (Tkinter / TTK)

import tkinter as tk
from tkinter import ttk

class Menu:
    def __init__(self, master, usuario, gestor):
        self.master = master
        self.usuario = usuario
        self.gestor = gestor

        self.master.title("CarDir HelpDesk")
        self.master.geometry("800x600+100+50")

        # ----- FRAME SUPERIOR -----
        frame_superior = tk.Frame(self.master)
        frame_superior.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        etiqueta = tk.Label(frame_superior, text="CarDir HelpDesk 1.0", font=("Arial", 16))
        etiqueta.grid(row=0, column=0, padx=10, pady=10)

        separator = ttk.Separator(self.master, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)

        boton_listar = tk.Button(frame_superior, text="Listar Tickets", command=self.mostrar_tickets)
        boton_listar.grid(row=1, column=1, padx=10, pady=10)
        boton_buscar = tk.Button(frame_superior, text="Buscar Tickets", command="")
        boton_buscar.grid(row=1, column=2, padx=10, pady=10)
        boton_modificar = tk.Button(frame_superior, text="Modificar Tickets", command= "")
        boton_modificar.grid(row=1, column=3, padx=10, pady=10)
        boton_eliminar = tk.Button(frame_superior, text="Eliminar Tickets", command="")
        boton_eliminar.grid(row=1, column=4, padx=10, pady=10)



        # ----- FRAME DEL TREEVIEW -----


        frame_tree = tk.Frame(self.master)
        frame_tree.grid(row=2, column=0, sticky="nsew")

        # Permitir que el Treeview se expanda
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self.columnas = ("ID", "Usuario", "Descripción", "Categoría", "Prioridad", "Estado")
        self.tree = ttk.Treeview(frame_tree, columns=self.columnas, show="headings")

        for col in self.columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Expandir Treeview dentro del frame
        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)


    def mostrar_tickets(self):
        # Limpiar el Treeview antes de insertar
        for item in self.tree.get_children():
            self.tree.delete(item)

        tickets = self.gestor.listar_tickets()

        for t in tickets:
            self.tree.insert("", tk.END, values=(
                t["id_ticket"],
                t["usuario"],
                t["descripcion"],
                t["categoria"],
                t["prioridad"],
                t["estado"]
            ))
