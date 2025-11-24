import bcrypt
from dataManager import get_conexion
import sqlite3


class Usuario:
    def __init__(self, usuario=None, password=None, id=None):
        self.id = id
        self.usuario = usuario.strip() if usuario else None
        self.password = password  # Guardamos en plano, se encripta al registrar

        # Connection única por instancia
        self.conexion = get_conexion()
        self.cursor = self.conexion.cursor()

    # ------------------------------------------
    # REGISTRAR USUARIO
    # ------------------------------------------
    def registrar(self):

        if not all([self.usuario, self.email, self.password]):
            return "Error: usuario, email y contraseña son obligatorios."

        # Hash correcto, una sola vez
        hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())

        try:
            self.cursor.execute(
                "INSERT INTO usuarios (usuario, email, password) VALUES (?, ?, ?)",
                (self.usuario, self.email, hashed)
            )
            self.conexion.commit()
            self.id = self.cursor.lastrowid
            return f"Usuario {self.usuario} registrado correctamente."

        except sqlite3.IntegrityError:
            return f"Error: usuario '{self.usuario}' ya existe."

    # ------------------------------------------
    # LOGIN
    # ------------------------------------------
    def verificar(self, usuario, password):

        # Buscar usuario
        self.cursor.execute(
            "SELECT password FROM usuarios WHERE usuario=?",
            (usuario,)
        )
        fila = self.cursor.fetchone()

        if fila is None:
            return False  # usuario no encontrado

        hash_guardado = fila[0]

        # Comparar con bcrypt
        return bcrypt.checkpw(password.encode(), hash_guardado)

    # ------------------------------------------
    # Cerrar conexión cuando se desee
    # ------------------------------------------
    def close(self):
        self.conexion.close()
