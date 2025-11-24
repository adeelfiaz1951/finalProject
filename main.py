<<<<<<< HEAD
from dataManager import crea_tablas
import tkinter as tk
from interface.login_UI import Login_ui

if __name__ == '__main__':
    crea_tablas()
    root = tk.Tk()
    Login_ui(root)
    root.mainloop()
=======
# Importamos los módulos necesarios
from biblio_dialog import BibliotecaApp

# -------------------------------
#        EJECUCIÓN PRINCIPAL
# -------------------------------

if __name__ == "__main__":
    app = BibliotecaApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

>>>>>>> 848af4fb687f16f569bf97e1b7f09164c57f8572
