from flask import Flask, request, render_template
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        pclass = request.form['pclass']
        sex = request.form['sex']
        age = request.form['age']
        sibsp = request.form['sibsp']
        parch = request.form['parch']
        fare = request.form['fare']
        embarked = request.form['embarked']
        who = request.form['who']
        alone = request.form['alone']
    try:
        pclass = int(pclass)
        sex = int(sex)
        age = int(age)
        sibsp = int(sibsp)
        parch = int(parch)
        fare = int(fare)
        embarked = int(embarked)
        who = int(who)
        adult_male = True if who == 1 else False
        alone = bool(alone)                

        data = {'pclass': [pclass],
            'sex': [sex],
            'age': [age],
            'sibsp': [sibsp],
            'parch': [parch],
            'fare': [fare],
            'embarked': [embarked],
            'who': [who],
            'adult_male': [adult_male],
            'alone': [alone]}

        df = pd.DataFrame(data)
        scaler = joblib.load('scaler_titanic.pkl')
        scaled_data = scaler.transform(df)

        prediction = model.predict(scaled_data)
        return f'Prediction: {"Il aurait survécu" if prediction == 1 else "Il n aurait pas survécu"}'
    except ValueError as e:
        return f'Donnée invalide, veuillez remplir le form a nouveau. Erreur: {e}'
    
@app.route('/home')
def home():
    return "Welcome to the Titanic survival prediction app"


app.run(host='0.0.0.0', port=8080)