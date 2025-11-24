from dataManager import get_conexion
import sqlite3


class Libro:
    def __init__(self, isbn, titulo, autor_id, genre, anio_publicacion):
        self.isbn = isbn.replace("-", "").strip()
        self.titulo = titulo.strip()
        self.autor_id = autor_id
        self.genre = genre
        self.anio_publicacion = anio_publicacion
        
        # Una sola conexión por instancia
        self.conexion = get_conexion()
        self.cursor = self.conexion.cursor()

    # ------------------------------------------
    # VALIDACIÓN ISBN
    # ------------------------------------------
    def validar_isbn(self, isbn):
        if len(isbn) == 10:
            return isbn.isdigit()
        if len(isbn) == 13:
            return isbn.isdigit()
        return False

    # ------------------------------------------
    # CRUD LIBROS
    # ------------------------------------------

    def anadir_libro(self):
        # VALIDAR ISBN
        if len(self.isbn) not in (10, 13) or not self.isbn.isdigit():
            return "Error: ISBN inválido."

        if not all([self.isbn, self.titulo, self.autor_id]):
            return "Error: ISBN, título y autor son obligatorios."

        if not self.validar_isbn(self.isbn):
            return "Error: ISBN no válido."

        try:
            self.cursor.execute("""
                INSERT INTO libros (isbn, titulo, autor_id, genre, anio_publicacion)
                VALUES (?, ?, ?, ?, ?)
            """, (self.isbn, self.titulo, self.autor_id, self.genre, self.anio_publicacion))

            self.conexion.commit()
            return True

        except sqlite3.IntegrityError:
            return "Error: un libro con este ISBN ya existe."

    def eliminar_libro(self):
        try:
            self.cursor.execute("DELETE FROM libros WHERE isbn=?", (self.isbn,))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            return f"Error eliminando libro: {e}"

    def modificar_libro(self):
        try:
            self.cursor.execute("""
                UPDATE libros 
                SET titulo=?, genre=?, anio_publicacion=? 
                WHERE isbn=?
            """, (self.titulo, self.genre, self.anio_publicacion, self.isbn))

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

    def close(self):
        """Cerrar la conexión manualmente cuando ya no se necesite la instancia"""
        self.conexion.close()
