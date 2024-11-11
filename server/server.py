from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from algorithms import *
import validators

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/', methods=['GET'])
def hello():
    return jsonify(message="Hola"), 200

@app.route('/predict', methods=['POST'])
def predict_LonelyURL():
    try:
        # Obtener la URL desde el cuerpo de la solicitud JSON
        data = request.get_json()
        print(data)
        URL = data.get('url')

        if not URL or not validators.url(URL):
            print("URL no válida")
            return jsonify([-1]), 400

        prediction = final_prediction(URL)
        print(prediction)
        if len(prediction) == 0:
            return jsonify([0, "Legitim"])
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/predictgroup', methods=['POST'])
def predict_GroupURL():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    try:
        print("Here!")
        prediction = group_final_prediction(file)

        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
