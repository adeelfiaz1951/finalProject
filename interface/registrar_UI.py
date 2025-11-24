import tkinter as tk
from tkinter import messagebox
from modulos.usuario import Usuario

class Register_ui:
    def __init__(self, root):
        self.root = root
        root.title("Registro")
        root.geometry("500x250")

        tk.Label(root, text="Usuario:").pack(pady=(10))
        self.usuario = tk.Entry(root)
        self.usuario.pack()

        tk.Label(root, text="Email:").pack(pady=(6))
        self.email = tk.Entry(root)
        self.email.pack()

        tk.Label(root, text="Contrasena:").pack(pady=(6))
        self.password = tk.Entry(root, show='*')
        self.password.pack()

        tk.Button(root, text="Crear usuario", command=self.crear).pack(pady=12)

    def crear(self):
        crea_user = Usuario(self.usuario.get().strip(), self.email.get().strip(), self.password.get().strip())
        res = crea_user.registrar()
        if res is True:
            messagebox.showinfo("OK", "Usuario creado")
            self.root.destroy()
        else:
            messagebox.showerror("Error", res)
