from dataManager import get_conexion
import sqlite3

class Autor:
    def __init__(self, nombre,autor_id):
        self.nombre = nombre.strip()
        self.autor_id = autor_id
        self.conexion = get_conexion()
        self.cursor = self.conexion.cursor()
          # ------------------------------------------
    # CRUD AUTORES
    # ------------------------------------------
    def load_autor(self):
        
        self.cursor.execute("SELECT autor_id, nombre FROM autores")
        autor_datos = self.cursor.fetchall()

        return autor_datos
    

    def anadir_autor(self):
        if not self.nombre:
            return "Error: nombre de autor requerido."

        try:
            self.cursor.execute("INSERT INTO autores (nombre) VALUES (?)", (self.nombre,))
            self.conexion.commit()
            return True  # anadir correctamente
        except sqlite3.IntegrityError:
            return "Error: el autor ya existe."

    def eliminar_autor(self):
        if not self.autor_id:
            return "Error: autor_id requerido."

        try:
            self.cursor.execute(
                "DELETE FROM autores WHERE autor_id = ?",
                (self.autor_id,)
            )
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            return f"Error eliminando autor: {e}"

    def close(self):
        """Cerrar la conexión manualmente cuando ya no se use"""
        self.conexion.close()