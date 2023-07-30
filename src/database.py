import sqlite3

def configurar_base_de_datos():
    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    # Creación de la tabla Recetas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            ingredientes TEXT,
            pasos TEXT
        )
    ''')

    conn.commit()
    conn.close()

def agregar_receta(titulo, ingredientes, pasos):
    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Recetas (titulo, ingredientes, pasos) VALUES (?, ?, ?)',
                   (titulo, ingredientes, pasos))

    conn.commit()
    conn.close()
