import tkinter as tk
from tkinter import ttk, messagebox

from modulos.libro import Libro
from modulos.autor import Autor
from modulos.prestamo import Prestamo


class App:
    def __init__(self, root, usuario_id, usuario):
        self.root = root
        self.usuario_id = usuario_id
        self.usuario = usuario

        root.title(f"Biblioteca - {usuario}")
        root.geometry("1000x600")

        self.left_frame = tk.Frame(root, width=260, bg="#f0f0f0")
        self.left_frame.pack(side='left', fill='y')

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side='right', fill='both', expand=True)

        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menubar.add_command(label='Libro', command=self.menu_libro)
        menubar.add_command(label='Autor', command=self.menu_autor)
        menubar.add_command(label='Usuario', command=self.menu_usuario)
        menubar.add_command(label='Préstamos', command=self.menu_prestamos)

        # Treeview
        self.tree = ttk.Treeview(self.right_frame, columns=(1,2,3,4,5), show='headings')
        self.tree.pack(fill='both', expand=True)

        # Fix: selection binding
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.selected_row = None

        self.current_section = None
        self.menu_libro()


    # ---------------- UTILS --------------------

    def on_tree_select(self, event):
        """ Store the selected row globally """
        sel = self.tree.selection()
        if sel:
            self.selected_row = self.tree.item(sel[0])['values']
        else:
            self.selected_row = None

    def clear_left(self):
        for w in self.left_frame.winfo_children():
            w.destroy()

    def clear_tree(self):
        for col in self.tree['columns']:
            self.tree.heading(col, text='')
        self.tree.delete(*self.tree.get_children())
        self.selected_row = None


    # ---------------- MENÚ: LIBROS --------------------

    def menu_libro(self):
        self.current_section = 'libro'
        self.clear_left()
        self.clear_tree()

        tk.Label(self.left_frame, text='Gestión Libros', bg='#f0f0f0', font=('Arial',12,'bold')).pack(pady=8)
        tk.Button(self.left_frame, text='Añadir Libro', width=25, command=self.form_add_libro).pack(pady=4)
        tk.Button(self.left_frame, text='Eliminar Libro', width=25, command=self.action_eliminar_libro).pack(pady=4)
        tk.Button(self.left_frame, text='Modificar Libro', width=25, command=self.form_modificar_libro).pack(pady=4)
        tk.Button(self.left_frame, text='Libros Disponibles', width=25, command=self.show_libros_disponibles).pack(pady=4)

        self.show_libros()


    # ---------------- MENÚ: AUTORES --------------------

    def menu_autor(self):
        self.current_section = 'autor'
        self.clear_left()
        self.clear_tree()

        tk.Label(self.left_frame, text='Gestión Autores', bg='#f0f0f0', font=('Arial',12,'bold')).pack(pady=8)
        tk.Button(self.left_frame, text='Añadir Autor', width=25, command=self.form_add_autor).pack(pady=4)
        tk.Button(self.left_frame, text='Eliminar Autor', width=25, command=self.action_eliminar_autor).pack(pady=4)

        self.show_autores()


    # ---------------- MENÚ: USUARIOS --------------------

    def menu_usuario(self):
        self.current_section = 'usuario'
        self.clear_left()
        self.clear_tree()

        tk.Label(self.left_frame, text='Usuario', bg='#f0f0f0', font=('Arial',12,'bold')).pack(pady=8)
        tk.Button(self.left_frame, text='Cerrar sesión', width=25, command=self.cerrar_sesion).pack(pady=4)

        self.show_usuarios()


    # ---------------- MENÚ: PRÉSTAMOS --------------------

    def menu_prestamos(self):
        self.current_section = 'prestamos'
        self.clear_left()
        self.clear_tree()

        tk.Label(self.left_frame, text='Préstamos', bg='#f0f0f0', font=('Arial',12,'bold')).pack(pady=8)
        tk.Button(self.left_frame, text='Prestar Libro', width=25, command=self.form_prestar).pack(pady=4)
        tk.Button(self.left_frame, text='Devolver Libro', width=25, command=self.action_devolver).pack(pady=4)

        self.show_prestamos_usuario()


    # ---------------- FORMS --------------------

    def form_add_libro(self):
        top = tk.Toplevel(self.root)
        top.title('Añadir Libro')

        tk.Label(top, text='ISBN:').grid(row=0, column=0, padx=8, pady=4)
        isbn = tk.Entry(top); isbn.grid(row=0, column=1)

        tk.Label(top, text='Título:').grid(row=1, column=0, padx=8, pady=4)
        titulo = tk.Entry(top); titulo.grid(row=1, column=1)

        tk.Label(top, text='Autor ID:').grid(row=2, column=0, padx=8, pady=4)
        autor_id = tk.Entry(top); autor_id.grid(row=2, column=1)

        tk.Label(top, text='Género:').grid(row=3, column=0, padx=8, pady=4)
        genre = tk.Entry(top); genre.grid(row=3, column=1)

        tk.Label(top, text='anio_publicacion:').grid(row=4, column=0, padx=8, pady=4)
        anio_publicacion = tk.Entry(top); anio_publicacion.grid(row=4, column=1)

        def submit():
            try:
                L = Libro(
                    isbn.get().strip(),
                    titulo.get().strip(),
                    int(autor_id.get().strip()),
                    genre.get().strip(),
                    int(anio_publicacion.get().strip())
                )
                res = L.guardar()
                if res is True:
                    messagebox.showinfo('OK', 'Libro añadido')
                    top.destroy()
                    self.show_libros()
                else:
                    messagebox.showerror('Error', res)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text='Guardar', command=submit).grid(row=5, column=0, columnspan=2, pady=10)


    def form_modificar_libro(self):
        if not self.selected_row:
            messagebox.showerror('Error','Seleccione un libro en la tabla')
            return

        item = self.selected_row
        libro_id = item[0]

        top = tk.Toplevel(self.root)
        top.title("Modificar Libro")

        tk.Label(top, text='Título:').grid(row=0,column=0,padx=8,pady=4)
        titulo = tk.Entry(top); titulo.insert(0,item[2]); titulo.grid(row=0,column=1)

        tk.Label(top, text='Autor ID:').grid(row=1,column=0,padx=8,pady=4)
        autor_id = tk.Entry(top); autor_id.grid(row=1,column=1)

        tk.Label(top, text='Género:').grid(row=2,column=0,padx=8,pady=4)
        genre = tk.Entry(top); genre.insert(0,item[4]); genre.grid(row=2,column=1)

        tk.Label(top, text='Año:').grid(row=3,column=0,padx=8,pady=4)
        anio = tk.Entry(top); anio.insert(0,item[5]); anio.grid(row=3,column=1)

        def submit():
            try:
                L = Libro(item[1], titulo.get().strip(),
                          int(autor_id.get().strip()) if autor_id.get().strip() else None,
                          genre.get().strip(),
                          int(anio.get().strip()))

                L.id = libro_id
                res = L.modificar()
                if res is True:
                    messagebox.showinfo('OK','Modificado')
                    top.destroy()
                    self.show_libros()
                else:
                    messagebox.showerror('Error', res)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text='Guardar', command=submit).grid(row=4,column=0,columnspan=2,pady=10)


    def action_eliminar_libro(self):
        if not self.selected_row:
            messagebox.showerror('Error','Seleccione un libro')
            return

        libro_id = self.selected_row[0]
        L = Libro(id=libro_id)
        res = L.eliminar()
        if res is True:
            messagebox.showinfo('OK','Eliminado')
            self.show_libros()
        else:
            messagebox.showerror('Error', res)


    def form_add_autor(self):
        top = tk.Toplevel(self.root)
        top.title('Añadir Autor')

        tk.Label(top, text='Nombre:').grid(row=0,column=0,padx=8,pady=4)
        nombre = tk.Entry(top); nombre.grid(row=0,column=1)

        def submit():
            A = Autor(nombre=nombre.get().strip())
            res = A.guardar()
            if res is True:
                messagebox.showinfo('OK','Autor añadido')
                top.destroy()
                self.show_autores()
            else:
                messagebox.showerror('Error', res)

        tk.Button(top, text='Guardar', command=submit).grid(row=1,column=0,columnspan=2,pady=8)


    def action_eliminar_autor(self):
        if not self.selected_row:
            messagebox.showerror('Error','Seleccione un autor')
            return

        autor_id = self.selected_row[0]
        A = Autor(id=autor_id)
        res = A.eliminar()

        if res is True:
            messagebox.showinfo('OK','Autor eliminado')
            self.show_autores()
        else:
            messagebox.showerror('Error', res)


    # ------------ PRÉSTAMOS -------------

    def form_prestar(self):
        if not self.selected_row:
            messagebox.showerror('Error','Seleccione un libro para prestar')
            return

        libro_id = self.selected_row[0]

        top = tk.Toplevel(self.root)
        top.title('Prestar libro')

        tk.Label(top, text='Fecha (YYYY-MM-DD):').pack(pady=6)
        fecha = tk.Entry(top); fecha.pack()

        def submit():
            P = Prestamo(
                libro_id=libro_id,
                usuario_id=self.usuario_id,
                fecha_prestamo=fecha.get().strip()
            )
            res = P.registrar()
            if res is True:
                messagebox.showinfo('OK','Préstamo registrado')
                top.destroy()
                self.show_prestamos_usuario()
                self.show_libros()
            else:
                messagebox.showerror('Error', res)

        tk.Button(top, text='Prestar', command=submit).pack(pady=8)


    def action_devolver(self):
        if not self.selected_row:
            messagebox.showerror('Error','Seleccione un préstamo')
            return

        prestamo_id = self.selected_row[0]

        try:
            from dataManager import get_conexion
            import datetime

            conn = get_conexion()
            cur = conn.cursor()
            fecha = datetime.date.today().isoformat()

            cur.execute(
                'UPDATE prestamos SET fecha_devolucion=? WHERE id=?',
                (fecha, prestamo_id)
            )

            conn.commit()
            messagebox.showinfo("OK", "Devolución registrada")

            self.show_prestamos_usuario()
            self.show_libros()

        except Exception as e:
            messagebox.showerror("Error", str(e))


    # ---------------- TABLE LOADING --------------------

    def show_libros(self):
        self.clear_tree()

        cols = ['id','isbn','titulo','autor','genre','anio']
        self.tree['columns'] = cols

        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=140)

        for row in Libro.obtener_todos():
            self.tree.insert('', 'end', values=row)


    def show_libros_disponibles(self):
        self.clear_tree()

        cols = ['id','isbn','titulo','autor','genre','anio']
        self.tree['columns'] = cols

        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=140)

        for row in Libro.obtener_disponibles():
            self.tree.insert('', 'end', values=row)


    def show_autores(self):
        self.clear_tree()

        cols = ['id','nombre']
        self.tree['columns'] = cols

        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=200)

        for row in Autor.obtener_todos():
            self.tree.insert('', 'end', values=row)


    def show_usuarios(self):
        self.clear_tree()

        cols = ['id','nombre','username']
        self.tree['columns'] = cols

        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=180)

        from dataManager import get_conexion
        conn = get_conexion()
        cur = conn.cursor()

        cur.execute('SELECT id,nombre,username FROM usuarios ORDER BY nombre')

        for row in cur.fetchall():
            self.tree.insert('', 'end', values=row)


    def show_prestamos_usuario(self):
        self.clear_tree()

        cols = ['id','isbn','titulo','fecha_prestamo']
        self.tree['columns'] = cols

        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=180)

        for row in Prestamo.prestamos_activos_por_usuario(self.usuario_id):
            self.tree.insert('', 'end', values=row)


    # ------------ SESSION -------------

    def cerrar_sesion(self):
        self.root.destroy()
