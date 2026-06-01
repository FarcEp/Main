from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base de datos simulada en memoria para la demo en vivo
PROBLEMAS = {
    1: {
        "id": 1,
        "titulo": "71. Simplify Path",
        "dificultad": "Medium",
        "categoria": "Stack",
        "descripcion": "Dada una ruta absoluta para un sistema de archivos, conviértela a la ruta canónica simplificada. Ignora los puntos simples '.' y maneja los dobles '..' subiendo un nivel de directorio.",
        "tests": [
            {"input": '"/home/"', "expected": '"/home"'},
            {"input": '"/../"', "expected": '"/"'},
            {"input": '"/home//foo/"', "expected": '"/home/foo"'}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', problem=PROBLEMAS[1])

@app.route('/ejecutar', methods=['POST'])
def ejecutar_codigo():
    datos = request.json
    lenguaje = datos.get('lenguaje')
    codigo = datos.get('codigo')
    
    resultados = []
    aprobado_todo = True
    
    # Simulación de evaluación
    for i, test in enumerate(PROBLEMAS[1]['tests']):
        if len(codigo.strip()) < 15:
            estado = "Fallo"
            salida = "Error: Código insuficiente o error de sintaxis."
            aprobado_todo = False
        else:
            estado = "Aprobado"
            salida = test['expected']
            
        resultados.append({
            "test_id": i + 1,
            "estado": estado,
            "input": test['input'],
            "expected": test['expected'],
            "salida": salida
        })
        
    return jsonify({
        "veredicto": "Correcto" if aprobado_todo else "Error",
        "lenguaje": lenguaje,
        "resultados": resultados
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
