import tkinter as tk
import database
import gui

def main():
    # Configurar la base de datos
    database.configurar_base_de_datos()

    # Crear y ejecutar la interfaz gráfica
    root = tk.Tk()
    app = gui.RecetasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
