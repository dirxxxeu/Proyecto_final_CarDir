# Capa de Interfaz Gráfica (Tkinter / TTK)

import tkinter as tk
from tkinter import ttk, messagebox
from models import TicketManager, Usuario

class Menu:
    """Pantalla principal"""
    def __init__(self, master):
        self.master = master

        self.ticket_manager = TicketManager()   # ← gestor de tickets

        self.master.title("CarDir HelpDesk")

        # ----- CENTRAR LA VENTANA PRINCIPAL -----
        ancho = 1080
        alto = 800

        pantalla_ancho = self.master.winfo_screenwidth()
        pantalla_alto = self.master.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")

        #self.frame_treeview()
        self.botones()
        #self.formulario_crear()

    def frame_treeview(self):
        self.frame_tree = tk.Frame(self.master)
        self.frame_tree.grid(row=2, column=0, sticky="nsew")

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.columnas = ("ID", "Usuario", "Descripción", "Categoría", "Prioridad", "Estado")
        self.tree = ttk.Treeview(self.frame_tree, columns=self.columnas, show="headings")

        for col in self.columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.frame_tree.grid_rowconfigure(0, weight=1)
        self.frame_tree.grid_columnconfigure(0, weight=1)

    def mostrar_tickets(self):
        self.frame_treeview()
        for item in self.tree.get_children():
            self.tree.delete(item)

        tickets = self.ticket_manager.listar_tickets()

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
        self.frame_tree.destroy()
        self.frame_crear = tk.LabelFrame(self.master, text="Crear Ticket", padx=10, pady=10)
        self.frame_crear.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(self.frame_crear, text="Usuario:").grid(row=0, column=0, sticky="w")
        self.usuario_nombre = tk.Entry(self.frame_crear, width=40)
        self.usuario_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_crear, text="Apellido:").grid(row=1, column=0, sticky="w")
        self.usuario_apellido = tk.Entry(self.frame_crear, width=40)
        self.usuario_apellido.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_crear, text="Descripción:").grid(row=2, column=0, sticky="w")
        self.descripcion = tk.Entry(self.frame_crear, width=50)
        self.descripcion.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame_crear, text="Categoría:").grid(row=3, column=0, sticky="w")
        self.categoria = ttk.Combobox(self.frame_crear, values=["Hardware", "Software", "Red", "Otro"])
        self.categoria.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.frame_crear, text="Prioridad:").grid(row=4, column=0, sticky="w")
        self.prioridad = ttk.Combobox(self.frame_crear, values=["Baja", "Media", "Alta"])
        self.prioridad.grid(row=4, column=1, padx=5, pady=5)

        boton_cr = tk.Button(self.frame_crear, text="Crear Ticket", command=self.crear_ticket)
        boton_cr.grid(row=5, column=1, pady=10, sticky="e")

    def crear_ticket(self):
        self.frame_tree.destroy()

        nombre = self.usuario_nombre.get().strip()
        apellido = self.usuario_apellido.get().strip()
        descripcion = self.descripcion.get().strip()
        categoria = self.categoria.get().strip()
        prioridad = self.prioridad.get().strip()

        if not nombre or not apellido or not descripcion or not categoria or not prioridad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        usuario = Usuario(nombre, apellido)

        self.ticket_manager.crear_ticket(usuario, descripcion, categoria, prioridad)

        messagebox.showinfo("OK", "Ticket creado correctamente")

        #  Aquí se destruye el formulario
        self.frame_crear.destroy()

        # Opcional: refrescar la tabla
        #self.mostrar_tickets()

    def formulario_buscar(self):
        # ----- FORMULARIO BUSCAR -----
        self.frame_buscar = tk.LabelFrame(self.master, text="Buscar Ticket", padx=10, pady=10)
        self.frame_buscar.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(self.frame_buscar, text="ID del Ticket:").grid(row=0, column=0, sticky="w")
        self.buscar_id = tk.Entry(self.frame_buscar, width=20)
        self.buscar_id.grid(row=0, column=1, padx=5, pady=5)

        boton_buscar = tk.Button(self.frame_buscar, text="Buscar", command=self.ticket_manager.buscar_ticket)
        boton_buscar.grid(row=1, column=1, pady=10, sticky="e")

    def botones(self):
        frame_superior = tk.LabelFrame(self.master)
        frame_superior.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        etiqueta = tk.Label(frame_superior, text="CarDir HelpDesk 1.0", font=("Arial", 16))
        etiqueta.grid(row=0, column=0, padx=10, pady=10)

        separator = ttk.Separator(self.master, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)

        boton_listar = tk.Button(frame_superior, text="Listar Tickets", command=self.mostrar_tickets)
        boton_listar.grid(row=1, column=1, padx=10, pady=10)

        boton_nuevo =tk.Button(frame_superior,text="Nuevo Ticket", command=self.formulario_crear)
        boton_nuevo.grid(row=1, column=2, padx=10, pady=10)

        boton_busqueda = tk.Button(frame_superior, text="Buscar Ticket", command=self.formulario_buscar)
        boton_busqueda.grid(row=1, column=3, padx=10, pady=10)

        boton_eliminar =tk.Button(frame_superior, text="Eliminar Ticket", command="")
        boton_eliminar.grid(row=1, column=4, padx=10, pady=10)