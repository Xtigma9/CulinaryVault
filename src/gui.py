import sqlite3
import tkinter as tk
import database

class RecetasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recetas App")
        
        # Widgets y otros componentes de la interfaz aquí...
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry_search = tk.Entry(self.root, textvariable=self.search_var, width=30)
        self.entry_search.pack(pady=10)
        
        self.listbox_recetas = tk.Listbox(self.root, width=50)
        self.listbox_recetas.pack()

        # Botón para agregar una nueva receta
        self.btn_agregar_receta = tk.Button(self.root, text="Agregar Receta", command=self.abrir_ventana_agregar_receta)
        self.btn_agregar_receta.pack()

        # Botón para eliminar la receta seleccionada
        self.btn_eliminar_receta = tk.Button(self.root, text="Eliminar Receta", command=self.eliminar_receta)
        self.btn_eliminar_receta.pack()

    def update_list(self, *args):
        # ... (código para actualizar la lista de recetas)
        search_term = self.search_var.get()
        conn = sqlite3.connect("recetas.db")
        cursor = conn.cursor()

        cursor.execute('SELECT titulo FROM Recetas WHERE titulo LIKE ?', ('%' + search_term + '%',))
        recetas = cursor.fetchall()
        
        self.listbox_recetas.delete(0, tk.END)
        for receta in recetas:
            self.listbox_recetas.insert(tk.END, receta[0])

        conn.close()

    def mostrar_detalles_receta(self, event):
        # ... (código para mostrar los detalles de la receta seleccionada)
        seleccion = self.listbox_recetas.curselection()
        if seleccion:
            index = seleccion[0]
            titulo_receta = self.listbox_recetas.get(index)
            detalles = self.obtener_detalles_receta(titulo_receta)
            # TODO: Mostrar los detalles de la receta en una nueva ventana

    def obtener_detalles_receta(self, titulo):
        # ... (código para obtener los detalles de una receta de la base de datos)
        conn = sqlite3.connect("recetas.db")
        cursor = conn.cursor()

        cursor.execute('SELECT ingredientes, pasos FROM Recetas WHERE titulo = ?', (titulo,))
        detalles = cursor.fetchone()

        conn.close()
        return detalles

    def mostrar_ventana_detalles(self, titulo, detalles):
        # ... (código para mostrar los detalles de la receta en una nueva ventana)
        ventana_detalles = tk.Toplevel(self.root)
        ventana_detalles.title(titulo)

        label_ingredientes = tk.Label(ventana_detalles, text="Ingredientes:")
        label_ingredientes.pack()
        text_ingredientes = tk.Text(ventana_detalles, width=40, height=6)
        text_ingredientes.pack()
        text_ingredientes.insert(tk.END, detalles[0])

        label_pasos = tk.Label(ventana_detalles, text="Pasos:")
        label_pasos.pack()
        text_pasos = tk.Text(ventana_detalles, width=40, height=10)
        text_pasos.pack()
        text_pasos.insert(tk.END, detalles[1])

    def abrir_ventana_agregar_receta(self):
        # Crear una nueva ventana para añadir recetas
        ventana_agregar_receta = tk.Toplevel(self.root)
        ventana_agregar_receta.title("Añadir Receta")

        # Etiquetas y campos de texto para los detalles de la receta
        tk.Label(ventana_agregar_receta, text="Título:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_titulo = tk.Entry(ventana_agregar_receta, width=30)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana_agregar_receta, text="Ingredientes:").grid(row=1, column=0, padx=5, pady=5)
        self.text_ingredientes = tk.Text(ventana_agregar_receta, width=40, height=6)
        self.text_ingredientes.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana_agregar_receta, text="Pasos:").grid(row=2, column=0, padx=5, pady=5)
        self.text_pasos = tk.Text(ventana_agregar_receta, width=40, height=10)
        self.text_pasos.grid(row=2, column=1, padx=5, pady=5)

        # Botón para guardar la receta
        btn_guardar = tk.Button(ventana_agregar_receta, text="Guardar", command=self.guardar_receta)
        btn_guardar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def guardar_receta(self):
        titulo = self.entry_titulo.get()
        ingredientes = self.text_ingredientes.get("1.0", tk.END)
        pasos = self.text_pasos.get("1.0", tk.END)

        # Llamar a la función para agregar la receta a la base de datos
        database.agregar_receta(titulo, ingredientes, pasos)

        # Actualizar la lista de recetas en la interfaz gráfica
        self.update_list()

        # Cerrar la ventana de agregar receta
        self.abrir_ventana_agregar_receta.destroy()

    def eliminar_receta(self):
        # Obtener el índice de la receta seleccionada en la lista
        seleccion = self.listbox_recetas.curselection()
        if seleccion:
            index = seleccion[0]
            titulo_receta = self.listbox_recetas.get(index)
            # Llamar a la función para eliminar la receta de la base de datos
            database.eliminar_receta(titulo_receta)
            # Actualizar la lista de recetas en la interfaz gráfica
            self.update_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecetasApp(root)
    root.mainloop()
