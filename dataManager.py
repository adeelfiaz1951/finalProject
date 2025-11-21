import sqlite3
import bcrypt
from datetime import datetime


class DataManager:
    def __init__(self, root=None):
        self.root = root
        if self.root:
            self.root.title("Gestión de Biblioteca")

        # Conexión a la base de datos
        self.conexion = sqlite3.connect("biblio.db")
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    # ------------------------------------------
    # CREAR TABLAS
    # ------------------------------------------
    def crear_tablas(self):
        try:
            # Tabla usuarios
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE,
                    email TEXT,
                    password BLOB
                )
            """)

            # Tabla autores
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS autores (
                    autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL
                )
            """)

            # Tabla libros
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor_id INTEGER NOT NULL,
                    genre TEXT,
                    anio_publicacion INTEGER,
                    FOREIGN KEY (autor_id) REFERENCES autores(autor_id)
                )
            """)

            # Tabla préstamos
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prestamos (
                    prestado_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn_libro TEXT NOT NULL,
                    nombre_usuario TEXT NOT NULL,
                    fecha_prestado DATE NOT NULL,
                    fecha_devolucion DATE,
                    FOREIGN KEY (isbn_libro) REFERENCES libros(isbn)
                )
            """)

            self.conexion.commit()

        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")

    # ------------------------------------------
    # REGISTRAR USUARIO
    # ------------------------------------------
    def registrar(self, usuario, email, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            self.cursor.execute(
                "INSERT INTO usuarios (usuario, email, password) VALUES (?, ?, ?)",
                (usuario, email, hashed)
            )
            self.conexion.commit()
            return f"Usuario {usuario} registrado correctamente."
        except sqlite3.IntegrityError:
            return f"Error: usuario '{usuario}' ya existe."

    # ------------------------------------------
    # LOGIN
    # ------------------------------------------
    def verificar(self, usuario, password):
        self.cursor.execute("SELECT password FROM usuarios WHERE usuario=?", (usuario,))
        fila = self.cursor.fetchone()

        if fila:
            return bcrypt.checkpw(password.encode(), fila[0])
        return False

    # ------------------------------------------
    # VALIDAR ISBN
    # ------------------------------------------
    def validar_isbn(self, isbn):
        return (len(isbn) == 10 or len(isbn) == 13) and isbn.isdigit()

    # ------------------------------------------
    # CRUD AUTORES
    # ------------------------------------------
    def load_autor(self):
        self.cursor.execute("SELECT autor_id, nombre FROM autores")
        return self.cursor.fetchall()

    def anadir_autor(self, nombre):
        if not nombre:
            return "Error: nombre de autor requerido."

        try:
            self.cursor.execute("INSERT INTO autores (nombre) VALUES (?)", (nombre,))
            self.conexion.commit()
            return "Autor añadido correctamente."
        except sqlite3.IntegrityError:
            return "Error: el autor ya existe."

    def eliminar_autor(self, autor_id):
        try:
            self.cursor.execute("DELETE FROM autores WHERE autor_id=?", (autor_id,))
            self.conexion.commit()
            return "Autor eliminado correctamente."
        except sqlite3.Error as e:
            return f"Error eliminando autor: {e}"

    # ------------------------------------------
    # CRUD LIBROS
    # ------------------------------------------
    def anadir_libro(self, isbn, titulo, autor_id, genre, anio_publicacion):
        if not all([isbn, titulo, autor_id]):
            return "Error: ISBN, título y autor son obligatorios."

        if not self.validar_isbn(isbn):
            return "Error: ISBN no válido."

        try:
            self.cursor.execute("""
                INSERT INTO libros (isbn, titulo, autor_id, genre, anio_publicacion)
                VALUES (?, ?, ?, ?, ?)
            """, (isbn, titulo, autor_id, genre, anio_publicacion))

            self.conexion.commit()
            return "Libro añadido correctamente."

        except sqlite3.IntegrityError:
            return "Error: un libro con este ISBN ya existe."

    def eliminar_libro(self, isbn):
        try:
            self.cursor.execute("DELETE FROM libros WHERE isbn=?", (isbn,))
            self.conexion.commit()
            return "Libro eliminado correctamente."
        except sqlite3.Error as e:
            return f"Error eliminando libro: {e}"

    def modificar_libro(self, isbn, titulo, genre, anio_publicacion):
        try:
            self.cursor.execute("""
                UPDATE libros SET titulo=?, genre=?, anio_publicacion=? WHERE isbn=?
            """, (titulo, genre, anio_publicacion, isbn))

            self.conexion.commit()
            return "Libro modificado correctamente."
        except sqlite3.Error as e:
            return f"Error modificando libro: {e}"

    def load_libros(self):
        self.cursor.execute("""
            SELECT libros.isbn, libros.titulo, autores.nombre, libros.genre, libros.anio_publicacion
            FROM libros
            JOIN autores ON libros.autor_id = autores.autor_id
        """)
        return self.cursor.fetchall()

    def load_libros_disponibles(self):
        self.cursor.execute("""
            SELECT libros.isbn, libros.titulo, autores.nombre, libros.genre, libros.anio_publicacion
            FROM libros
            JOIN autores ON libros.autor_id = autores.autor_id
            WHERE libros.isbn NOT IN (
                SELECT isbn_libro FROM prestamos WHERE fecha_devolucion IS NULL
            )
        """)
        return self.cursor.fetchall()

    # ------------------------------------------
    # PRÉSTAMOS
    # ------------------------------------------
    def reg_prestamo(self, isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion):
        if not all([isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion]):
            return "Error: todos los campos son obligatorios."

        try:
            fecha_pre = datetime.strptime(fecha_prestado, "%Y-%m-%d")
            fecha_dev = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
        except ValueError:
            return "Error: las fechas deben estar en formato YYYY-MM-DD."

        if fecha_dev <= fecha_pre:
            return "Error: la devolución debe ser posterior al préstamo."

        self.cursor.execute(
            "SELECT COUNT(*) FROM prestamos WHERE isbn_libro=? AND fecha_devolucion IS NULL",
            (isbn_libro,)
        )
        if self.cursor.fetchone()[0] > 0:
            return "Error: el libro ya está prestado."

        try:
            self.cursor.execute("""
                INSERT INTO prestamos (isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion)
                VALUES (?, ?, ?, ?)
            """, (isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion))

            self.conexion.commit()
            return "Préstamo registrado correctamente."
        except sqlite3.Error as e:
            return f"Error registrando préstamo: {e}"

    def reg_devolucion(self, isbn_libro, fecha_devolucion):
        try:
            self.cursor.execute("""
                SELECT prestado_id FROM prestamos
                WHERE isbn_libro=? AND fecha_devolucion IS NULL
            """, (isbn_libro,))
            prestamo = self.cursor.fetchone()

            if not prestamo:
                return "Error: no hay préstamo activo para este libro."

            prestamo_id = prestamo[0]

            self.cursor.execute("""
                UPDATE prestamos SET fecha_devolucion=? WHERE prestado_id=?
            """, (fecha_devolucion, prestamo_id))

            self.conexion.commit()
            return "Devolución registrada correctamente."

        except sqlite3.Error as e:
            return f"Error registrando devolución: {e}"

    # ------------------------------------------
    def cerramos(self):
        self.conexion.close()


# ----------------------------------------------
# CLASES MODELO
# ----------------------------------------------
class Autor:
    def __init__(self, autor_id, nombre):
        self.autor_id = autor_id
        self.nombre = nombre


class Libro:
    def __init__(self, isbn, titulo, autor_id, genre, anio_publicacion):
        self.isbn = isbn
        self.titulo = titulo
        self.autor_id = autor_id
        self.genre = genre
        self.anio_publicacion = anio_publicacion


class Prestamo:
    def __init__(self, id_prestado, isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion=None):
        self.id_prestado = id_prestado
        self.isbn_libro = isbn_libro
        self.nombre_usuario = nombre_usuario
        self.fecha_prestado = fecha_prestado
        self.fecha_devolucion = fecha_devolucion
