# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Usuario, Ticket, TicketManager

class Menu:
    def __init__(self, master):
        self.master = master
        self.master.title("CarDir HelpDesk")
        self.master.geometry("900x600")

        self.manager = TicketManager()
        self.usuario_actual = Usuario("Dirceu", "Lozano", id_usuario=1)

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_tickets()

    # ---------------- FORMULARIO ----------------
    def crear_formulario(self):
        frame = tk.LabelFrame(self.master, text="Crear Ticket", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Descripción:").grid(row=0, column=0, sticky="w")
        self.descripcion = tk.Entry(frame, width=50)
        self.descripcion.grid(row=0, column=1)

        tk.Label(frame, text="Categoría:").grid(row=1, column=0, sticky="w")
        self.categoria = ttk.Combobox(frame, values=["Hardware", "Software", "Red", "Otro"])
        self.categoria.grid(row=1, column=1)

        tk.Label(frame, text="Prioridad:").grid(row=2, column=0, sticky="w")
        self.prioridad = ttk.Combobox(frame, values=["Baja", "Media", "Alta"])
        self.prioridad.grid(row=2, column=1)

        tk.Button(frame, text="Crear Ticket", command=self.crear_ticket).grid(row=3, column=1, pady=10)

    # ---------------- TABLA ----------------
    def crear_tabla(self):
        self.tabla = ttk.Treeview(self.master, columns=("ID", "Usuario", "Descripción", "Categoría", "Prioridad", "Estado"), show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)

        tk.Button(self.master, text="Eliminar Ticket Seleccionado", command=self.eliminar_ticket).pack(pady=10)

    # ---------------- CRUD ----------------
    def crear_ticket(self):
        descripcion = self.descripcion.get()
        categoria = self.categoria.get()
        prioridad = self.prioridad.get()

        if not descripcion or not categoria or not prioridad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        nuevo_id = len(self.manager.tickets) + 1
        ticket = Ticket(nuevo_id, self.usuario_actual, descripcion, categoria, prioridad)

        self.manager.crear_ticket(ticket)
        self.cargar_tickets()

        messagebox.showinfo("OK", "Ticket creado correctamente")

    def cargar_tickets(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for t in self.manager.listar_tickets():
            self.tabla.insert("", "end", values=(t["id_ticket"], t["usuario"], t["descripcion"], t["categoria"], t["prioridad"], t["estado"]))

    def eliminar_ticket(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un ticket")
            return

        valores = self.tabla.item(seleccionado)["values"]
        id_ticket = valores[0]

        if self.manager.eliminar(id_ticket):
            self.cargar_tickets()
            messagebox.showinfo("OK", "Ticket eliminado")
        else:
            messagebox.showerror("Error", "No se pudo eliminar")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root)
    root.mainloop()
