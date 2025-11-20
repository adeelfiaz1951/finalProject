import sqlite3
DB = 'biblio.db'
# crea la ruta de  la base de datos
def crear_tablas(db_path = None):
    ruta_db = db_path or DB
    with sqlite3.connect(ruta_db) as conexion:

        cursor = conexion.cursor()


        # crea la tabla de autor
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS autors(
            autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT)
        """)


        # crea la tabla de libros

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros(
            isbn INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            anio INTEGER,
            genre TEXT
            )           
        """)
            #FOREIGN KEY (autor_id) REFERENCES autors(autor_id)
        # crea la tabla de Prestamos

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestado(
            pretado_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetcha_prestar DATE,
            fetcha_volver DATE
            )
        """)
            #FOREIGN KEY (isbn) REFERENCES libros(isbn),

# Los funciones de CRUD de libros
def anadir_libro(titulo, anio, genre, db_path = None):
    ruta_db = db_path or DB
    crear_tablas(ruta_db)
    try:
        with sqlite3.connect(ruta_db) as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO libros (titulo, anio, genre) VALUES (?, ?, ?)", (titulo, anio, genre,))
            conexion.commit()
            return True
    except sqlite3.IntegrityError:
        return False

# guardamos los cambios 
    conexion.commit()
print("El producto añadido corectamente. ")
anadir_libro('book', 2001, 'novel')







# class Validavion:
#     def __init__(self, db_path = 'biblio.db'):
#         self.db_path = db_path
#         self.creat_table() 
        
#     # Crea un nuevo usario si no existe
#     def crear_tabla(self):
#         conexion = sqlite3.connect(self.db_path)
#         cursor = conexion.cursor()
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS usuarios(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             usuario TEXT UNIQUE,
#             email as TEXT,
#             password BLOB
#         )                    
        
#         """)
#         conexion.commit()
#         conexion.close()
#     # Registrar  usario  
#     def registrar(self, usuario, email, password):
#         conexion = sqlite3.connect(self.db_path)
#         cursor = conexion.cursor()
    
#         hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#         try:
#             conexion = sqlite3.connect(self.db_path)
#             cursor = conexion.cursor()
#             cursor.execute("INSERT INTO usuarios (usuario, email, password) VALUES (?, ?)", (usuario, email, hashed))
#             conexion.commit()
#             print(f'usuario {usuario} registrado')
#         except sqlite3.IntegrityError:
#             print(f'El usuario {usuario} ya esta registrado.')
            
#     # validar inicio de sesión
#     def verificar(self,usuario,email, password):
    
#         conexion = sqlite3.connect(self.db_path)
#         cursor = conexion.cursor()
#         cursor.execute("SELECT password FROM usuarios WHERE usuario=?, email=?", (usuario,email,))
#         fila = cursor.fetchone()
#         if fila:
#             return bcrypt.checkpw(password.encode(), fila[0])
#         else:
#             return False
        
