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

        # TODO: Agregar los eventos para manejar la selección de una receta

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

if __name__ == "__main__":
    root = tk.Tk()
    app = RecetasApp(root)
    root.mainloop()
