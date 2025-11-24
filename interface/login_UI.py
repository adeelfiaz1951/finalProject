import tkinter as tk
from tkinter import messagebox
from modulos.usuario import Usuario

from interface.app import App



class Login_ui:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('400x200')

        tk.Label(root, text="Usuario:").pack(pady=(10))
        self.usuario = tk.Entry(root)
        self.usuario.pack()
        tk.Label(root, text="Contrasena:").pack(pady=(6))
        self.password = tk.Entry(root, show='*')
        self.password.pack()


        tk.Button(root, text="Iniciar sesión", command=self.iniciar).pack(pady=10)
        tk.Button(root, text="Registrarse", command=self.abrir_registro).pack()

    def iniciar(self):
        res = Usuario.verificar(self.usuario.get().strip(), self.password.get().strip())
        if res:
            usuario_id, usuario = res
            messagebox.showinfo("OK", f"Bienvenido {usuario}")
            self.root.destroy()
            ventana = tk.Tk()
            App(ventana, usuario_id = usuario_id, usuario=usuario,)
            ventana.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_registro(self):
        from interface.registrar_UI import Register_ui
        Register_ui(tk.Toplevel(self.root))
