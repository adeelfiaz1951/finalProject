
from dataManager import crea_tablas
import tkinter as tk
from interface.login_UI import Login_ui

if __name__ == '__main__':
    crea_tablas()
    root = tk.Tk()
    Login_ui(root)
    root.mainloop()
