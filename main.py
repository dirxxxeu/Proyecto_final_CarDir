# Punto de Entrada de la Aplicación


import tkinter as tk
from models import Usuario, TicketManager
from views import Menu

if __name__ == "__main__":
    #usuario_actual = Usuario("Dirceu", "Lozano")
    #gestor = TicketManager()

    # Ejemplo de creación de ticket
    #.crear_ticket(, "No funciona el WiFi", "Red", "Alta")

    root = tk.Tk()
    app = Menu.formulario_gestor(root)
    root.mainloop()
