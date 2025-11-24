import tkinter as tk
from tkinter import messagebox, ttk
from dataManager import DataManager
from libros import Libro


ventana = tk.Tk()
class biblioteca(ventana):
# propidads de ventana
    ventana.title('Gestión de Biblioteca')
    ventana.geometry('800x600')

    tk.Label(self, text="isbn:").pack(pady=5)
    self.isbn_entry = tk.Entry(self)
    self.isbn_entry.pack(pady=5)
    isbn = self.isbn_entry.get()

    tk.Label(self, text="titulo:").pack(pady=5)
    self.titulo_entry = tk.Entry(self)
    self.titulo_entry.pack(pady=5)
    titulo = self.titulo_entry.get()

    tk.Label(self, text="autor_id:").pack(pady=5)
    self.autor_id_entry = tk.Entry(self)
    self.autor_id_entry.pack(pady=5)

    autor_id = self.autor_id_entry.get()

    crear_libro = Libro.nuevo_libro(isbn,titulo, autor_id)
    crear_libro = DataManager.anadir_libro(isbn,titulo, autor_id)

    if crear_libro:
        messagebox.INFO("Correcto", "Libro creado")
    else:
        messagebox.ERROR("Error", "Libro no creado")
    
    


    ventana.mainloop()
# class BibliotecaApp(ventana):
#     """Ventana principal"""
#     def __init__(self):
#         super().__init__()
#         self.title("Sistema de Gestión de Biblioteca")
#         self.geometry("800x600")
        
#         # Inicilacion DataManager
#         self.data_manager = DataManager()
#         self.current_user = None # Stores the logged-in username
        
#         # Container to hold pages (Login or Main Dashboard)
#         self.container = tk.Frame(self)
#         self.container.pack(fill="both", expand=True)
        
#         self.show_login_page()

#     def show_login_page(self):
#         """Displays the login window."""
#         self.clear_container()
#         login_frame = LoginWindow(self.container, self)
#         login_frame.pack(fill="both", expand=True)

#     def show_register_page(self):
#         """Displays the registration window."""
#         self.clear_container()
#         register_frame = RegisterWindow(self.container, self)
#         register_frame.pack(fill="both", expand=True)

#     def show_main_dashboard(self, username):
#         """Displays the main application dashboard after successful login."""
#         self.current_user = username
#         self.title(f"Sistema de Gestión de Biblioteca - Usuario: {username}")
#         self.clear_container()
#         MainDashboard(self.container, self).pack(fill="both", expand=True)
        
#     def clear_container(self):
#         """Removes all widgets from the main container."""
#         for widget in self.container.winfo_children():
#             widget.destroy()

#     def on_closing(self):
#         """Handles application closing, ensuring database connection is closed."""
#         self.data_manager.cerramos()
#         self.destroy()

# # --- Login and Registration Windows ---

# class LoginWindow(tk.Frame):
#     """Frame for user login."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
        
#         # --- Widgets ---
#         tk.Label(self, text="INICIAR SESIÓN", font=('Arial', 18, 'bold')).pack(pady=20)
        
#         tk.Label(self, text="Usuario:").pack(pady=5)
#         self.user_entry = tk.Entry(self)
#         self.user_entry.pack(pady=5)
        
#         tk.Label(self, text="Contraseña:").pack(pady=5)
#         self.pass_entry = tk.Entry(self, show="*")
#         self.pass_entry.pack(pady=5)
        
#         tk.Button(self, text="Login", command=self.login).pack(pady=10)
        
#         tk.Button(self, text="Registrar", command=controller.show_register_page).pack(pady=5)

#     def login(self):
#         username = self.user_entry.get()
#         password = self.pass_entry.get()
        
#         if not username or not password:
#             messagebox.showerror("Error de Login", "Todos los campos son obligatorios.")
#             return

#         # Call DataManager method
#         if self.controller.data_manager.verificar(username, password):
#             messagebox.showinfo("Éxito", "¡Login exitoso!")
#             self.controller.show_main_dashboard(username)
#         else:
#             messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

# class RegisterWindow(tk.Frame):
#     """Frame for user registration."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
        
#         # --- Widgets ---
#         tk.Label(self, text="REGISTRAR NUEVO USUARIO", font=('Arial', 18, 'bold')).pack(pady=20)
        
#         tk.Label(self, text="Usuario:").pack(pady=5)
#         self.user_entry = tk.Entry(self)
#         self.user_entry.pack(pady=5)
        
#         tk.Label(self, text="Email:").pack(pady=5)
#         self.email_entry = tk.Entry(self)
#         self.email_entry.pack(pady=5)
        
#         tk.Label(self, text="Contraseña:").pack(pady=5)
#         self.pass_entry = tk.Entry(self, show="*")
#         self.pass_entry.pack(pady=5)
        
#         tk.Button(self, text="Registrar", command=self.register).pack(pady=10)
        
#         tk.Button(self, text="Volver a Login", command=controller.show_login_page).pack(pady=5)
        
#     def register(self):
#         username = self.user_entry.get()
#         email = self.email_entry.get()
#         password = self.pass_entry.get()
        
#         if not all([username, email, password]):
#             messagebox.showerror("Error de Registro", "Todos los campos son obligatorios.")
#             return
        
#         # Call DataManager method
#         result = self.controller.data_manager.registrar(username, email, password)
#         messagebox.showinfo("Resultado de Registro", result)
        
#         if "correctamente" in result:
#             self.controller.show_login_page()

# # --- Main Dashboard ---

# class MainDashboard(ttk.Frame):
#     """Main application frame with tabs for different functionalities."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
        
#         notebook = ttk.Notebook(self)
#         notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
#         # Create tabs
#         libros_tab = LibrosTab(notebook, controller)
#         autores_tab = AutoresTab(notebook, controller)
#         prestamos_tab = PrestamosTab(notebook, controller)
        
#         notebook.add(libros_tab, text="Gestión de Libros")
#         notebook.add(autores_tab, text="Gestión de Autores")
#         notebook.add(prestamos_tab, text="Gestión de Préstamos")
        
#         tk.Label(self, text=f"Usuario Activo: {controller.current_user}").pack(side="left", padx=10, pady=5)
#         tk.Button(self, text="Cerrar Sesión", command=controller.show_login_page).pack(side="right", padx=10, pady=5)

# # --- Tab Classes (Functionality specific) ---

# class LibrosTab(tk.Frame):
#     """Tab for managing books (CRUD)."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
        
#         # Treeview to display books
#         self.tree = ttk.Treeview(self, columns=("ISBN", "Título", "Autor", "Género", "Año"), show="headings")
#         self.tree.heading("ISBN", text="ISBN")
#         self.tree.heading("Título", text="Título")
#         self.tree.heading("Autor", text="Autor")
#         self.tree.heading("Género", text="Género")
#         self.tree.heading("Año", text="Año")
        
#         self.tree.column("ISBN", width=100)
#         self.tree.column("Título", width=200)
#         self.tree.column("Autor", width=150)
#         self.tree.column("Género", width=100)
#         self.tree.column("Año", width=50)
        
#         self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        
#         # Button frame
#         btn_frame = tk.Frame(self)
#         btn_frame.pack(pady=10)
        
#         tk.Button(btn_frame, text="Añadir Libro", command=self.open_add_book_window).pack(side="left", padx=5)
#         tk.Button(btn_frame, text="Recargar Lista", command=self.load_books).pack(side="left", padx=5)
        
#         self.load_books() # Initial data load

#     def load_books(self):
#         """Loads book data into the Treeview."""
#         # Clear existing data
#         for item in self.tree.get_children():
#             self.tree.delete(item)
            
#         # Fetch new data
#         books = self.controller.data_manager.load_libros()
        
#         # Insert data
#         for book in books:
#             self.tree.insert("", tk.END, values=book)

#     def open_add_book_window(self):
#         """Opens a new window for adding a book."""
#         AddBookWindow(self.controller, self)


# class AddBookWindow(tk.Toplevel):
#     """Toplevel window for adding a new book."""
#     def __init__(self, controller, parent_tab):
#         super().__init__(controller)
#         self.title("Añadir Nuevo Libro")
#         self.geometry("300x350")
#         self.controller = controller
#         self.parent_tab = parent_tab
#         self.transient(controller) # Keep window on top of main app
#         self.grab_set() # Modal window
        
#         # Get authors for dropdown
#         self.authors = self.controller.data_manager.load_autor()
#         self.author_names = {name: id for id, name in self.authors}
#         self.selected_author = tk.StringVar(self)
        
#         # --- Widgets (ISBN, Título, Autor, Género, Año) ---
        
#         # Helper to create labeled entry
#         def create_entry(label_text, row):
#             tk.Label(self, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
#             entry = tk(self)
#             entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
#             return entry

#         self.isbn_entry = create_entry("ISBN:", 0)
#         self.title_entry = create_entry("Título:", 1)
#         self.genre_entry = create_entry("Género:", 3)
#         self.year_entry = create_entry("Año Publ.:", 4)
        
#         # Autor Dropdown
#         tk.Label(self, text="Autor:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
#         if self.author_names:
#             ttk.Combobox(self, textvariable=self.selected_author, 
#                          values=list(self.author_names.keys()), state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
#         else:
#              tk.Label(self, text="No hay autores").grid(row=2, column=1, padx=5, pady=5, sticky="ew")

#         # Submit button
#         tk.Button(self, text="Guardar Libro", command=self.save_book).grid(row=5, column=0, columnspan=2, pady=15)

#     def save_book(self):
#         isbn = self.isbn_entry.get().strip()
#         title = self.title_entry.get().strip()
#         genre = self.genre_entry.get().strip()
#         year = self.year_entry.get().strip()
#         author_name = self.selected_author.get()

#         if not author_name:
#             messagebox.showerror("Error", "Debe seleccionar un autor.")
#             return

#         author_id = self.author_names.get(author_name)
        
#         # Simple year validation
#         anio_publicacion = None
#         if year:
#             try:
#                 anio_publicacion = int(year)
#             except ValueError:
#                 messagebox.showerror("Error", "El año debe ser un número entero.")
#                 return
        
#         # Call DataManager method
#         result = self.controller.data_manager.anadir_libro(isbn, title, author_id, genre, anio_publicacion)
        
#         messagebox.showinfo("Resultado", result)
        
#         if "correctamente" in result:
#             self.parent_tab.load_books()
#             self.destroy()

# class AutoresTab(tk.Frame):
#     """Placeholder Tab for Authors."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         tk.Label(self, text="Gestión de Autores - Implementación pendiente", font=('Arial', 14)).pack(pady=20)
#         tk.Button(self, text="Añadir Autor (Ejemplo)", command=self.add_author_example).pack(pady=10)

#     def add_author_example(self):
#         # Example call to add_autor
#         result = self.controller.data_manager.anadir_autor("Nuevo Autor Ejemplo")
#         messagebox.showinfo("Autor", result)

# class PrestamosTab(tk.Frame):
#     """Placeholder Tab for Loans."""
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         tk.Label(self, text="Gestión de Préstamos - Implementación pendiente", font=('Arial', 14)).pack(pady=20)


