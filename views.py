# Capa de Interfaz Gráfica (Tkinter / TTK)

import tkinter as tk
from tkinter import ttk
from venv import create

from models import TicketManager,Usuario


class Menu:
    """Pantalla principal"""
    def __init__(self, master):
        self.master = master
        # self.usuario = usuario
        # self.gestor = gestor

        self.master.title("CarDir HelpDesk")

        # ----- CENTRAR LA VENTANA PRINCIPAL -----
        ancho = 1080
        alto = 800

        pantalla_ancho = self.master.winfo_screenwidth()
        pantalla_alto = self.master.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")




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
    def formulario_crear(self):
        # ----- FORMULARIO -----
        frame = tk.LabelFrame(self.master, text="Crear Ticket", padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(frame, text="Descripción:").grid(row=0, column=0, sticky="w")
        self.descripcion = tk.Entry(frame, width=50)
        self.descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Categoría:").grid(row=1, column=0, sticky="w")
        self.categoria = ttk.Combobox(frame, values=["Hardware", "Software", "Red", "Otro"])
        self.categoria.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Prioridad:").grid(row=2, column=0, sticky="w")
        self.prioridad = ttk.Combobox(frame, values=["Baja", "Media", "Alta"])
        self.prioridad.grid(row=2, column=1, padx=5, pady=5)

        boton_cr = tk.Button(frame, text="Crear Ticket", command=self.gestor.crear_ticket)
        boton_cr.grid(row=3, column=1, pady=10, sticky="e")


    def botones(self):
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
        boton_modificar = tk.Button(frame_superior, text="Modificar Tickets", command="")
        boton_modificar.grid(row=1, column=3, padx=10, pady=10)
        boton_eliminar = tk.Button(frame_superior, text="Eliminar Tickets", command="")
        boton_eliminar.grid(row=1, column=4, padx=10, pady=10)


    def formulario_gestor(self):
        frame = tk.LabelFrame(self.master, text="Usuario Gestor", padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre = tk.Entry(frame, width=50)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Apellido:").grid(row=1, column=0, sticky="w")
        self.apellido = tk.Entry(frame, width=50)
        self.apellido.grid(row=1, column=1, padx=5, pady=5)

        boton_cr_ges = tk.Button(frame, text="Crear Gestor", command=self.guardar_gestor)
        boton_cr_ges.grid(row=3, column=1, pady=10)

    def guardar_gestor(self):
        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()

        ok, mensaje = self.usuario.crear_gestor(nombre, apellido)

        if ok:
            self.messagebox.showinfo("OK", mensaje)
        else:
            self.messagebox.showerror("Error", mensaje)






