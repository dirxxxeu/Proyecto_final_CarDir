import json
import os

class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

class Usuario(Persona):
    def __init__(self, nombre, apellido, id_usuario=0):
        super().__init__(nombre, apellido)
        self.id_usuario = id_usuario

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Ticket:
    def __init__(self, id_ticket, usuario, descripcion, categoria, prioridad, estado="Abierto"):
        self.id_ticket = id_ticket
        self.usuario = usuario
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.estado = estado

    def to_dict(self):
        return {
            "id_ticket": self.id_ticket,
            "usuario": str(self.usuario),
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "estado": self.estado
        }

class TicketManager:
    def __init__(self, archivo="tickets.json"):
        self.archivo = archivo
        self.tickets = []
        self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.tickets = json.load(f)
        else:
            self.tickets = []

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.tickets, f, indent=4, ensure_ascii=False)

    def crear_ticket(self, usuario, descripcion, categoria, prioridad):
        nuevo_id = len(self.tickets) + 1
        ticket = Ticket(nuevo_id, usuario, descripcion, categoria, prioridad)
        self.tickets.append(ticket.to_dict())
        self.guardar()
        return ticket

    def listar_tickets(self):
        return self.tickets

    def obtener_metricas(self):
        abiertos = sum(1 for t in self.tickets if t["estado"] == "Abierto")
        proceso = sum(1 for t in self.tickets if t["estado"] == "En Proceso")
        cerrados = sum(1 for t in self.tickets if t["estado"] == "Cerrado")

        return abiertos, proceso, cerrados

    def buscar_ticket(self, id_ticket):
        for t in self.tickets:
            if t["id_ticket"] == id_ticket:
                return t
        return None

    def actualizar_estado(self, id_ticket, nuevo_estado):
        ticket = self.buscar_ticket(id_ticket)
        if ticket:
            ticket["estado"] = nuevo_estado
            self.guardar()
            return True
        return False

    def eliminar_ticket(self, id_ticket):
        inicial = len(self.tickets)
        self.tickets = [t for t in self.tickets if t["id_ticket"] != id_ticket]
        self.guardar()
        return len(self.tickets) < inicial
