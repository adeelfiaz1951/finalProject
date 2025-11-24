
from dataManager import DataManager


class Libro:
    def __init__(self):
        pass

    def nuevo_libro(self, isbn, titulo, autor_id, genre, anio_publicacion):

        try:
            nuevo = DataManager.anadir_libro(isbn, titulo, autor_id, genre, anio_publicacion)
            if (nuevo == "Libro añadido correctamente."):
                return True
            
        except ValueError:
            print(ValueError)
            return False


