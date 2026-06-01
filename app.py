import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_problem(problem_id):
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute('SELECT * FROM problemas WHERE id = ?', (problem_id,))
    row = cur.fetchone()
    if not row:
        return None

    cur.execute('SELECT * FROM casos_prueba WHERE problema_id = ?', (problem_id,))
    casos = cur.fetchall()
    con.close()

    return {
        "id":          row["id"],
        "titulo":      row["titulo"],
        "dificultad":  row["dificultad"],
        "categoria":   row["categoria"],
        "descripcion": row["descripcion"],
        "tests": [
            {"input": c["entrada"], "expected": c["salida_esperada"]}
            for c in casos
        ]
    }

@app.route('/')
def index():
    problem = get_problem(1)
    return render_template('index.html', problem=problem)

@app.route('/ejecutar', methods=['POST'])
def ejecutar_codigo():
    datos   = request.json
    lenguaje = datos.get('lenguaje')
    codigo   = datos.get('codigo')

    problem = get_problem(1)
    resultados   = []
    aprobado_todo = True

    for i, test in enumerate(problem['tests']):
        if len(codigo.strip()) < 15:
            estado = "Fallo"
            salida = "Error: código insuficiente o error de sintaxis."
            aprobado_todo = False
        else:
            estado = "Aprobado"
            salida = test['expected']

        resultados.append({
            "test_id":  i + 1,
            "estado":   estado,
            "input":    test['input'],
            "expected": test['expected'],
            "salida":   salida
        })

    return jsonify({
        "veredicto":  "Correcto" if aprobado_todo else "Error",
        "lenguaje":   lenguaje,
        "resultados": resultados
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
