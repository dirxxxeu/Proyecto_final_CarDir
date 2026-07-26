import tkinter as tk

import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Visor de Estudiantes")
ventana.geometry("600x300")

# Definir las columnas de la tabla
columnas = ("id", "nombre", "apellido", "nota")
tree = ttk.Treeview(ventana, columns=columnas, show="headings")

# Configurar los encabezados
tree.heading("id", text="ID")
tree.heading("nombre", text="Nombre")
tree.heading("apellido", text="Apellido")
tree.heading("nota", text="Nota")

# Configurar el ancho de las columnas
tree.column("id", width=50, anchor=tk.CENTER)
tree.column("nombre", width=150)
tree.column("apellido", width=150)
tree.column("nota", width=80, anchor=tk.CENTER)

# Datos de ejemplo
datos_estudiantes = [
    (1, "Ana", "García", 8.5),
    (2, "Luis", "Pérez", 7.0),
    (3, "Marta", "Ruiz", 9.2),
    (4, "Carlos", "Sánchez", 6.8),
    (5, "Sofía", "Martín", 9.5)
]

# Insertar datos en el Treeview
for i, estudiante in enumerate(datos_estudiantes):
    tree.insert("", tk.END, iid=i, values=estudiante)

# Scrollbar vertical
scrollbar_y = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_y.set)

# Empaquetar
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

ventana.mainloop()
