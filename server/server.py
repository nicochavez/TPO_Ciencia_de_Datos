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
            return jsonify(-1), 400
        


        if final_prediction(URL):
            return jsonify(1)
        
        return jsonify(0)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/predictgroup', methods=['POST'])
def predict_GroupURL():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    try:
        # Leer el archivo CSV en un DataFrame
        csvDF = pd.read_csv(file)

        # Extraer la columna de URLs (suponiendo que la columna se llama 'url')
        df_urlPredict = csvDF[['url']]
        
        # Calcular las características de las URLs
        df_urlPredict = valueCalc(df_urlPredict)
        
        # Eliminar la columna 'url' antes de la predicción
        df_urlPredict.drop('url', axis=1, inplace=True)

        MLNB = get_MLNB()

        # Realizar la predicción
        prediction = MLNB.predict(df_urlPredict)

        finalDF = csvDF[['url']]
        finalDF['prediction'] = prediction
        finalDF['finalPrediction'] = complementaryPrediction(finalDF['url'], finalDF['prediction'])       

        # Contar las predicciones y crear el resultado
        prediction_counts = pd.Series(finalDF['finalPrediction']).value_counts().to_dict()

        return jsonify(prediction_counts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
