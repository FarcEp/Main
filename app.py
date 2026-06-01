from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        problema = conn.execute('SELECT * FROM problemas WHERE id = 1').fetchone()
        tests = conn.execute('SELECT * FROM casos_prueba WHERE problema_id = 1').fetchall()
        conn.close()
        return render_template('index.html', problem=problema, tests=tests)
    except Exception as e:
        return f"Error de conexión: {e}"

@app.route('/ejecutar', methods=['POST'])
def ejecutar_codigo():
    datos = request.json
    lenguaje = datos.get('lenguaje', 'python')
    codigo = datos.get('codigo', '')
    
    # Simulación lógica
    return jsonify({
        "veredicto": "Correcto",
        "lenguaje": lenguaje,
        "resultados": [{"test_id": 1, "estado": "Aprobado", "input": "...", "salida": "..."}]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
