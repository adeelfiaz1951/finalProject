import sqlite3

     # Conexión a la base de datos
def get_conexion():
    conexion = sqlite3.connect("biblio.db")
    return conexion


def crea_tablas():
        conexion = get_conexion()
        cursor = conexion.cursor()
        # Tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password BLOB NOT NULL
            )
        """)

        # Tabla autores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autores (
                autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)

        # Tabla libros
        cursor.execute("""
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                prestado_id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn_libro TEXT NOT NULL,
                nombre_usuario TEXT NOT NULL,
                fecha_prestado DATE NOT NULL,
                fecha_devolucion DATE,
                FOREIGN KEY (isbn_libro) REFERENCES libros(isbn)
                FOREIGN KEY (nombre_usuario) REFERENCES usuarios(nombre)
                            
                            
            )
        """)

<<<<<<< HEAD
        conexion.commit()
        conexion.close()
   
=======
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




# # ----------------------------------------------
# # CLASES MODELO
# # ----------------------------------------------
# class Autor:
#     def __init__(self, autor_id, nombre):
#         self.autor_id = autor_id
#         self.nombre = nombre


# class Libro:
#     def __init__(self, isbn, titulo, autor_id, genre, anio_publicacion):
#         self.isbn = isbn
#         self.titulo = titulo
#         self.autor_id = autor_id
#         self.genre = genre
#         self.anio_publicacion = anio_publicacion


#     def anadir_libro(self, isbn, titulo, autor_id, genre, anio_publicacion):

#         nuevo = DataManager.anadir_libro(isbn, titulo, autor_id, genre, anio_publicacion)





# class Prestamo:
#     def __init__(self, id_prestado, isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion=None):
#         self.id_prestado = id_prestado
#         self.isbn_libro = isbn_libro
#         self.nombre_usuario = nombre_usuario
#         self.fecha_prestado = fecha_prestado
#         self.fecha_devolucion = fecha_devolucion
>>>>>>> 848af4fb687f16f569bf97e1b7f09164c57f8572
