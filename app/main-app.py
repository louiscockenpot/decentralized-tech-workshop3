from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
from math import fsum
import json

app = Flask(__name__)

urls = []

@app.route('/register_model', methods=['GET', 'POST'])
def register_model():
    global urls

    if request.method == 'GET':
        file_path = 'app/data/json_database.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        if "models" in data:
            models = data["models"]
            urls = [model['model_url'] for model in models]        
            
        return render_template('form-registration.html')
    
    elif request.method == 'POST':
        model_url = request.form['model_url']                
        model_acc = float(request.form['model_accuracy'])
        deposit = float(request.form['deposit'])
        urls.append(model_url)
        new_data = {            
            "model_url": model_url,
            "model_acc": model_acc,
            "deposit": deposit,
            "predictions_count": 0,
            "penalties": 0           
        }

        file_path = 'app/data/json_database.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if any(model['model_url'] == model_url for model in data.get("models", [])):
            return render_template('form-registration.html', error_message='Model already registered')
        
        if "models" in data:
            data["models"].append(new_data)
        else:
            data["models"] = [new_data]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return redirect(url_for('predict'))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    file_path = 'app/data/json_database.json'
    with open(file_path, 'r') as file:
        data_models = json.load(file)

    if "models" in data_models:
        models = data_models["models"]

    if request.method == 'GET':                
        return render_template('form.html')
    
    elif request.method == 'POST':
        data = {
            'pclass': int(request.form['pclass']),
            'sex': int(request.form['sex']),
            'age': int(request.form['age']),
            'sibsp': int(request.form['sibsp']),
            'parch': int(request.form['parch']),
            'fare': float(request.form['fare']),
            'embarked': int(request.form['embarked']),
            'who': int(request.form['who']),
            'adult_male': request.form['who'] == 'men',
            'alone': not (int(request.form['sibsp']) > 0 or int(request.form['parch']) > 0)
        }

        predictions = []
        sum_weights = 0

        for model in models:
            response = requests.post(model['model_url'], json=data)

            if response.status_code == 200:
                prediction = response.json()['prediction']
                weight = model['model_acc']
                sum_weights += weight            
                predictions.append((prediction, weight))
            else:
                return response.text, response.status_code                
            
        weighted_sum_predictions = fsum(prediction * weight for prediction, weight in predictions) / sum_weights
        consensus_prediction = round(weighted_sum_predictions)

        #update models
        for i, model in enumerate(models):
            model['predictions_count'] += 1
            if consensus_prediction == predictions[i][0]:
                model['penalties'] += 1
                model['deposit'] -= 0.1 * model['deposit']
                model['model_acc'] -= 0.1 * model['model_acc']

        data_models["models"] = models
        with open(file_path, 'w') as file:
            json.dump(data_models, file, indent=4)        

        traveler_status = 'He would have survived' if consensus_prediction == 1.0 else 'He would have died mskn'
        return f'All predictions: {predictions} -- Consensus prediction: {traveler_status} ({weighted_sum_predictions})', 200


@app.route("/")
def home():
    return redirect(url_for("register_model"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
