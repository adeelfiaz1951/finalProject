import tkinter as tk
from tkinter import simpledialog,messagebox

class gestionDialog(simpledialog.Dialog): #Contiene clases y funciones convenientes para crear diálogos modales
    
    # Mostramos los datos iniciales si existen
    def __init__(self, parent, title="Gestion de Biblioteca", initial_data=None):
        self.initial_data = initial_data or {"name": "", "email": "", "phone": ""}
        super().__init__(parent, title)
    
    # Método que construye la ventana de diálogo
    def body(self, master):
        # Etiquetas de los campos
        tk.Label(master, text="Nombre:").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Correo Electrónico:").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="Teléfono:").grid(row=2, column=0, sticky="e")

        # Campos de entrada de texto
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=1, column=1)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=2, column=1)

        # Rellenar si vienen datos iniciales (para editar)
        self.name_entry.insert(0, self.initial_data["name"])
        self.email_entry.insert(0, self.initial_data["email"])
        self.phone_entry.insert(0, self.initial_data["phone"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.name_entry

    def validate(self):
        # Validar campos no vacíos
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not email or not phone:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return False
        return True

    # Método que se ejecuta cuando el usuario pulsa "Aceptar"
    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip()
        }
