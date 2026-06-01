import sqlite3

# 1. Conectar a la base de datos (se creará automáticamente el archivo)
conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

# 2. Crear tabla de Problemas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS problemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        dificultad TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL
    )
''')

# 3. Crear tabla de Casos de Prueba (relacionada al problema)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS casos_prueba (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problema_id INTEGER,
        entrada TEXT NOT NULL,
        salida_esperada TEXT NOT NULL,
        FOREIGN KEY (problema_id) REFERENCES problemas (id)
    )
''')

# 4. Insertar nuestro primer problema real
cursor.execute('''
    INSERT INTO problemas (titulo, dificultad, categoria, descripcion)
    VALUES ('71. Simplify Path', 'Medium', 'Stack', 'Dada una ruta absoluta para un sistema de archivos, conviértela a la ruta canónica simplificada. Ignora los puntos simples ''.'' y maneja los dobles ''..'' subiendo un nivel de directorio.')
''')
problema_id = cursor.lastrowid # Obtenemos el ID que se le asignó

# 5. Insertar los casos de prueba para ese problema
casos = [
    ('"/home/"', '"/home"'),
    ('"/../"', '"/"'),
    ('"/home//foo/"', '"/home/foo"')
]

cursor.executemany('''
    INSERT INTO casos_prueba (problema_id, entrada, salida_esperada)
    VALUES (?, ?, ?)
''', [(problema_id, c[0], c[1]) for c in casos])

# Guardar cambios y cerrar
conexion.commit()
conexion.close()

print("¡Éxito! Base de datos 'database.db' inicializada correctamente.")
