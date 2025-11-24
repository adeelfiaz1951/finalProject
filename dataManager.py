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

        conexion.commit()
        conexion.close()
   