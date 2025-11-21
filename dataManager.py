import sqlite3,  datetime, bcrypt

        
class DataManager:
    def __init__(self, root):
        self.root = root
        self.root.titulo('Gestion de Biblioteca')

    # conexion a la base de datos
        self.conexion = sqlite3.connect("biblio.db") # crea el archivo si no existe
        self.cursor = self.conexion.cursor()
        self.crear_tablas() # crea la tabla contactos si no existe
        
        
    # Crea tabla usuario si no existe
    def crear_tablas(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                email as TEXT,
                password BLOB
            )                    
            
            """)
            # Tabla de autores
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS autores (
                    autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL
                )
            ''')
            # Tabla de libros
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS libros (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor_id INTEGER NOT NULL,
                    genre TEXT,
                    anio_publicacion INTEGER,
                    FOREIGN KEY (autor_id) REFERENCES autores(autor_id)
                )
            ''')
            # Tabla de prestamos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    prestado_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn_libro TEXT NOT NULL,
                    nombre_usuario TEXT NOT NULL,
                    fecha_prestado DATE NOT NULL,
                    fecha_devolucion DATE,
                    FOREIGN KEY (isbn_libro) REFERENCES libros(isbn)
                )
            ''')
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f'Error con la base de datos {e}')
            
    # Registrar  usario  
    def registrar(self, usuario, email, password):
        conexion = sqlite3.connect('biblio.db')
        cursor = conexion.cursor()
    
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            conexion = sqlite3.connect('biblio.db')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, email, password) VALUES (?, ?, ?)", (usuario, email, hashed))
            conexion.commit()
            print(f'usuario {usuario} registrado')
        except sqlite3.IntegrityError:
            print(f'El usuario {usuario} ya esta registrado.')
            
    # validar inicio de sesión
    def verificar(self,usuario, password):
    
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE usuario=?,", (usuario,))
        fila = cursor.fetchone()
        if fila:
            return bcrypt.checkpw(password.encode(), fila[0])
        else:
            return False
        
    # isn valoidacion
    def validar_isbn(self, isbn):
        if len(isbn) == 10 or len(isbn) == 13 and isbn.isdigit():
            return True
    
     # Cargar autores desde DB
    # -------------------------------
    def load_autor(self):
        self.cursor.execute("SELECT * FROM autores")  # Select todo de autores
        self.autor = self.cursor.fetchall()  # lista de tuplas (id, nombre)
    # anadir autor
    def anadir_autor(self, nombre):
        if nombre:
            self.cursor.execute("INSERT INTO autores (nombre) Values(?,)", (nombre))
            self.conexion.commit()
            return 'El autor anadir correctamente'
        else:
            return 'Autor ya existe'

    # anadir libro
    def anadir_libro(self, isbn, titulo, autor_id, genre, anio_publicacion):
        if not all([isbn, titulo, autor_id]): return "Error: ISBN, título y autor son obligatorios."
        if not self.validar_isbn(isbn): return "Error: Formato ISBN no válido (10 o 13 dígitos)."
        try:
            self.cursor.execute("INSERT INTO libros (isbn, titulo, autor_id, genre, anio_publicacion) VALUES (?, ?, ?, ?, ?)",
                                (isbn, titulo, autor_id, genre, anio_publicacion))
            self.conexion.commit()
            return "Libro añadido ."
        except sqlite3.IntegrityError:
            return "Error: Libro con este ISBN ya existe."
        # cargar libros de base de datos
    def load_libros(self):
        self.cursor.execute('''
            SELECT libros.isbn, libros.titulo, autores.nombre, libros.genre, libros.anio_publicacion, libros.autor_id
            FROM libros 
            JOIN autores ON libros.autor_id = autores.autor_id
        ''')
        return self.cursor.fetchall()
        # cargar libros disponibles
    def load_libros_disponibles(self):
        self.cursor.execute('''
            SELECT libros.isbn, libros.titulo, autores.nombre, libros.genre, libros.anio_publicacion
            FROM libros 
            JOIN autores ON libros.autor_id = autores.autor_id
            WHERE libros.isbn NOT IN (
                SELECT isbn_libro FROM prestamos WHERE fecha_devolucion IS NULL
            )
        ''')
        return self.cursor.fetchall()

    # --- metodos para prestamos ---

    def reg_prestamo(self, isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion):
        if not all([isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion]):
            return "Error: Todos los campo son obligatorios."
        # forma de fetcha
        try:
            fecha_pre = datetime.strptime(fecha_prestado, '%Y-%m-%d')
            fecha_dev = datetime.strptime(fecha_devolucion, '%Y-%m-%d')
        except ValueError:
            return "Error: Formato de fecha incorrecto (debe ser YYYY-MM-DD)."
        
        # fecha de devolucion debe que menos de fecta prestar
        if fecha_dev <= fecha_pre:
            return "Error: La fecha de devolución estimada debe ser posterior a la fecha de préstamo."

        self.cursor.execute("SELECT COUNT(*) FROM prestamos WHERE isbn_libro = ? AND fecha_devolucion IS NULL", (isbn_libro,))
        if self.cursor.fetchone()[0] > 0:
            return "Error: El libro ya se encuentra prestado."

        try:
            self.cursor.execute("INSERT INTO prestamos (isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion) VALUES (?, ?, ?, ?)",
                                (isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion))
            self.conexion.commit()
            return "prestamo registrado con exito."
        except sqlite3.Error as e:
            return f"Error de base de datos: {e}"
    # metodo para devolucion libro
    def reg_devolucion(self, isbn_libro, fecha_devolucion):
        try:
            self.cursor.execute("SELECT prestado_id FROM prestamos WHERE isbn_libro = ? AND fecha_devolucion IS NULL", (isbn_libro,))
            prestamo_activo = self.cursor.fetchone()

            if prestamo_activo:
                prestado_id = prestamo_activo[0]
                self.cursor.execute("UPDATE prestamos SET fecha_devolucion = ? WHERE prestado_id = ?",
                                    (fecha_devolucion, prestado_id))
                self.conexion.commit()
                return "Devolución registrada con éxito."
            else:
                return "Error: No se encontró un prestamo activo para este ISBN."
        except sqlite3.Error as e:
            return f"Error con baso de datos: {e}"
    def cerramos(self):
        self.conexion.close()

# las classes de biblioteca 


class Autor:
    """Clase para representar a un Autor."""
    def __init__(self, autor_id, nombre):
        self.autor_id = autor_id
        self.nombre = nombre

class Libro:
    """Clase para representar un Libro."""
    def __init__(self, isbn, titulo, autor_id, genre, anio_publicacion):
        self.isbn = isbn
        self.titulo = titulo
        self.autor_id = autor_id
        self.genre = genre
        self.anio_publicacion = anio_publicacion

class Prestamo:
    """Clase para representar un Préstamo."""
    def __init__(self, id_prestado, isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion = None):
        self.id_prestado = id_prestado
        self.isbn_libro = isbn_libro
        self.nombre_usuario = nombre_usuario
        self.fecha_prestado = fecha_prestado
        self.fecha_devolucion = fecha_devolucion
    