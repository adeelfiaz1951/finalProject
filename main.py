# Importamos los módulos necesarios
from biblio_dialog import BibliotecaApp

# -------------------------------
#        EJECUCIÓN PRINCIPAL
# -------------------------------

if __name__ == "__main__":
    app = BibliotecaApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

