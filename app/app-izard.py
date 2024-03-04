from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import joblib 


app = Flask(__name__)

model = joblib.load('app/models/model.pkl')

@app.route('/')
def home():
    return redirect(url_for('predict'))
    
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])
        scaler = joblib.load('app/models/scaler.pkl')
        scaled_data = scaler.transform(df)

        prediction = model.predict(scaled_data)
        return jsonify({'prediction': int(prediction[0]), 'model_acc' : 0.81}), 200

    except ValueError as e:
        return f'Donnée invalide, veuillez remplir le form a nouveau. Erreur: {str(e)}', 400

@app.route('/health')
def health():
    return 'Server is running and healthy', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
