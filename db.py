import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS problemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        dificultad TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS casos_prueba (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problema_id INTEGER,
        entrada TEXT NOT NULL,
        salida_esperada TEXT NOT NULL,
        FOREIGN KEY (problema_id) REFERENCES problemas (id)
    )
''')

cursor.execute('''
    INSERT INTO problemas (titulo, dificultad, categoria, descripcion)
    VALUES (
        '71. Simplify Path',
        'Medium',
        'Stack',
        'Dada una ruta absoluta para un sistema de archivos, conviértela a la ruta canónica simplificada. Ignora los puntos simples . y maneja los dobles .. subiendo un nivel de directorio.'
    )
''')

problema_id = cursor.lastrowid

casos = [
    ('"/home/"',    '"/home"'),
    ('"/../"',      '"/"'),
    ('"/home//foo/"', '"/home/foo"')
]

cursor.executemany('''
    INSERT INTO casos_prueba (problema_id, entrada, salida_esperada)
    VALUES (?, ?, ?)
''', [(problema_id, c[0], c[1]) for c in casos])

conexion.commit()
conexion.close()
print("Base de datos inicializada correctamente.")
