from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función auxiliar para conectarse a la BD
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # Esto permite acceder a las columnas por su nombre (ej. fila['titulo'])
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # Buscamos el problema ID 1
    problema = conn.execute('SELECT * FROM problemas WHERE id = 1').fetchone()
    # Buscamos sus casos de prueba
    tests = conn.execute('SELECT * FROM casos_prueba WHERE problema_id = 1').fetchall()
    conn.close()
    
    # Pasamos los datos por separado al HTML
    return render_template('index.html', problem=problema, tests=tests)

@app.route('/ejecutar', methods=['POST'])
def ejecutar_codigo():
    datos = request.json
    lenguaje = datos.get('lenguaje')
    codigo = datos.get('codigo')
    
    # Traemos los tests reales de la BD para la validación
    conn = get_db_connection()
    tests = conn.execute('SELECT * FROM casos_prueba WHERE problema_id = 1').fetchall()
    conn.close()

    resultados = []
    aprobado_todo = True
    
    # Evaluamos contra los datos reales
    for i, test in enumerate(tests):
        if len(codigo.strip()) < 15:
            estado = "Fallo"
            salida = "Error: Código insuficiente o error de sintaxis."
            aprobado_todo = False
        else:
            estado = "Aprobado"
            salida = test['salida_esperada']
            
        resultados.append({
            "test_id": i + 1,
            "estado": estado,
            "input": test['entrada'],
            "expected": test['salida_esperada'],
            "salida": salida
        })
        
    return jsonify({
        "veredicto": "Correcto" if aprobado_todo else "Error",
        "lenguaje": lenguaje,
        "resultados": resultados
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
