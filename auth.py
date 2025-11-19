import sqlite3, bcrypt
class Validavion:
    def __init__(self, db_path = 'biblio.db'):
        self.db_path = db_path
        self.creat_table() 
        
    # Crea un nuevo usario si no existe
    def crear_tabla(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            email as TEXT,
            password BLOB
        )                    
        
        """)
        conexion.commit()
        conexion.close()
    # Registrar  usario  
    def registrar(self, usuario, email, password):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
    
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, email, password) VALUES (?, ?)", (usuario, email, hashed))
            conexion.commit()
            print(f'usuario {usuario} registrado')
        except sqlite3.IntegrityError:
            print(f'El usuario {usuario} ya esta registrado.')
            
    # validar inicio de sesión
    def verificar(self,usuario,email, password):
    
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE usuario=?, email=?", (usuario,email,))
        fila = cursor.fetchone()
        if fila:
            return bcrypt.checkpw(password.encode(), fila[0])
        else:
            return False
        
