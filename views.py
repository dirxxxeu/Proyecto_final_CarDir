# Capa de Interfaz Gráfica (Tkinter / TTK)

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askokcancel

from models import TicketManager, Usuario

class Menu:
    """Pantalla principal"""
    def __init__(self, master):
        self.master = master

        self.ticket_manager = TicketManager()   # Lógica separada

        self.master.title("CarDir HelpDesk")

        # ----- CENTRAR LA VENTANA PRINCIPAL -----
        ancho = 900
        alto = 800

        pantalla_ancho = self.master.winfo_screenwidth()
        pantalla_alto = self.master.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Vista inicial
        self.metricas()
        self.botones()

    def metricas(self):
        """Hace un recuento de los tickets"""
        self.frame_metricas = tk.LabelFrame(self.master, text="Métricas", padx=10, pady=10)
        self.frame_metricas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Obtener métricas desde el modelo
        abiertos, proceso, cerrados = self.ticket_manager.obtener_metricas()

        # Mostrar métricas
        tk.Label(self.frame_metricas, text=f"Tickets Abiertos: {abiertos}").grid(row=0, column=0, sticky="w")
        tk.Label(self.frame_metricas, text=f"Tickets En Proceso: {proceso}").grid(row=1, column=0, sticky="w")
        tk.Label(self.frame_metricas, text=f"Tickets Cerrados: {cerrados}").grid(row=2, column=0, sticky="w")

    # ---------------- TREEVIEW ----------------
    def frame_treeview(self):
        """Es el tree o tabla donde muestra los tickets abiertos"""
        self.cerrar_frames_abiertos()

        self.frame_tree = tk.Frame(self.master)
        self.frame_tree.grid(row=3, column=0, sticky="nsew")

        self.master.grid_rowconfigure(3, weight=1)
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
        """Mediante el ciclo hace una busqueda y los pinta en el tree o tabla"""
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

    # ---------------- CREAR TICKET ----------------
    def formulario_crear(self):
        """Formulario para crear ticket"""
        self.cerrar_frames_abiertos()

        self.frame_crear = tk.LabelFrame(self.master, text="Crear Ticket", padx=10, pady=10)
        self.frame_crear.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

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
        """Crea el ticket con los datos del formulario"""
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

        self.frame_crear.destroy()

    # ---------------- BUSCAR TICKET ----------------
    def formulario_buscar(self):
        """Formulario de buscar ticket"""
        self.cerrar_frames_abiertos()

        self.frame_buscar = tk.LabelFrame(self.master, text="Buscar Ticket", padx=10, pady=10)
        self.frame_buscar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(self.frame_buscar, text="ID del Ticket:").grid(row=0, column=0, sticky="w")
        self.buscar_id = tk.Entry(self.frame_buscar, width=20)
        self.buscar_id.grid(row=0, column=1, padx=5, pady=5)

        boton_buscar = tk.Button(self.frame_buscar, text="Buscar", command=self.ejecutar_busqueda)
        boton_buscar.grid(row=1, column=1, pady=10, sticky="e")

    def ejecutar_busqueda(self):
        """Ejecuta la busqueda del ticket"""
        id_ticket = self.buscar_id.get().strip()

        if not id_ticket.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número")
            return

        ticket = self.ticket_manager.buscar_ticket(int(id_ticket))

        if ticket:
            messagebox.showinfo(
                "Ticket encontrado",
                f"ID: {ticket['id_ticket']}\n"
                f"Usuario: {ticket['usuario']}\n"
                f"Descripción: {ticket['descripcion']}\n"
                f"Categoría: {ticket['categoria']}\n"
                f"Prioridad: {ticket['prioridad']}\n"
                f"Estado: {ticket['estado']}"
            )
        else:
            messagebox.showerror("No encontrado", "No existe un ticket con ese ID")

        self.frame_buscar.destroy()

    # ---------------- ELIMINAR TICKET ----------------
    def formulario_eliminar(self):
        """Formulario de eliminar ticket """
        self.cerrar_frames_abiertos()

        self.frame_eliminar = tk.LabelFrame(self.master, text="Eliminar Ticket", padx=10, pady=10)
        self.frame_eliminar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(self.frame_eliminar, text="ID del Ticket:").grid(row=0, column=0, sticky="w")
        self.eliminar_id = tk.Entry(self.frame_eliminar, width=20)
        self.eliminar_id.grid(row=0, column=1, padx=5, pady=5)

        boton_eliminar = tk.Button(self.frame_eliminar, text="Eliminar", command=self.ejecutar_eliminar)
        boton_eliminar.grid(row=1, column=1, pady=10, sticky="e")

    def ejecutar_eliminar(self):
        id_ticket = self.eliminar_id.get().strip()

        if not id_ticket.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número")
            return

        if askokcancel("Eliminar", f"Eliminar Ticket {id_ticket}"):
            eliminado = self.ticket_manager.eliminar_ticket(int(id_ticket))
            if eliminado:
                messagebox.showerror("Eliminado", f"Ticket {id_ticket} eliminado correctamente")
            else:
                messagebox.showerror("Error", f"No existe un ticket con el ID {id_ticket}")


        self.frame_eliminar.destroy()

    # ---------------- MODIFICAR TICKET ----------------
    def formulario_modificar(self):
        self.cerrar_frames_abiertos()

        self.frame_modificar = tk.LabelFrame(self.master, text="Modificar Ticket", padx=10, pady=10)
        self.frame_modificar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(self.frame_modificar, text="ID del Ticket:").grid(row=0, column=0, sticky="w")
        self.modificar_id = tk.Entry(self.frame_modificar, width=20)
        self.modificar_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_modificar, text="Nuevo Estado:").grid(row=1, column=0, sticky="w")
        self.nuevo_estado = ttk.Combobox(self.frame_modificar, values=["Abierto", "En Proceso", "Cerrado"])
        self.nuevo_estado.grid(row=1, column=1, padx=5, pady=5)

        boton_modificar = tk.Button(self.frame_modificar, text="Modificar", command=self.ejecutar_modificar)
        boton_modificar.grid(row=2, column=1, pady=10, sticky="e")

    def ejecutar_modificar(self):
        id_ticket = self.modificar_id.get().strip()
        estado = self.nuevo_estado.get().strip()

        if not id_ticket.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número")
            return

        if not estado:
            messagebox.showerror("Error", "Debe seleccionar un estado")
            return

        modificado = self.ticket_manager.actualizar_estado(int(id_ticket), estado)

        if modificado:
            messagebox.showinfo("Modificado", f"Ticket {id_ticket} actualizado a '{estado}'")
        else:
            messagebox.showerror("Error", "No existe un ticket con ese ID")

        self.frame_modificar.destroy()

    # ---------------- CERRAR FRAMES ----------------
    def cerrar_frames_abiertos(self):
        """Cierra cualquier frame abierto en la vista excepto métricas."""
        for frame_name in ["frame_crear", "frame_buscar", "frame_eliminar", "frame_modificar", "frame_tree"]:
            if hasattr(self, frame_name):
                try:
                    getattr(self, frame_name).destroy()
                except:
                    pass

    # ---------------- BOTONES SUPERIORES ----------------
    def botones(self):

        frame_superior = tk.LabelFrame(self.master)
        frame_superior.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        etiqueta = tk.Label(frame_superior, text="CarDir HelpDesk 1.0", font=("Arial", 16))
        etiqueta.grid(row=0, column=0, padx=10, pady=10)


        tk.Button(frame_superior, text="Listar Tickets", command=self.mostrar_tickets).grid(row=1, column=1, padx=10)
        tk.Button(frame_superior, text="Nuevo Ticket", command=self.formulario_crear).grid(row=1, column=2, padx=10)
        tk.Button(frame_superior, text="Buscar Ticket", command=self.formulario_buscar).grid(row=1, column=3, padx=10)
        tk.Button(frame_superior, text="Modificar Ticket", command=self.formulario_modificar).grid(row=1, column=4, padx=10)
        tk.Button(frame_superior, text="Eliminar Ticket", command=self.formulario_eliminar).grid(row=1, column=5, padx=10)
