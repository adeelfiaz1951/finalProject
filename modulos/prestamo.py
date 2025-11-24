from dataManager import get_conexion
import sqlite3
from datetime import datetime

class Prestamo:
    def __init__(self, id_prestamo=None, isbn_libro=None, nombre_usuario=None,
                 fecha_prestado=None, fecha_devolucion=None):

        self.id_prestamo = id_prestamo
        self.isbn_libro = isbn_libro
        self.nombre_usuario = nombre_usuario
        self.fecha_prestado = fecha_prestado
        self.fecha_devolucion = fecha_devolucion

        # Una sola conexión por instancia
        self.conexion = get_conexion()
        self.cursor = self.conexion.cursor()

    # ------------------------------------------
    # REGISTRAR PRÉSTAMO
    # ------------------------------------------
    def reg_prestamo(self):
        # Fecha de devolución NO es obligatoria al crear préstamo
        if not all([self.isbn_libro, self.nombre_usuario, self.fecha_prestado]):
            return "Error: ISBN, usuario y fecha de préstamo son obligatorios."

        # Validar fecha préstamo
        try:
            datetime.strptime(self.fecha_prestado, "%Y-%m-%d")
        except ValueError:
            return "Error: la fecha de préstamo debe ser YYYY-MM-DD."

        # Verificar si el libro está prestado actualmente
        self.cursor.execute("""
            SELECT COUNT(*) FROM prestamos 
            WHERE isbn_libro=? AND fecha_devolucion IS NULL
        """, (self.isbn_libro,))

        if self.cursor.fetchone()[0] > 0:
            return "Error: el libro ya está prestado."

        try:
            self.cursor.execute("""
                INSERT INTO prestamos (isbn_libro, nombre_usuario, fecha_prestado, fecha_devolucion)
                VALUES (?, ?, ?, NULL)
            """, (self.isbn_libro, self.nombre_usuario, self.fecha_prestado))

            self.conexion.commit()
            return True

        except sqlite3.Error as e:
            return f"Error registrando préstamo: {e}"

    # ------------------------------------------
    # REGISTRAR DEVOLUCIÓN
    # ------------------------------------------
    def reg_devolucion(self, isbn_libro, fecha_devolucion):

        # Validar fecha
        try:
            datetime.strptime(fecha_devolucion, "%Y-%m-%d")
        except ValueError:
            return "Error: la fecha de devolución debe ser YYYY-MM-DD."

        try:
            # Buscar préstamo ACTIVO
            self.cursor.execute("""
                SELECT prestamo_id 
                FROM prestamos
                WHERE isbn_libro=? AND fecha_devolucion IS NULL
            """, (isbn_libro,))

            prestamo = self.cursor.fetchone()

            if not prestamo:
                return "Error: no hay un préstamo activo para este libro."

            prestamo_id = prestamo[0]

            # Actualizar préstamo
            self.cursor.execute("""
                UPDATE prestamos 
                SET fecha_devolucion=?
                WHERE prestamo_id=?
            """, (fecha_devolucion, prestamo_id))

            self.conexion.commit()
            return True

        except sqlite3.Error as e:
            return f"Error registrando devolución: {e}"

    # ------------------------------------------
    # CERRAR CONEXIÓN CUANDO SE DESEE
    # ------------------------------------------
    def close(self):
        self.conexion.close()
